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
# 1- NO me gusta - ¿cambiar tag 1.1 POR el commit?????? NO SACA LO MISMO QUE DEV, QUE ESTÁ MEJORADO!!!!
# 2- https://github.com/lagoproject/DMP/blob/1.1/defs/sitesLago.jsonld#and -> 
#        https://raw.githubusercontent.com/lagoproject/DMP/1.1/defs/sitesLago.jsonld
# 3- y codigos anadir LAGOsim
# 4- "prov:wasAssociatedWith": {"@id": "HANDLETOCDMI/LAGOsoft/corsika/corsika-75600-lago.tar.gz",
# 5- En JSON catalogue:  "_landing_page": "https://datahub.egi.eu/dummy_hash",  -> NO existe landing page en Catalog DCAT-AP2
# 6- OJO "Catalogue" y "catalogue" son los correctos en DCAT-AP2, comprobado en el GitHub.... ->   "@type": "Catalog", está mal
# 7- OJO lago:ulimit y lago:llimit son uLimit y lLimit 



import argparse
import requests
import json

import mdUtils
import do_share_onedata as mdaux

from fileinput import filename


def patch_catalog(folder_name, folder_id, host, token):
    
    # get current metadata
    old_json = mdaux.get_json_metadata(folder_id, host, token)
    
    j_text = json.dumps(old_json)

    # 2- https://github.com/lagoproject/DMP/blob/1.1/defs/sitesLago.jsonld-> 
    #    https://raw.githubusercontent.com/lagoproject/DMP/1.1/defs/sitesLago.jsonld
    j_text.replace("https://github.com/lagoproject/DMP/blob/1.1/defs/sitesLago.jsonld",
                   "https://raw.githubusercontent.com/lagoproject/DMP/1.1/defs/sitesLago.jsonld")

    # 5- En JSON catalogue:  "'_landing_page': 'https://datahub.egi.eu/dummy_hash',"  -> NO existe landing page en Catalogue DCAT-AP2
    j_text.replace("'_landing_page': 'https://datahub.egi.eu/dummy_hash',", "")

    # 6- OJO "Catalogue" y "catalogue" son los correctos en DCAT-AP2, comprobado en el GitHub.... ->   "@type": "Catalog", está mal
    j_text.replace("'@type': 'Catalog'", "'@type': 'Catalogue'")
    

    # 7- OJO lago:ulimit y lago:llimit son uLimit y lLimit 
    j_text.replace("lago:ulimit", "lago:uLimit")
    j_text.replace("lago:llimit", "lago:lLimit")
    
    
    print(json.loads(j_text))
        



# ###############
# MAIN CODE
# ###############


# External arguments for command line use
parser = argparse.ArgumentParser(description='Enricher of metadata')
parser.add_argument('--token', help ='')
parser.add_argument('--host', help ='')  # OneData Provider !!!
parser.add_argument('--folder_id', help ='' ) #INCOMPATIBLE CON --myspace_path
parser.add_argument('--myspace_path', help ='' ) #INCOMPATIBLE CON --folder_id
parser.add_argument('--recursive', action='store_true', default=None,
                     help="Enable finding sub-catalogs and sharing the ones that weren\'t shared)")

args = parser.parse_args()

if args.myspace_path:
    args.folder_id = mdaux.get_folder_id(args.myspace_path, args.host, args.token) 

if args.recursive is True:
    all_level0 = mdaux.folder0_content(args.folder_id, args.host, args.token)
    for p in all_level0['children']:
        patch_catalog(p['name'], p['id'], args.host, args.token)
else:
    if args.folder_id:
        filename = mdaux.get_filename(args.folder_id, args.host, args.token)
    patch_catalog(filename, args.folder_id, args.host, args.token)