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

#EXAMPLE of possible standard modules needed
import xattr
import json
import os
import shutil

from queue import Queue

# own functions
import args_showers

import mdUtils
import osUtils


from ARTIwrapper import ARTIwrapper

# ---- specific metadata for S1 datasets (ARTI analyisis files) ----

# output primaries
def _get_pri_metadata(filecode):

    args=['common_activity.json', 'dataset_arti_pri_output.json']
    s = mdUtils.get_metadata_for_dataset(args)
    s = s.replace('FILENAME', filecode +'.pri.bz2')
    # DCAT2 distribution:format & mediaType
    s = s.replace('FORMAT', 'TXT')  ## BIN or TXT
    s = s.replace('MEDIATYPE', 'text')  ## octect-stream or text
    return s

def _get_sec_metadata(filecode):

    args=['common_activity.json', 'dataset_arti_sec_output.json']
    s = mdUtils.get_metadata_for_dataset(args)
    s = s.replace('FILENAME', filecode + '.sec.bz2')
    # DCAT2 distribution:format & mediaType
    s = s.replace('FORMAT', 'TXT')  ## BIN or TXT
    s = s.replace('MEDIATYPE', 'text')  ## octect-stream or text
    return s

def _get_shw_metadata(filecode):

    args=['common_activity.json', 'dataset_arti_shw_output.json']
    s = mdUtils.get_metadata_for_dataset(args)
    s = s.replace('FILENAME', filecode + '.shw.bz2')
    # DCAT2 distribution:format & mediaType
    s = s.replace('FORMAT', 'TXT')  ## BIN or TXT
    s = s.replace('MEDIATYPE', 'text')  ## octect-stream or text
    return s


def _get_prt_metadata(filecode):

    args=['common_activity.json', 'dataset_arti_prt_output.json']
    s = mdUtils.get_metadata_for_dataset(args)
    s = s.replace('FILENAME', filecode + '.prt.bz2')
    # DCAT2 distribution:format & mediaType
    s = s.replace('FORMAT', 'TXT')  ## BIN or TXT
    s = s.replace('MEDIATYPE', 'text')  ## octect-stream or text
    return s


def get_dataset_metadata_S1_pri_sec(catcodename, filecode, startdate, end_date,
                                    arti_params_dict):

    #TO BE DONE  (only illustrative)

    mdlistaux = [_get_pri_metadata(filecode),
                 _get_sec_metadata(filecode)]
    mdlist = []
    for s in mdlistaux:
        s = mdUtils.replace_common_patterns(s, catcodename, arti_params_dict)
        s = s.replace('NRUN', filecode)
        s = s.replace('STARTDATE', startdate)
        s = s.replace('ENDDATE', end_date)
        # STUFFF FOR SHW (origin of the data (ej. DAT...))
        mdlist.append(s)
    return mdlist



def get_dataset_metadata_S1_shw(catcodename, filecode, startdate, end_date,
                                arti_params_dict):

    #TO BE DONE  (only illustrative)

    mdlistaux = [_get_shw_metadata(filecode)]

    mdlist = []
    for s in mdlistaux:
        s = mdUtils.replace_common_patterns(s, catcodename, arti_params_dict)
        s = s.replace('NRUN', filecode)
        s = s.replace('STARTDATE', startdate)
        s = s.replace('ENDDATE', end_date)
        # STUFFF FOR SHW (origin of the data (ej. *.sec.bz2 ...))
        mdlist.append(s)
    return mdlist



def get_dataset_metadata_S1_prt(catcodename, filecode, startdate, end_date,
                                arti_params_dict):

    #TO BE DONE  (only illustrative)

    mdlistaux = [_get_prt_metadata(filecode)]
    mdlist = []
    for s in mdlistaux:
        s = mdUtils.replace_common_patterns(s, catcodename, arti_params_dict)
        s = s.replace('NRUN', filecode)
        s = s.replace('STARTDATE', startdate)
        s = s.replace('ENDDATE', end_date)
        # STUFFF FOR SHW (origin of the data (ej. *<element>.pri.bz2 ...))
        mdlist.append(s)
    return mdlist

# ---- END: specific metadata for S1 datasets (ARTI analyisis files) ----


# ---- specific producer for S1 datasets (arti) ----

# create: codename.run, codename.shw.run, codename.pri.run
# codename.run (DATxxxx.bz2 -> xxx.pri/sec.bz2)
# codename.shw.run (*.sec.bz2 -> codename.shw)
# codename.pri.run (*<element>.pri.bz2 -> <element>.prt)
    
