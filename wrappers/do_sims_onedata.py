#!/usr/bin/env python3
#
###############################################################################
# Original Author: A.J. Rubio-Montero (http://orcid.org/0000-0001-6497-753X), #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track),#
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).        #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause) #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)  #
###############################################################################


# additional modules needed
# apt-get install python3-xattr
# or yum install -y python36-pyxattr
import os
import shutil

from queue import Queue

# own functions
import args_sims

import mdUtils
import osUtils


from ARTIwrapper import ARTIwrapper


# ---- specific metadata for S0 datasets (corsika files) ----

def _get_input_metadata(filecode):

    args = ['common_activity.json', 'dataset_corsika_input.json']
    s = mdUtils.get_metadata_for_dataset(args)
    s = s.replace('FILENAME', 'DAT' + filecode + '.input')
    # DCAT2 distribution:format & mediaType
    s = s.replace('FORMAT', 'TXT')
    s = s.replace('MEDIATYPE', 'text')
    # warning, corsikainput metadata must be included also...
    return s


def _get_bin_output_metadata(filecode):

    args = ['common_dataset_corsika_output.json',
            'dataset_corsika_bin_output.json']
    s = mdUtils.get_metadata_for_dataset(args)
    runnr = filecode.split('-')[0]
    s = s.replace('FILENAME', 'DAT' + runnr + '.bz2')
    # DCAT2 distribution:format & mediaType
    s = s.replace('FORMAT', 'BIN')
    s = s.replace('MEDIATYPE', 'octet-stream')
    return s


def _get_lst_output_metadata(filecode):

    args = ['common_dataset_corsika_output.json',
            'dataset_corsika_lst_output.json']
    s = mdUtils.get_metadata_for_dataset(args)
    s = s.replace('FILENAME', 'DAT' + filecode + '.lst.bz2')
    # DCAT2 distribution:format & mediaType
    s = s.replace('FORMAT', 'TXT')
    s = s.replace('MEDIATYPE', 'text')
    # falta comprimir si fuera necesario
    return s


def get_dataset_metadata_S0(catcodename, filecode, startdate, end_date,
                            arti_params_dict):

    mdlistaux = [_get_bin_output_metadata(filecode),
                 _get_lst_output_metadata(filecode),
                 _get_input_metadata(filecode)]
    mdlist = []
    for s in mdlistaux:
        s = mdUtils.replace_common_patterns(s, catcodename, arti_params_dict)
        s = s.replace('NRUN', filecode)
        s = s.replace('STARTDATE', startdate)
        s = s.replace('ENDDATE', end_date)
        mdlist.append(s)
    return mdlist

# ---- END: specific metadata for S0 datasets (corsika files) ----


# ---- specific producer for S0 datasets (corsika) ----

def producerS0(catcodename, arti_params):

    q = Queue()

    # clean a possible previous simulation
    if os.path.exists(catcodename):
        shutil.rmtree(catcodename, ignore_errors=True)

    # WARNING, I HAD TO LINK BRANCH IN corsika binary
    aux_list = arti_params.split(' ')
    corsika_ver = aux_list[aux_list.index('-v') + 1]
    try:
        ver_only_num = corsika_ver.split('-')[0]
        for file in os.listdir():
            if file.startswith("corsika") and not os.path.islink(file):
                link = file.replace(ver_only_num, corsika_ver)
                if not os.path.exists(link):
                    cmd = 'ln -s ' + file + ' ' + link
                    osUtils.run_Popen_interactive(cmd)
                    print('Link created: ' + link)
    except Exception as inst:
        pass

    # PATCH: correct the creation of tasks, which is based on (-j) in ARTI.
    #        ARTI tries fit the number of tasks (NRUN) to the number of procs
    #        for being correct in terms of physics, however was not implemented
    #        for fit the output sizes vs flux-time (arti_params[t])

    params_aux_flux = arti_params[arti_params.find("-t")+3:]
    flux_time = int(params_aux_flux[:params_aux_flux.find("-")])

    params_aux = arti_params[arti_params.find("-j")+3:]
    old_j = int(params_aux[:params_aux.find("-")])

    aux_j = int(int(flux_time)/900)
    if aux_j == 0:
        aux_j = 1
    if aux_j > 12:
        aux_j = 12
    arti_params = arti_params[:arti_params.find("-j")] + "-j " + str(aux_j) + " " + params_aux[params_aux.find("-"):]

    print("PATCH: change -j : " + str(old_j) + " by :" + str(aux_j) + " to generate tasks")

    # generate tasks
    cmd = 'do_sims.sh ' + arti_params
    osUtils.run_Popen_interactive(cmd)

    # WARNING, I HAD TO PATCH rain.pl FOR AVOID SCREEN !!!!
    cmd = "sed 's/screen -d -m -a -S \$name \$script; screen -ls/\$script/' " + \
          " rain.pl -i"
    osUtils.run_Popen(cmd)

    # WARNING, I HAD TO PATCH rain.pl FOR AVOID .long files !!!
    # 20210519 not necessary since arti@d8f8caa
    # cmd = "sed 's/\$llongi /F /' rain.pl -i"
    # osUtils.run_Popen(cmd)

    # -g only creates .input's
    # cmd="sed 's/\.\/rain.pl/echo \$i: \.\/rain.pl -g /' go-*.sh  -i"
    cmd = "sed 's/\.\/rain.pl/echo \$i: \.\/rain.pl /' go-*.sh  -i"
    osUtils.run_Popen(cmd)
    cmd = "cat go-*.sh | bash  2>/dev/null"
    lines = osUtils.run_Popen(cmd).decode("utf-8").split('\n')
    for z in lines:
        if z != "":
            print(z)
            z_aux = z.split(":")
            runnr = z_aux[0]
            # prmpar name only allows 4 characters, we use zfill to fill with
            #  0's and limit to 4 characters if were needed.
            prmpar = str(int(runnr)).zfill(4)[-4:]
            task = z_aux[1]
            z_aux = task.split(catcodename)
            s_aux = z_aux[1].replace('/', '')
            s_aux = z_aux[1].replace('.run', '')
            z_aux = s_aux.split('-')
            # runnr has at least 6 characters, but can has more
            runnr_6 = str(int(runnr)).zfill(6)
            filecode = runnr_6 + '-' + prmpar + '-' + z_aux[1]
            q.put((filecode, task))

    return q


# ---- MAIN run ----

simulation = ARTIwrapper(args_sims.get_sys_args_S0, get_dataset_metadata_S0,
                         producerS0)
simulation.run()
