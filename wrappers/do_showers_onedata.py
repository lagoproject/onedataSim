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

# ---- specific metadata for S1 datasets (corsika files) ----

# output primaries
def _get_pri_metadata(filecode):

    args=['common_activity.json', 'dataset_arti_pri_output.json']
    s = mdUtils.get_metadata_for_dataset(args)
    s = s.replace('FILENAME', filecode +'.pri.bz2')
    # DCAT2 distribution:format & mediaType
    s = s.replace('FORMAT', 'BIN')  ## BIN or TXT
    s = s.replace('MEDIATYPE', 'octet-stream')  ## octect-stream or text
    return s

def _get_sec_metadata(filecode):

    args=['common_activity.json', 'dataset_arti_sec_output.json']
    s = mdUtils.get_metadata_for_dataset(args)
    s = s.replace('FILENAME', filecode + '.sec.bz2')
    # DCAT2 distribution:format & mediaType
    s = s.replace('FORMAT', 'BIN')  ## BIN or TXT
    s = s.replace('MEDIATYPE', 'octet-stream')  ## octect-stream or text
    return s

def _get_shw_metadata(filecode):

    args=['common_activity.json', 'dataset_arti_shw_output.json']
    s = mdUtils.get_metadata_for_dataset(args)
    s = s.replace('FILENAME', filecode + '.shw.bz2')
    # DCAT2 distribution:format & mediaType
    s = s.replace('FORMAT', 'BIN')  ## BIN or TXT
    s = s.replace('MEDIATYPE', 'octet-stream')  ## octect-stream or text
    return s


def get_dataset_metadata_S1(catcodename, filecode, startdate, end_date,
                         arti_params_dict):

    #TO BE DONE  (only illustrative)

    mdlistaux = [_get_pri_metadata(filecode),
                 _get_sec_metadata(filecode),
                 _get_shw_metadata(filecode)]
    mdlist = []
    for s in mdlistaux:
        s = mdUtils.replace_common_patterns(s, catcodename, arti_params_dict)
        s = s.replace('NRUN', filecode)
        s = s.replace('STARTDATE', startdate)
        s = s.replace('ENDDATE', end_date)
        mdlist.append(s)
    return mdlist

# ---- END: specific metadata for S0 datasets (corsika files) ----


# ---- specific producer for S1 datasets (arti) ----

def producer_S1(catcodename, arti_params):

    # it is need, this queue will be returned for the function
    q = Queue()

    # clean a possible previous simulation
    if os.path.exists(catcodename):
        shutil.rmtree(catcodename, ignore_errors=True)

    cmd = 'do_showers.sh ' + arti_params
    osUtils.run_Popen_interactive(cmd)

    # IN DO_SHOWERS.SH (BASH) the section of code that proccess & create files is:
    #
    # for i in ${wdir}/DAT??????.bz2; do
    #    j=${i/.bz2/}
    #     u=${j/DAT/}
    #     run="bzip2 -d -k $i; echo $j | ${arti_path}/analysis/lagocrkread | ${arti_path}/analysis/analysis -p ${u}; rm ${j}"
    #    echo $run >> $prj.run
    # done
    # nl=$(cat $prj.run | wc -l)
    # if [ $parallel -gt 0 ]; then
    #    # parallel mode, just produce the shower analysis file and exit
    #    echo "bzcat ${wdir}/*.sec.bz2 | ${arti_path}/analysis/${cmd}" > $prj.shw.run
    #    exit 0
    #
    # THEREFORE THE FILE THAT CONTAIN FIRST EXECUTIONS IS $prj.run = "catcodename.run"  (PIMARIES?)
    # AND WHEN ALL THOSE HAS BEEN COMPLETED can execute the line in "catcodename.shw.run" (SECONDARIES?)
    #
    # This final execution is a PROBLEM.... I only centering on primaries

    with open('./' + catcodename + '/'+ catcodename + '.run', 'r') as file1:
        print(file1)
        for z in file1.readlines():
            if z != "":
                # YOU OBTAIN SOMETHING SIMILAR TO:
                # "bzip2 -d -k $i; echo $j | ${arti_path}/analysis/lagocrkread | ${arti_path}/analysis/analysis -p ${u}; rm ${j}"
                # AND YOU SHOUD CREATE SOMETHING SIMILAR TO:
                # filecode = $i
                # task =  "cp remote_onedata/$i ." + z
                print(z)
                filecode = z.split("echo DAT")[1].split(" ")[0]
                task = z
                q.put((filecode, task))

    return q


# ---- MAIN run ----

simulation = ARTIwrapper(args_showers.get_sys_args_S1, get_dataset_metadata_S1,
                         producer_S1)
simulation.run()




