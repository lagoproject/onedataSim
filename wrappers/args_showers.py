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


def _get_arti_params_json_md(arti_dict):
    dict_aux = {
         "@id": "/" + arti_dict['p'] + "#artiParams",
         "@type": "lago:ArtiParams",
         # "lago:detectorSite":
         # "https://github.com/lagoproject/DMP/blob/1.1/defs/sitesLago.jsonld#"+arti_dict['priv_site'], # OJO quizás no es necesario con el origen
         # "lago:originDirectory": arti_dict['o'], # OJO DEBIERA SER UN LINK AL CATALOGO S0, con un DCAT...
         "lago:energyBins": arti_dict['e'],
         "lago:distanceBins": arti_dict['d'],
         # "lago:obsLev": arti_dict['k'],
         "lago:typeFilterSec": arti_dict['s'],
         # "lago:fluxTime": arti_dict['t'],
         "lago:binsPerDecade": arti_dict['m']
    }

    # create JSON removing empty values
    j = {"@graph": [
        {k: v for k, v in dict_aux.items() if v is not None}
    ]}

    return j


def get_sys_args_S1():

    disclaimer = 'do_showers_onedata: analysis S0 simulation raw data and storing/publishing \
    results in OneData.'
    # epilog= "this can be ASCII art"
    parser = argparse.ArgumentParser(description=disclaimer, add_help=False)

    parser.add_argument('-o', dest='o', required=True,
                        help='Origin dir, where the DAT files are located.')
    # parser.add_argument('-r', dest='r', required=True,
    #                     help='ARTI installation directory, generally pointed by \$LAGO_ARTI (default).')
    # parser.add_argument('-w', dest='w', required=True,
    #                     help='Working dir, where the analysis will be done (default is current directory, ${wdir}).')
    parser.add_argument('-e', dest='e', required=False, type=int, default=20,
                        help='Number of energy secondary bins (default: $energy_bins).')
    parser.add_argument('-d', dest='d', required=False, type=int, default=20,
                        help='Number of distance secondary bins (default: $distance_bins).')
    # parser.add_argument('-p', dest='p',
    #                     help='Base name for identification of S1 files (do not use spaces). Default: odir basename.')
    parser.add_argument('-k', dest='k', required=True, type=int,
                         help='For curved mode (default), site altitude in m a.s.l. (mandatory).')
    parser.add_argument('-s', dest='s', required=False, type=int,
                        help='Filter secondaries by type: 1: EM, 2: MU, 3: HD.')
    # parser.add_argument('-t', dest='t', required=True, type=int,
    #                     help='Flux time (in seconds) for simulations.')
    parser.add_argument('-m', dest='m', required=False, type=int, default=10,
                        help='Produce files with the energy distribution of the primary flux per nuclei.')
    parser.add_argument('-j', dest='j', type=int, default=1,
                        help='Number of processors to use.')
    # parser.add_argument('-l', dest='l',
    #                     help='Execute locally. (If not, only produces .run files for posterior batch processing).')
    parser.add_argument('-?', action='help', help='Shows this help and exit.')

    # added, not equiv in do_showers:

    parser.add_argument('-u', dest='u', required=True,
                        help='ORCID code describing user, plain usernames are \
                        no allowed for publication.')

    parser.add_argument('--onedata_path', dest='onedata_path',
                        help='Changing storage path, only for testing purposes.')

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
    # args_dict.update({'v': CORSIKA_VER})

    # project a.k.a codename
    # it should describe a simulation

    # codename is identical to the S0 origin, but begins with S1
    S0_codename_full = args_dict['o']
    S0_codename = S0_codename_full.split("/")
    S0_codename = S0_codename[-1]  # last in list

    codename = 'S1_' + S0_codename.replace('S0_', '', 1)

    args_dict.update({'p': codename})

    # working dir

    args_dict.update({'w': os.getcwd()})

    # OJO PROVI: DEBERIA SACARSE DE LOS METADATOS DE S0
    # other args for ARTI showers from CODENAME
    splitted = S0_codename.split('_')
    print(splitted)
    # LAGO site
    # args_dict.update({'priv_site': splitted[1]})
    # flux time in seconds
    args_dict.update({'t': splitted[2]})
    # site altitude in m a.s.l.  #OJO BUG, SOLO FUNCIONARIA SI NO ES LA ALTURA DEFAULT
    # MUY PELIGROSO
    # lo saco y agrego -k como mandatorio
    # args_dict.update({'k': int(float(splitted[3]))})

    return (codename, args_dict, _get_arti_params_json_md(args_dict))
