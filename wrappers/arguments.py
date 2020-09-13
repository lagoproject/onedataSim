#
################################################################################
# Original Author: A.J. Rubio-Montero (http://orcid.org/0000-0001-6497-753X),  #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track), #
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).         #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause)  #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)   #
################################################################################


# note:
# command line, arti_params identical than do_sim.sh in ARTI.
# https://docs.python.org/3.3/library/argparse.html

import argparse, sys
#from builtins import int

CORSIKA_VER='75600'

def _get_arti_params_json_md(arti_dict):
    
    j= {"@graph" : [
    {
     "@id" : "/"+arti_dict['p']+"#artiParams",
     "@type" : "lago:ArtiParams",
     "lago:fluxTime" : "P"+str(arti_dict['p'])+"S", 
     "lago:highEnergyIntModel" : arti_dict['h'], 
     "lago:detectorSite" : "https://github.com/lagoproject/DMP/blob/0.0.1/defs/sitesLago.jsonld#"+arti_dict['s'],
     "lago:obsLev" : arti_dict['k'],     
     "lago:flatArray" : not arti_dict['y'],                      
     "lago:cherenkov" : arti_dict['e'],
     "lago:debug" : arti_dict['k'], 
     "lago:highEnergyCutsSecondaries" : arti_dict['a']
    }
    ]}
    return j

def get_sys_args():

    disclaimer='do_onedata: simulating LAGO sites and storing/publishing results in OneData' 
    #epilog= "this can be ASCII art"
    parser = argparse.ArgumentParser(description=disclaimer, add_help=False)
    
    #parser.add_argument('-sum', dest='accumulate', default=max,
    #                   help='sum the integers (default: find the max)')
    
    #parser.add_argument('-sum', dest='accumulate', default=max,
    #                   help='sum the integers (default: find the max)')
    
    
    #showhelp() {
    #  echo 
    #  echo -e "$0 version $VERSION"
    #  echo 
    #  echo -e "USAGE $0:"
    #  echo
    #  echo -e "  -w <working dir>               : Working directory, where bin (run) files are located"
    #removed for OneData
    #  echo -e "  -p <project name>              : Project name (suggested format: NAMEXX)"
    #project name is set by the script as a fixed CODENAME 
    #  echo -e "  -t <flux time>                 : Flux time (in seconds) for simulations"
    parser.add_argument('-t', dest='t', required=True, type=int,
                       help='Flux time (in seconds) for simulations')
    #  echo -e "  -v <CORSIKA version>           : CORSIKA version"
    # fixed, every docker image has their own CORSIKA version
    #  echo -e "  -h <HE Int Model (EPOS|QGSII)> : Define the high interaction model to be used"
    parser.add_argument('-h', dest='h', required=True, choices=['EPOS', 'QGSII'],
                       help='Define the high interaction model to be used <(EPOS|QGSII)>')
    #  echo -e "  -u <user name>                 : User Name."
    parser.add_argument('-u', dest='u', required=True,
                       help='ORCID code describing user, plain usernames are no allowed for publication')
    #  echo -e "  -s <site>                      : Location (several options)"
    parser.add_argument('-s', dest='s', required=True, choices=["hess","sac","etn","ber","lim","glr",
                                                                "mch","bga","mge","brc","and","mpc",
                                                                "cha","cid","mor","lsc","mbo","ccs"],     
                       help='Predefined LAGO site')
    #  echo -e "  -j <procs>                     : Number of processors to use"
    parser.add_argument('-j', dest='j', default=1,
                       help='Number of processors to use')
    #  echo -e "  -y                             : Select volumetric detector mode (default=flat array)"
    parser.add_argument('-y', action='store_true', default=None,
                       help='Select volumetric detector mode (default=flat array)')
    #  echo -e "  -e                             : Enable CHERENKOV mode"
    parser.add_argument('-e', action='store_true', default=None,
                       help='Enable CHERENKOV mode')
    #  echo -e "  -d                             : Enable DEBUG mode"
    parser.add_argument('-d', action='store_true', default=None,
                       help='Enable DEBUG mode')
    #  echo -e "  -a                             : Enable high energy cuts for secondaries"
    parser.add_argument('-a', action='store_true', default=None,
                       help='Enable high energy cuts for secondaries')
    #  echo -e "  -k <altitude, in cm>           : Fix altitude, even for predefined sites"
    parser.add_argument('-k', dest='k', required=True, type=float,
                       help='Fix altitude, even for predefined sites, in cm, float and scientific notation allowed')
    #  echo -e "  -?                             : Shows this help and exit."
    parser.add_argument('-?', action='help', help='Shows this help and exit.')
    #  echo
    #}
    
    args = parser.parse_args()
    
    args_dict=vars(args)
    
    #add working dir, project, and corsika version...
    
    args_dict.update({'v':CORSIKA_VER})
    
    #project a.k.a codename
    #it shoulds describe a simulation 
    
    codename=args_dict['s'] +'_'+ str(args_dict['t']) +'_'+ str(args_dict['k']) +'_'+ args_dict['v'] +'_'+ args_dict['h']
    if args_dict['y'] is True:
        codename+='_volu'
    else: 
        codename+='_flat'
    
    if args_dict['e'] is True:
        codename+='_Cherenk'
        
    if args_dict['a'] is True:
        codename+='_HEcuts'
    
        
    args_dict.update({'p': codename})
    
    
    #working dir
    #args_dict.update({'w': '/opt/corsika-'+CORSIKA_VER+'-lago/run/'+str(args_dict['t'])})
    args_dict.update({'w': '/opt/corsika-'+CORSIKA_VER+'-lago/run/'})
    
    s=''
    for (key,value) in args_dict.items():
        if value is not None:
            s+=' -'+key
            if value is not True:
                s+=' '+str(value)
    
    return (s, args_dict, _get_arti_params_json_md(args_dict))









