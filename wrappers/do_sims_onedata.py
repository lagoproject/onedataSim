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
import xattr
import json
import shutil

from queue import Queue

# own functions
from arguments import get_sys_args
from utils import _run_Popen, _run_Popen_interactive, 
    _add_json, _replace_common_patterns, _get_common_metadata_aux

from ARTIwrapper import ARTIwrapper




# ---- specific metadata for S0 datasets (corsika files) ----

onedataSimPath = os.path.dirname(os.path.abspath(__file__))

def _get_input_metadata(filecode):

    with open(onedataSimPath+'/json_tpl/common_activity.json',
              'r') as file1:
        with open(onedataSimPath+'/json_tpl/dataset_corsika_input.json',
                  'r') as file2:
            j = _get_common_metadata_aux()
            j = _add_json(j, json.loads(file1.read()))
            j = _add_json(j, json.loads(file2.read()))
            s = json.dumps(j)
            s = s.replace('FILENAME', 'DAT'+filecode+'.input')
            # DCAT2 distribution:format & mediaType
            s = s.replace('FORMAT', 'TXT')  
            s = s.replace('MEDIATYPE', 'text') 
            # warning, corsikainput metadata must be included also...
            return s


def _get_bin_output_metadata(filecode):

    with open(onedataSimPath+'/json_tpl/common_dataset_corsika_output.json',
              'r') as file1:
        with open(onedataSimPath +
                  '/json_tpl/dataset_corsika_bin_output.json',
                  'r') as file2:
            j = _get_common_metadata_aux()
            j = _add_json(j, json.loads(file1.read()))
            j = _add_json(j, json.loads(file2.read()))
            s = json.dumps(j)
            runnr = filecode.split('-')[0]
            s = s.replace('FILENAME', 'DAT'+runnr+'.bz2')
            # DCAT2 distribution:format & mediaType
            s = s.replace('FORMAT', 'BIN')  
            s = s.replace('MEDIATYPE', 'octet-stream') 
            return s


def _get_lst_output_metadata(filecode):

    with open(onedataSimPath+'/json_tpl/common_dataset_corsika_output.json',
              'r') as file1:
        with open(onedataSimPath +
                  '/json_tpl/dataset_corsika_lst_output.json',
                  'r') as file2:
            j = _get_common_metadata_aux()
            j = _add_json(j, json.loads(file1.read()))
            j = _add_json(j, json.loads(file2.read()))
            s = json.dumps(j)
            s = s.replace('FILENAME', 'DAT'+filecode+'.lst.bz2')
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
        s = _replace_common_patterns(s, catcodename, arti_params_dict)
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

    cmd = 'do_sims.sh ' + arti_params
    _run_Popen_interactive(cmd)

    # WARNING, I HAD TO PATCH rain.pl FOR AVOID SCREEN !!!!
    cmd = "sed 's/screen -d -m -a -S \$name \$script; screen -ls/\$script/' " + \
       " rain.pl -i"
    _run_Popen(cmd)
    
    # WARNING, I HAD TO PATCH rain.pl FOR AVOID .long files !!!
    cmd = "sed 's/\$llongi /F /' rain.pl -i"
    _run_Popen(cmd)

    # -g only creates .input's
    # cmd="sed 's/\.\/rain.pl/echo \$i: \.\/rain.pl -g /' go-*.sh  -i"
    cmd = "sed 's/\.\/rain.pl/echo \$i: \.\/rain.pl /' go-*.sh  -i"
    _run_Popen(cmd)
    cmd = "cat go-*.sh | bash  2>/dev/null"
    lines = _run_Popen(cmd).decode("utf-8").split('\n')
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
            filecode = runnr_6 + '-' +prmpar +'-' + z_aux[1]
            q.put((filecode, task))

    return q


# ---- MAIN run ----

simulation = ARTIwrapper(get_sys_args, get_dataset_metadata_S0, producerS0)
simulation.run()





