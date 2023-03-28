#
###############################################################################
# Original Author: A.J. Rubio-Montero (http://orcid.org/0000-0001-6497-753X), #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track),#
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).        #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause) #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)  #
###############################################################################


import argparse
import json
import sys

import do_share_onedata as mdaux


def patch(force, only_test, folder_name, folder_id, folder_where_md_hidden, host, token):

    print('\n\n')
    print(folder_name)
    print('\n')

    if not force:
        old_json = mdaux.get_json_metadata(folder_id, host, token)
        if old_json != None:
            print(old_json)
            print('NOT OVERWRITE METADATA')
            return False
        
    new_json = mdaux.get_latest_file_in_hidden_metadata_folder(folder_name, folder_where_md_hidden, host, token)
    
    if not only_test and new_json != None:
        # careful!!! modifiying metadata
        mdaux.put_json_metadata(new_json, folder_id, host, token)
        print('METADATA OVERWRITED')
    print(new_json)

    # si ha cambiado cosas
    return True

# ###############
# MAIN CODE
# ###############


def main():
    # External arguments for command line use
    parser = argparse.ArgumentParser(description='Recover JSON metadata from backups')
    parser.add_argument('--token', help='')
    parser.add_argument('--host', help='')  # OneData Provider !!!
    parser.add_argument('--folder_id', help='')  # INCOMPATIBLE CON --myspace_path
    parser.add_argument('--myspace_path', help='Only Catalgues or paths that contain sub-catalogues')  # INCOMPATIBLE CON --folder_id
    parser.add_argument('--recursive', action='store_true', default=False,
                        help="Enable finding sub-catalogues and patching the ones that weren\'t shared). Careful: it skips partially-patched Catalogues.")
    parser.add_argument('--force', action='store_true', default=False,
                        help="Careful: it force overwrite the JSON metadata.")    
    parser.add_argument('--only_test', action='store_true', default=False,
                        help="If it is set, only test the changes and outputs)")

    args = parser.parse_args()

    if args.myspace_path:
        args.folder_id = mdaux.get_folder_id(args.myspace_path, args.host, args.token)
        if not args.folder_id:
            exit(-1)

    # dos niveles de recursividad, preparado para cambiar desde el Space, los metadatos del catalogo y sus datasets
    if args.recursive is True:
        all_level0 = mdaux.folder0_content(args.folder_id, args.host, args.token)
        print("Testing patchin in " + str(len(all_level0['children'])) + " Catalogues.")
        for p in all_level0['children']:
            # OJO dejo de parchear si el directorio del catálogo ya está parcheado.
            # solo se puede forzar el parcheo con "force"
            patched = patch(args.force, args.only_test, p['name'], p['id'], p['id'], args.host, args.token)
            if not patched:
                print('Already patched, skipping Catalogue.')
                continue
            all_level1 = mdaux.folder0_content(p['id'], args.host, args.token)
            for q in all_level1['children']:
                if q['name'] != ".metadata":
                    patch(args.force, args.only_test, q['name'], q['id'], p['id'], args.host, args.token)

    else:
        filename = mdaux.get_filename(args.folder_id, args.host, args.token)
        patch(args.force, args.only_test, filename, args.folder_id, args.folder_id, args.host, args.token)
        all_level1 = mdaux.folder0_content(args.folder_id, args.host, args.token)
        for q in all_level1['children']:
            if q['name'] != ".metadata":
                patch(args.force, args.only_test, q['name'], q['id'], args.folder_id, args.host, args.token)


if __name__ == '__main__':
    sys.exit(main())
