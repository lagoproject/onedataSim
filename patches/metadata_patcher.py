#
###############################################################################
# Original Author: A.J. Rubio-Montero (http://orcid.org/0000-0001-6497-753X), #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track),#
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).        #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause) #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)  #
###############################################################################

# CHANGELOG: SOLVED ERRORS
#
# NO me gusta - ¿cambiar tag 1.1 POR el commit??????
# - https://github.com/lagoproject/DMP/blob/1.1/defs/sitesLago.jsonld#and -> 
#        https://raw.githubusercontent.com/lagoproject/DMP/1.1/defs/sitesLago.jsonld
# - y codigos anadir LAGOsim
# - "prov:wasAssociatedWith": {"@id": "HANDLETOCDMI/LAGOsoft/corsika/corsika-75600-lago.tar.gz",
# - En JSON catalogue:  "_landing_page": "https://datahub.egi.eu/dummy_hash",  -> NO existe landing page en Catalog DCAT-AP2
# - OJO "Catalogue" y "catalogue" son los correctos en DCAT-AP2, comprobado en el GitHub.... ->   "@type": "Catalog", está mal



import argparse
import requests
import json

import mdUtils
import do_share_onedata

from fileinput import filename








# ###############
# MAIN CODE
# ###############


# External arguments for command line use
parser = argparse.ArgumentParser(description='Arguments for publishing data')
parser.add_argument('--token', help ='')
parser.add_argument('--host', help ='')  # OneData Provider !!!
parser.add_argument('--folder_id', help ='' ) #INCOMPATIBLE CON --myspace_path
parser.add_argument('--myspace_path', help ='' ) #INCOMPATIBLE CON --folder_id
parser.add_argument('--recursive', action='store_true', default=None,
                     help="Enable finding sub-catalogs and sharing the ones that weren\'t shared)")

args = parser.parse_args()

if args.myspace_path:
    args.folder_id = get_folder_id(args.myspace_path, args.host, args.token) 

if args.recursive is True:
    all_level0 = folder0_content(args.folder_id, args.host, args.token)
    for p in all_level0['children']:
        patch_catalog(args.handleservice_id, p['name'], p['id'], args.host, args.token)
else:
    if args.folder_id:
        filename = get_filename(args.folder_id, args.host, args.token)
    patch_catalog(args.handleservice_id, filename, args.folder_id, args.host, args.token)