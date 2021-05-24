#
###############################################################################
# Original Author: A.J. Rubio-Montero (http://orcid.org/0000-0001-6497-753X), #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track),#
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).        #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause) #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)  #
###############################################################################


# note:
# command line, arti_params identical than do_sim.sh in ARTI.
# https://docs.python.org/3.3/library/argparse.html

import argparse
import os

###CORSIKA_VER = '77402'

def _get_arti_params_json_md(arti_dict):

    dict_aux = {
         "@id": "/"+arti_dict['p']+"#artiParams",
         "@type": "lago:ArtiParams",
         "lago:detectorSite":
         "https://github.com/lagoproject/DMP/blob/1.1/defs/sitesLago.jsonld#"
         + arti_dict['s']
         #....
         #....
         # YOU SOULDH OBTAIN SOME PARAMETERS FROM THE S0 METADATA
         # OTHERS FROM PARAMETERS...
 
         }

    # create JSON removing empty values

    j = {"@graph": [
        {k: v for k, v in dict_aux.items() if v is not None}
        ]}

    return j


def get_sys_args_S0():

    disclaimer = 'do_onedata: simulating LAGO sites and storing/publishing \
    results in OneData'
    # epilog= "this can be ASCII art"
    parser = argparse.ArgumentParser(description=disclaimer, add_help=False)

    # YOU SHOULD PARSE EVERY ARGUMENT
    
    
    #  echo -e "  -t <flux time> : \
    #    Flux time (in seconds) for simulations"
    parser.add_argument('-t', dest='t', required=True, type=int,
                        help='Flux time (in seconds) for simulations')
    # ... parser.add_argument ...
    # ... parser.add_argument ...
    # ... parser.add_argument ...

    args = parser.parse_args()

    args_dict = vars(args)
    
    
    # ---- customise parameters for ARTI and onedataSim ----
    # 
    # the most important is the "project name" that it is used 
    # for onedataSim as "codename"
    #
    # the other are the version of external software used
    # and the working dir
     
    # version of external software 
    
    # for S1 there no are external software
    #### args_dict.update({'v': CORSIKA_VER})

    # project a.k.a codename
    # it should describe a simulation

    # codename is identical to the S0 origin, but begins with S1
    S0_codename = "S0_blah_blah...."
    S0_codename_tail= S0_codename[3:]
    codename = 'S1_' + S0_codename_tail

    args_dict.update({'p': codename})

    # working dir
    
    args_dict.update({'w': os.getcwd()})

 
    return (codename, args_dict, _get_arti_params_json_md(args_dict))
