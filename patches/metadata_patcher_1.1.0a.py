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
# 4- "prov:wasAssociatedWith": {"@id": "HANDLETOCDMI/LAGOsoft/corsika/corsika-75600-lago.tar.gz",
# 4 - SE HACE BIEN EN OTRO PATCHER2, aqui solo hacemos una pequeña ñapa para que pase el corte:
#    j_text = j_text.replace("CORSIKA 75600 for LAGO Collaboration",
#                            "CORSIKA 77402 for LAGO Collaboration")
#    j_text = j_text.replace("HANDLETOCDMI/LAGOsoft/corsika/corsika-75600-lago.tar.gz",
#                            "https://api.github.com/repos/lagoproject/lago-corsika")

# POR TANTO HAY QUE BUSCAR LOS QUE ESTEN CON "https://api.github.com/repos/lagoproject/lago-corsika" VACIO


import argparse
import requests
import json

import mdUtils
import do_share_onedata as mdaux

from fileinput import filename


def patch(only_test, folder_name, folder_id, host, token):
    
    
    # DataSets
    all_level0 = folder0_content(folder_id, host, token)
    # REMOVE .metadata!!!
    for p in all_level0['children']:
        
        # get current metadata
        old_json = mdaux.get_json_metadata(p['id'], host, token)
        
        # 4- "prov:wasAssociatedWith": {"@id": "HANDLETOCDMI/LAGOsoft/corsika/corsika-75600-lago.tar.gz",
        #                                      "name": "CORSIKA 75600 for LAGO Collaboration",
        # todos los que están en LAGOsim son 77400...., pero depende del commit de onedataSim para ver cual se usa
        #
        prov_wasAssociatedWith = old_json["@graph"][2]["prov:wasAssociatedWith"]
        runtimePlatform = prov_wasAssociatedWith["lago:runtimePlatform"]
        
        new_prov_wasAssociatedWith = prov_wasAssociatedWith     
        if prov_wasAssociatedWith["@id"] == "https://api.github.com/repos/lagoproject/lago-corsika":
            ods_commit = runtimePlatform[ "@id"].split("commits/")[1]
            # los de la rama dev, todos usan el commit "ae38b63419f6882ca1d070b34e3f6e46a721ffe9"
            dev_list=['23123','37437941'....]
            
            if ods_commit in dev_list:
                new_prov_wasAssociatedWith = {
                    "sdo:codeRepository": "https://github.com/lagoproject/lago-corsika/tree/ae38b63419f6882ca1d070b34e3f6e46a721ffe9",
                    "name": "lago-corsika-77402",
                    "@id": "https://api.github.com/repos/lagoproject/lago-corsika/git/commits/ae38b63419f6882ca1d070b34e3f6e46a721ffe9"
                }
            # else or switch....

            
        
        # estos ya no cambian
        new_prov_wasAssociatedWith["lago:runtimePlatform"] = runtimePlatform
        new_prov_wasAssociatedWith["@type"] = "lago:Software"


        id_json = {'@id': "/" + folder_name + "/" + p['name'] + "#activity",
                   'prov:wasAssociatedWith': new_prov_wasAssociatedWith
                   }
        
        print('\n\n')
        print(folder_name)
        print('\n')
        if only_test:
            print(id_json)
        else:
            new_json = updating_id_terms_in_json_metadata(id_json, p['id'], host, token)
            print(new_json)
            create_file_in_hidden_metadata_folder(json.dumps(new_json), p['name'] + '.jsonld', folder_id, host, token)
    


# ###############
# MAIN CODE
# ###############

def main():
    
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
    
    #dos niveles de recursividad, preparado para cambiar desde el Space, los metadatos del catalogo y sus datasets
    if args.recursive is True:
        all_level0 = mdaux.folder0_content(args.folder_id, args.host, args.token)
        for p in all_level0['children']:
            if p['name'] != ".metadata":
                patch(args.only_test, p['name'], p['id'], args.host, args.token)
                all_level1 = mdaux.folder0_content(p['id'], args.host, args.token)
                for q in all_level1['children']:
                    if q['name'] != ".metadata":
                        patch(args.only_test, q['name'], q['id'], args.host, args.token)
    else:
        if args.folder_id:
            filename = mdaux.get_filename(args.folder_id, args.host, args.token)
        patch(args.only_test, filename, args.folder_id, args.host, args.token)

    
if __name__ == '__main__':
    sys.exit(main())

    