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
import sys


# this script only runs in "/opt/lago-corsika-CORSIKA_VER/run" directory
def _get_corsika_version():

    try:
        return os.getcwd().split("/opt/lago-corsika-")[1].split("/run")[0]
    except Exception as inst:
        print("Please, execute in the /opt/lago-corsika-CORSIKA_VER/run directory")
        sys.exit(1)


def _get_arti_params_json_md(arti_dict):

    dict_aux = {
                "@id": "/" + arti_dict['p'] + "#artiParams",
                "@type": "lago:ArtiParams",
                "lago:fluxTime": "P" + str(arti_dict['t']) + "S",
                "lago:highEnergyIntModel": arti_dict['h'],
                "lago:detectorSite":
                    "https://github.com/lagoproject/DMP/blob/1.1/defs/sitesLago.jsonld#"
                    + arti_dict['s'],
                "lago:obsLev": arti_dict['k'],
                "lago:modatm": arti_dict['c'],
                "lago:rigidity": arti_dict['b'],
                "lago:tMin": arti_dict['m'],
                "lago:tMax": arti_dict['n'],
                "lago:llimit": arti_dict['r'],
                "lago:ulimit": arti_dict['i'],
                "lago:bx": arti_dict['o'],
                "lago:bz": arti_dict['q'],
                "lago:flatArray": not arti_dict['y'],
                "lago:cherenkov": arti_dict['e'],
                "lago:debug": arti_dict['d'],
                "lago:defaults": arti_dict['x'],
                "lago:highEnergyCutsSecondaries": arti_dict['a']
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

    # parser.add_argument('-sum', dest='accumulate', default=max,
    #                   help='sum the integers (default: find the max)')

    # parser.add_argument('-sum', dest='accumulate', default=max,
    #                   help='sum the integers (default: find the max)')
    #
    #
    # showhelp() {
    #  echo
    #  echo -e "$0 version $VERSION"
    #  echo
    #  echo -e "USAGE $0:"
    #  echo
    #  echo -e "  -w <working dir> : \
    #    Working directory, where bin (run) files are located"
    # removed for OneData
    #  echo -e "  -p <project name> : \
    #    Project name (suggested format: NAMEXX)"
    # project name is set by the script as a fixed CODENAME
    #  echo -e "  -t <flux time> : \
    #    Flux time (in seconds) for simulations"
    parser.add_argument('-t', dest='t', required=True, type=int,
                        help='Flux time (in seconds) for simulations')
    #  echo -e "  -v <CORSIKA version> : \
    #    CORSIKA version"
    # fixed, every docker image has their own CORSIKA version
    #  echo -e "  -h <HE Int Model (EPOS|QGSII)> : \
    #    Define the high interaction model to be used"
    parser.add_argument('-h', dest='h', required=True,
                        choices=['EPOS', 'QGSII'],
                        help='Define the high interaction model to be used \
                        <(EPOS|QGSII)>')
    #  echo -e "  -u <user name>                 : User Name."
    parser.add_argument('-u', dest='u', required=True,
                        help='ORCID code describing user, plain usernames are \
                        no allowed for publication')
    #  echo -e "  -s <site> : \
    #    Location (several options)"
    parser.add_argument('-s', dest='s', required=True,
                        # choices=[ "QUIE","and","asu","ber","bga","brc","bue",
                        #           "cha","chia","cpv","cuz","gua","kna","lim",
                        #           "lpb","lsc","mapi","mge","pam","sac","sao",
                        #           "sawb","serb","sng","tac","tuc","vcp" ],
                        help='Predefined LAGO site')
    #  echo -e "  -j <procs> : \
    #    Number of processors to use"
    parser.add_argument('-j', dest='j', type=int, default=1,
                        help='Number of processors to use')
    #  echo -e "  -y : \
    #    Select volumetric detector mode (default=flat array)"
    parser.add_argument('-y', action='store_true', default=None,
                        help='Select volumetric detector mode \
                        (default=flat array)')
    #  echo -e "  -e : \
    #    Enable CHERENKOV mode"
    parser.add_argument('-e', action='store_true', default=None,
                        help='Enable CHERENKOV mode')
    #  echo -e "  -d : \
    #    Enable DEBUG mode"
    parser.add_argument('-d', action='store_true', default=None,
                        help='Enable DEBUG mode')
    #  echo -e "  -a : \
    #    Enable high energy cuts for secondaries"
    # added by HA - Now -a option expect the ecut value in GeV. 04/OCT/2021
    # parser.add_argument('-a', action='store_true', default=None,
    #                    help='Enable high energy cuts for secondaries')
    parser.add_argument('-a', dest='a', type=float, default=0.0,
                        help='Enable and set high energy cuts for secondaries, \
                        0 = disabled; value in GeV = enabled')
    #  echo -e "  -k <altitude, in cm> : \
    #    Fix altitude, even for predefined sites"
    parser.add_argument('-k', dest='k', type=float,
                        help='Fix altitude, even for predefined sites, in cm, \
                        float and scientific notation allowed')
    #  echo -e "  -c <modatm> : \
    #    Atmospheric Model even for predefined sites"
    parser.add_argument('-c', dest='c',
                        help='Atmospheric Model even for predefined sites. \
                        Note: Start number with E to use external atmospheres \
                        module')
    #  echo -e "  -b <rigidity cutoff> : \
    #    Rigidity cutoff; 0 = disabled; value in GV = enabled"
    parser.add_argument('-b', dest='b', default=0.0,
                        help='Rigidity cutoff; 0 = disabled; value in GV = \
                        enabled')
    #  echo -e "  -m <Low edge zenith angle> : \
    #    Low edge of zenith angle (THETAP) [deg]"
    parser.add_argument('-m', dest='m', type=float,
                        help='Low edge of zenith angle (THETAP) [deg]')
    #  echo -e "  -n <High edge zenith angle> : \
    #    High edge of zenith angle (THETAP) [deg]"
    parser.add_argument('-n', dest='n', type=float,
                        help='High edge of zenith angle (THETAP) [deg]')
    #  echo -e "  -r<Low primary particle energy> : \
    #    Lower limit of the primary particle energy (ERANGE) [GeV]"
    parser.add_argument('-r', dest='r', type=float,
                        help='Lower limit of the primary particle \
                       energy (ERANGE) [GeV]')
    #  echo -e "  -i<Upper primary particle energy> : \
    #    Upper limit of the primary particle energy (ERANGE) [GeV]"
    parser.add_argument('-i', dest='i', type=float,
                        help='Upper limit of the primary particle \
                        energy(ERANGE) [GeV]')
    #  echo -e "  -o<BX> : \
    #    Horizontal comp. of the Earth's mag. field"
    parser.add_argument('-o', dest='o', type=float,
                        help='Horizontal comp. of the Earth mag. field')
    #  echo -e "  -q<BZ> : \
    #    Vertical comp. of the Earth's mag. field"
    parser.add_argument('-q', dest='q', type=float,
                        help='Vertical comp. of the Earth mag. field')
    #  echo -e "  -x : \
    #    Enable other defaults (It doesn't prompt user for unset parameters)"
    parser.add_argument('-x', action='store_true', default=None,
                        help="Enable other defaults (It doesn\
                        't prompt user for unset parameters)")
    #  echo -e "  -? : \
    #    Shows this help and exit."
    parser.add_argument('-?', action='help', help='Shows this help and exit.')
    #  echo
    # }

    args = parser.parse_args()
    args_dict = vars(args)

    # ---- customise parameters for ARTI and onedataSim ----
    #
    # the most important is the "project name" that it is used
    # for onedataSim as "codename"
    #
    # the other are the version of external software used
    # and the working dir

    # version of external software (Corsika version)
    CORSIKA_VER = _get_corsika_version()
    args_dict.update({'v': CORSIKA_VER})

    # project a.k.a codename
    # it should describe a simulation

    codename = 'S0_' + args_dict['s'] + '_' + str(args_dict['t'])

    if args_dict['k'] is not None:
        codename += '_' + str(args_dict['k'])

    codename += '_' + args_dict['v'] + '_' + args_dict['h']

    if args_dict['y'] is True:
        codename += '_volu'
    else:
        codename += '_flat'

    if args_dict['e'] is True:
        codename += '_Cherenk'

    if args_dict['a'] is True:
        codename += '_HEcuts' + str(args_dict['a'])

    if args_dict['x'] is True:
        codename += '_defaults'

    args_dict.update({'p': codename})

    # working dir

    args_dict.update({'w': '/opt/lago-corsika-'+CORSIKA_VER+'/run/'})

    return (codename, args_dict, _get_arti_params_json_md(args_dict))