def producer_S1_pri_sec(catcodename, arti_params):

    # it is need, this queue will be returned for the function
    q = Queue()

    # clean a possible previous simulation
    if os.path.exists(catcodename):
        shutil.rmtree(catcodename, ignore_errors=True)
    
    # remove -u user 
    try: 
        param_list=arti_params.split(' ')
        i = param_list.index('-u')
        param_list.pop(i) # - u    
        param_list.pop(i) # the user
        arti_params = ' '.join(param_list)   
    except:
        print("ERROR: ORCID is missed")
        raise
        
    cmd = 'do_showers.sh ' + arti_params
    osUtils.run_Popen_interactive(cmd)


    with open('./' + catcodename + '/' + catcodename + '.run', 'r') as file1:
        print(file1)
        for z in file1.readlines():
            if z != "":
                # YOU OBTAIN SOMETHING SIMILAR TO:
                # "bzip2 -d -k $i; echo $j | ${arti_path}/analysis/lagocrkread | ${arti_path}/analysis/analysis -p ${u}; rm ${j}"
                # else if .run is generated:
                # "cd $wdir; while ! cp -a $i ./; do sleep 5; done; bzip2 -d $j.bz2; echo $j | ${arti_path}/analysis/lagocrkread | ${arti_path}/analysis/analysis -p ${u}; rm ${j}; cd .."
                print(z)
                filecode = z.split("echo DAT")[1].split(" ")[0]
                task = z
                q.put((filecode, task))

    return q


def producer_S1_shw(catcodename, arti_params):

    # it is need, this queue will be returned for the function
    q = Queue()

    # clean a possible previous simulation
    # if os.path.exists(catcodename):
    #    shutil.rmtree(catcodename, ignore_errors=True)

    # cmd = 'do_showers.sh ' + arti_params
    # osUtils.run_Popen_interactive(cmd)


    with open('./' + catcodename + '/'+ catcodename + '.shw.run', 'r') as file1:
        print(file1)
        for z in file1.readlines():
            if z != "":
                # YOU OBTAIN SOMETHING SIMILAR TO:
                # "bzcat ${wdir}/*.sec.bz2 | ${arti_path}/analysis/${cmd}"
                print(z)
                filecode = z.split("echo DAT")[1].split(" ")[0]
                task = z
                q.put((filecode, task))

    return q


def producer_S1_prt(catcodename, arti_params):

    # it is need, this queue will be returned for the function
    q = Queue()

    # clean a possible previous simulation
    # if os.path.exists(catcodename):
    #    shutil.rmtree(catcodename, ignore_errors=True)

    # cmd = 'do_showers.sh ' + arti_params
    # osUtils.run_Popen_interactive(cmd)


    with open('./' + catcodename + '/' + catcodename + '.pri.run', 'r') as file1:
        print(file1)
        for z in file1.readlines():
            if z != "":
                # YOU OBTAIN SOMETHING SIMILAR TO:
                # "primaries.sh -w ${wdir} -r ${arti_path} -m ${prims}"
                # else if pri.run is generated, per element ${i}:
                # "cd $wdir; while ! cp -a ??$i ./; do sleep 5; done; \\
                #  bzcat ??${i}.pri.bz2 | grep -v "#" | awk '{print log($2)/log(10.)}' | sort -g |	awk -v bins=${prims} -v id=${i} 'BEGIN{n=0; mine=100000; maxe=-100000; bins = bins * 1.}{t[int($1*bins)]++; n++; if ($1 < mine) mine=$1; if ($1 > maxe) maxe=$1;}END{printf("# # # prt\n");printf("# # Primary energy histogram for %06d using %d bins per decade\n", id, bins);printf("# # Three column format is:\n# # energy_bin total_per_bin fraction_per_bin\n"); for (i in t) {print 10**(i/bins), t[i], t[i]*1./n; frc+=t[i]*1./n;} printf("# # Total primaries: %ld (%.2f) Emin=%.2f GeV; Emax=%.2f GeV\n", n, frc, 10**mine, 10**maxe);}' > "00${i}.prt ; \\
                #  rm ??${i}.pri.bz2; cd .."

                print(z)
                filecode = z.split("echo DAT")[1].split(" ")[0]
                task = z
                q.put((filecode, task))

    return q

# ---- MAIN run ----

simulation = ARTIwrapper(args_showers.get_sys_args_S1,
                         get_dataset_metadata_S1_pri_sec,
                         producer_S1_pri_sec)
simulation.run()

# simulation = ARTIwrapper(args_showers.get_sys_args_S1,
#                          get_dataset_metadata_S1_shw,
#                          producer_S1_shw)
# simulation.run()
# 
# simulation = ARTIwrapper(args_showers.get_sys_args_S1,
#                          get_dataset_metadata_S1_prt,
#                          producer_S1_prt)
# simulation.run()
