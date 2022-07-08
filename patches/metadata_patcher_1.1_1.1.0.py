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
#        "https://raw.githubusercontent.com/lagoproject/DMP/1.1/defs/sitesLago.jsonld"
# 3- y codigos anadir /LAGOsim  -> PERO SI AÑADO LAGOsim no va a funcionar ni la mitad de los wrappers..., es un cambio mayor!!!
# 4- "prov:wasAssociatedWith": {"@id": "HANDLETOCDMI/LAGOsoft/corsika/corsika-75600-lago.tar.gz", -> SE HACE una ñapa y se
#     SE CONTINUA EN OTRO PATCHER2
# 5- En JSON catalogue:  "_landing_page": "https://datahub.egi.eu/dummy_hash",  -> NO existe landing page en Catalog DCAT-AP2
# 6- OJO "Catalogue" y "catalogue" son los correctos en DCAT-AP2, comprobado en el GitHub.... ->   "@type": "Catalog", está mal
# 7- OJO lago:ulimit y lago:llimit son uLimit y lLimit
# 8 - Ojo se ha cambiado los codigos: pozn -> psnc ; juli-> jsc
# 9 - lagocollaboration.jsonld -> lagoCollaboration.jsonld
# 10 -  "@id:"-> "@id"
# 11 adding Main Release (major.minor): filename.jsonld -> filename.1.1.jsonld
# 12 Adding GitHub Tag with patch (major.minor.patch): "/DMP/1.1" -> "/DMP/1.1.0"


import argparse
import json
import sys

import do_share_onedata as mdaux


def patch(only_test, folder_name, folder_id, folder_where_md_hidden, host, token):

    # get current metadata
    old_json = mdaux.get_json_metadata(folder_id, host, token)

    j_text = json.dumps(old_json)

    # si está parcheado no vuelve a hacerlo
    if j_text.count('/DMP/1.1.0/') > 0:
        print('Already patched, skipping file')
        return False

    # 1- SE QUEDA COMO ESTA: borro y creo un tag 1.1 nuevo

    # 2- https://github.com/lagoproject/DMP/blob/1.1/defs/sitesLago.jsonld->
    #    https://raw.githubusercontent.com/lagoproject/DMP/1.1/defs/sitesLago.jsonld
    j_text = j_text.replace("https://github.com/lagoproject/DMP/blob/1.1/defs/sitesLago.jsonld",
                            "https://raw.githubusercontent.com/lagoproject/DMP/1.1/defs/sitesLago.jsonld")

    # 3-  SE QUEDA COMO ESTA

    # 4 - SE HACE BIEN EN OTRO PATCHER2, aqui solo hacemos una pequeña ñapa para que pase el corte:
    j_text = j_text.replace("CORSIKA 75600 for LAGO Collaboration",
                            "CORSIKA 77402 for LAGO Collaboration")
    j_text = j_text.replace("HANDLETOCDMI/LAGOsoft/corsika/corsika-75600-lago.tar.gz",
                            "https://api.github.com/repos/lagoproject/lago-corsika")

    # 5- En JSON catalogue:  "'_landing_page': 'https://datahub.egi.eu/dummy_hash',"  -> NO existe landing page en Catalogue DCAT-AP2
    j_text = j_text.replace("'_landing_page': 'https://datahub.egi.eu/dummy_hash',", "")

    # 6- OJO "Catalogue" y "catalogue" son los correctos en DCAT-AP2, comprobado en el GitHub.... ->   "@type": "Catalog", está mal
    j_text = j_text.replace("'@type': 'Catalog'", "'@type': 'Catalogue'")

    # 7- OJO lago:ulimit y lago:llimit son uLimit y lLimit
    j_text = j_text.replace("lago:ulimit", "lago:uLimit")
    j_text = j_text.replace("lago:llimit", "lago:lLimit")

    # 8 - Ojo se ha cambiado los codigos: pozn -> psnc ; juli-> jsc
    j_text = j_text.replace("jsonld#pozn", "jsonld#pnsc")  # OJO FALTA CAMBIAR SUS NOMBRES DE FICHERO
    j_text = j_text.replace("jsonld#juli", "jsonld#jsc")  # OJO FALTA CAMBIAR SUS NOMBRES DE FICHERO

    # 9 - lagocollaboration.jsonld -> lagoCollaboration.jsonld
    j_text = j_text.replace("lagocollaboration.jsonld", "lagoCollaboration.jsonld")

    # 10  "@id:"-> "@id"
    j_text = j_text.replace("@id:", "@id")

    # 11 adding Main Release (major.minor)
    j_text = j_text.replace("sitesLago.jsonld",
                            "sitesLago.1.1.jsonld")

    j_text = j_text.replace("lagoSchema.jsonld",
                            "lagoSchema.1.1.jsonld")

    j_text = j_text.replace("lagoCommonRights.jsonld",
                            "lagoCommonRights.1.1.jsonld")

    j_text = j_text.replace("lagoCollaboration.jsonld",
                            "lagoCollaboration.1.1.jsonld")

    # 12 Adding GitHub Tag with patch (major.minor.patch)

    j_text = j_text.replace("/DMP/1.1/",
                            "/DMP/1.1.0/")

    print('\n\n')
    print(folder_name)
    print('\n')

    new_json = json.loads(j_text)
    if not only_test:
        # careful!!! modifiying metadata
        mdaux.put_json_metadata(new_json, folder_id, host, token)
        mdaux.create_file_in_hidden_metadata_folder(json.dumps(new_json), folder_name + '.jsonld', folder_where_md_hidden, host, token)
    print(new_json)

    # si ha cambiado cosas
    return True

# ###############
# MAIN CODE
# ###############


def main():
    # External arguments for command line use
    parser = argparse.ArgumentParser(description='Enricher of metadata')
    parser.add_argument('--token', help='')
    parser.add_argument('--host', help='')  # OneData Provider !!!
    parser.add_argument('--folder_id', help='')  # INCOMPATIBLE CON --myspace_path
    parser.add_argument('--myspace_path', help='Only Catalgues or paths that contain sub-catalogues')  # INCOMPATIBLE CON --folder_id
    parser.add_argument('--recursive', action='store_true', default=None,
                        help="Enable finding sub-catalogues and sharing the ones that weren\'t shared). Careful: it skips partially-patched Catalogues. Without this option, you can force the patching.")
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
            # solo se puede forzar el parcheo individualmente
            patched = patch(args.only_test, p['name'], p['id'], p['id'], args.host, args.token)
            if not patched:
                print('Already patched, skipping Catalogue.')
                continue
            all_level1 = mdaux.folder0_content(p['id'], args.host, args.token)
            for q in all_level1['children']:
                if q['name'] != ".metadata":
                    patch(args.only_test, q['name'], q['id'], p['id'], args.host, args.token)

    else:
        filename = mdaux.get_filename(args.folder_id, args.host, args.token)
        patch(args.only_test, filename, args.folder_id, args.folder_id, args.host, args.token)
        all_level1 = mdaux.folder0_content(args.folder_id, args.host, args.token)
        for q in all_level1['children']:
            if q['name'] != ".metadata":
                patch(args.only_test, q['name'], q['id'], args.folder_id, args.host, args.token)


if __name__ == '__main__':
    sys.exit(main())
