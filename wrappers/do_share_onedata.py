#!/usr/bin/env python3
#
###############################################################################
# Original Author: R. Pagán Muñoz (https://orcid.org/0000-0002-6802-8179),    #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track),#
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).        #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause) #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)  #
###############################################################################


# additional modules needed
import argparse
import requests
import json
import sys
from yattag import Doc, indent

import mdUtils


def create_dublincore_xml_file(all_level1):
    """
    -------
    Modules
    -------
    Doc, indent
    -----------
    Description
    -----------
    Creates a "filename.xml" on "local_path" in  DublinCore format
    with the elements within "all_level1", the JSON of a Catalog.
    ----------
    Parameters
    ----------
    all_level1 : dict that contains the JSON of a Catalog (after json.loads)
    -------
    Returns
    -------
    ....????
    """

    # get publisher
    r_json = requests.get(all_level1["publisher"]['@id'])
    j_publisher = json.loads(r_json.text)
    # get current rights
    r_json = requests.get(all_level1["rights"])
    j_rights = json.loads(r_json.text)

    # ajrm: creating a handle at OneData needs a RDF file:
    # https://onedata.org/#/home/api/stable/onezone?anchor=operation/handle_service_register_handle
    # or simply adding parameters to metadata tag:
    # <metadata xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:dc="http://purl.org/dc/elements/1.1/">
    metadata_tag_content = 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:dc="http://purl.org/dc/elements/1.1/"'

    doc, tag, text = Doc().tagtext()

    # ajrm: it should appear dc terms in
    # http://www.openarchives.org/OAI/2.0/oai_dc/
    # http://www.openarchives.org/OAI/2.0/oai_dc.xsd
    # thats are the only supported by OneData

    with tag('metadata', metadata_tag_content):
        with tag('dc:title'):
            text(all_level1['title'])
        with tag('dc:creator'):
            text(get_orcid_name(all_level1["creator"]['@id']))
        with tag('dc:creator'):
            text(all_level1["creator"]['@id'])
        with tag('dc:subject'):  # OJO no existe "discipline" en DC, ni en DataCite, es solo esquema B2FIND
            text('4.2.5#Physics#Astrophysics and Astronomy')  # subject seria el aqui el equivalente a Discipline en B2FIND
        with tag('dc:subject'):
            text('https://raw.githubusercontent.com/EUDAT-B2FIND/md-ingestion/master/etc/b2find_disciplines.json#4.2.5#Physics#Astrophysics%20and%20Astronomy')
        with tag('dc:subject'):  # a partir de aqui son los equivalentes a keywords en B2FIND
            text('High energy astrophysics')
        with tag('dc:subject'):
            text('http://astrothesaurus.org/uat/739')
        with tag('dc:subject'):
            text('Particle astrophysics')
        with tag('dc:subject'):
            text('http://astrothesaurus.org/uat/96')
        with tag('dc:subject'):
            text('Astronomical simulations')
        with tag('dc:subject'):
            text('http://astrothesaurus.org/uat/1857')
        with tag('dc:description'):
            text(all_level1["description"])
        with tag('dc:publisher'):
            text('EGI DataHub')  # OJO SERIA MEJOR CAPTURARLO DE METADATOS
        with tag('dc:publisher'):
            text('https://datahub.egi.eu')
        with tag('dc:publisher'):
            text(j_publisher["name"])  # LAGO Collaboration
        with tag('dc:publisher'):
            text(j_publisher["url"])  # equivalent to landingPage
        with tag('dc:publisher'):
            text(j_publisher["sameAs"][0])  # equivalent URLS
        with tag('dc:contributor'):
            text(j_publisher["name"])  # LAGO Collaboration es tambien siempre contributor
        with tag('dc:contributor'):
            text(j_publisher["url"])  # equivalent to landingPage
        with tag('dc:contributor'):
            text(j_publisher["sameAs"][0])  # equivalent URLS, OJO SOLO PONGO LA PRIMERA Y ESPERO QUE APUNTE AL DMP
        with tag('dc:contributor'):
            text('EOSC-Synergy')  # OJO SERIA MEJOR CAPTURARLO DE METADATOS
        with tag('dc:contributor'):
            text('European Open Science Cloud-Expanding Capacities by building Capabilities (EOSC-SYNERGY) project')
        with tag('dc:contributor'):
            text('https://www.eosc-synergy.eu/')
        with tag('dc:contributor'):
            text('EOSC-synergy receives funding from the European Union\'s Horizon 2020 research and innovation programme under grant agreement No 857647')
        with tag('dc:contributor'):
            text('https://cordis.europa.eu/project/id/857647')
        # aqui podrian entrar otros "contributor": EGI DataHub, CETA-CIEMAT, CIEMAT. recursos cloud....
        with tag('dc:date'):
            text(all_level1["@graph"][-1]['prov:endedAtTime'])  # OJO graph[-1], last element
        with tag('dc:type'):
            text('Collection')
        with tag('dc:format'):
            text('octet-stream')
        # identifier (handle and share links) posteriorly added by OneData
        # <element ref="dc:identifier"/>
        # OJO source, interesante para los S1 y S2
        # "A related resource from which the described resource is derived."
        # <element ref="dc:source"/>
        with tag('dc:language'):
            text('en')
        # OJO relation
        # <element ref="dc:relation"/>
        # OJO coverage... (spatial, temporal, instrument?...)
        # <element ref="dc:coverage"/>
        #   ojo tambien que meto qualifiers...
        with tag('dc:coverage', 'xsi:type=”dcterms:Spatial”'):
            # east=148.26218; north=-36.45746; elevation=2228; name=Mt. Kosciusko (the highest point in Australia);
            text('east=' + all_level1["spatial"]["geometry"]['geo:latitude'] + '; ' +
                 'north=' + all_level1["spatial"]["geometry"]['geo:longitude'] + '; ' +
                 'elevation=' + all_level1["spatial"]["geometry"]['geo:altitude'] + ';')  # + # OJO aqui el enricher ya la ha cambiado por a la simulada (obsLev)
            # 'name=' + all_level1["spatial"][????] + ';')  # de momento no pongo el nombre, puesto que no esta estandarizado DCAT-AP2
        with tag('dc:coverage', 'xsi:type=”dcterms:Period”'):
            # name=The 1960s; start=1960-01-01; end=1969-12-31;
            text('start=' + all_level1["temporalCoverage"]["startDate"] + ';' + 'end=' + all_level1["temporalCoverage"]["endDate"] + ';')
        with tag('dc:rights'):  # DataCite (B2FIND) lo necesita en Rights, porque no tiene license
            text('CC BY-NC-SA 4.0')  # MEJOR CAPTURARLA DE "license",
        with tag('dc:rights'):
            text(all_level1["license"])
        with tag('dc:rights'):
            text(j_rights["title"])  # LAGO Common Rights
        with tag('dc:rights'):
            text(j_rights["landingPage"])
        with tag('dc:rights'):
            text(j_rights["relatedResource"])
        with tag('dc:rights'):
            text('Access Rights')
        with tag('dc:rights'):
            text(all_level1["accessRigths"])
        # with tag('dc:instrument'): # OJO no existe dc:instrument, ni en DataCite, es solo esquema B2FIND
        #    text('Water Cherenkov Detector')  # TIENE QUE SER HARDCODED en B2FIND
        # with tag(dc:instrument')
        #    text('WCD')
        # with tag(dc:instrument')
        #    text('https://lagoproject.net/wcd.html') # creo que no es necesario el link para la busqueda
        # with tag('dc:contact'):  # OJO no existe dc:contact, ni en DataCite, es solo esquema B2FIND
        #    text('lago-eosc(at)lagoproject.net')

    return indent(doc.getvalue(), indentation=' '*4, newline='\n').replace('”', '"')


def get_orcid_name(orcid_link):

    # the "name" usually is not set, i have to construct it with:
    #      "givenName" and "familyName"

    request_param = {'Accept': 'application/ld+json'}
    r = requests.get(orcid_link, headers=request_param)
    r_json = json.loads(r.text)

    return r_json['givenName'] + " " + r_json['familyName']


def read_only_permissions(folder_id, host, token, all_level1):

    # pueden haber varios #activity, es un bug que debería estar corregido
    # aquí cogería el primero que vea
    # activity_json = mdUtils.get_item_by_id(all_level1, "/" + folder_name + "#activity")

    mode = '0555'
    # default is to allow anonymous users only reading the metadata = 0554
    # mode = '0554'
    #  if anonym_access:
    #     mode = '0555'

    OneData_urlfolder = "https://" + host + '/api/v3/oneprovider/data/' + folder_id
    request_param = {'X-Auth-Token': token, 'Content-Type': 'application/json'}
    request_json = {'mode': mode}
    r_id = requests.put(OneData_urlfolder, headers=request_param, json=request_json)
    print(r_id)


def create_file_in_hidden_metadata_folder(content, filename, folder_id, host, token):

    # get hidden "/.metadata/" ID
    all_level1 = folder0_content(folder_id, host, token)

    hiden_metadata_folder_id = None
    for p in all_level1['children']:
        if p['name'] == ".metadata":
            hiden_metadata_folder_id = p['id']
            break
    if hiden_metadata_folder_id is None:
        return

    t = mdUtils.xsd_dateTime().replace('-', '').replace(':', '')

    OneData_Header = "application/octet-stream"
    OneData_urlcreatefile = "https://" + host + '/api/v3/oneprovider/data/' + hiden_metadata_folder_id + '/children?name=.' + filename + '.' + t
    request_param = {'X-Auth-Token': token, "Content-Type": OneData_Header}
    u_content = content.encode('utf-8')
    r = requests.post(OneData_urlcreatefile, headers=request_param, data=u_content)

    r_json = json.loads(r.text)
    print(r_json)


def folder0_content(folder0_id, host, token):
    """
    Modules
    -------
    request, json
    ----------
    Parameters
    ----------
    folder0_id : Onedata folder level 0 id containing the data to publish.
    host : OneData provider (e.g., ceta-ciemat-02.datahub.egi.eu).
    token : OneData personal access token.
    -------
    Returns
    -------
    all_level0: "name" and "id" of the folders contained in the folder defined by "folder0_id"
    """

    OneData_urlchildren = "https://" + host + '/api/v3/oneprovider/data/' + folder0_id + "/children"
    request_param = {'X-Auth-Token': token}
    r_level0 = requests.get(OneData_urlchildren, headers=request_param)
    all_level0 = json.loads(r_level0.text)

    return (all_level0)


def get_folder_id(myspace_path, host, token):

    OneData_urlfolder_id = "https://" + host + '/api/v3/oneprovider/lookup-file-id/' + myspace_path
    request_param = {'X-Auth-Token': token}
    r_id = requests.post(OneData_urlfolder_id, headers=request_param)
    print(r_id.text)
    folder_id = json.loads(r_id.text)['fileId']

    return folder_id


def get_filename(folder0_id, host, token):

    OneData_urlfolder_name = "https://" + host + '/api/v3/oneprovider/data/' + folder0_id + '?attribute=name'
    request_param = {'X-Auth-Token': token}
    r_id = requests.get(OneData_urlfolder_name, headers=request_param)
    filename = json.loads(r_id.text)['name']
    return filename


def OneData_sharing(filename, file_id, description, host, token):
    """
    -------
    Modules
    -------
    request
    ----------
    Parameters
    ----------
    filename : Folder name to share and handle.
    file_id : OneData folder id containing the data to publish.
    host : OneData provider (e.g., ceta-ciemat-02.datahub.egi.eu).
    token : OneData personal access token.
    -------
    Returns
    -------
    share_level1: share info
    """

    OneData_Header = "application/json"
    OneData_urlcreateShare = "https://" + host + '/api/v3/oneprovider/shares'
    request_param = {'X-Auth-Token': token, "Content-Type": OneData_Header}
    # OneData Bug/restriction: 'name' max 50 chars for share
    if len(filename) > 50:
        sharename = filename[0:49]
    else:
        sharename = filename
    data_file_share = {'name': sharename, "fileId": file_id, "description": description}
    r_share_level1 = requests.post(OneData_urlcreateShare, headers=request_param, json=data_file_share)

    # only returns shareID
    share_level1 = json.loads(r_share_level1.text)
    print(share_level1)

    return get_share_info(share_level1["shareId"], token)


def OneData_createhandle(handleservice_id, share_id, metadata, host, token):
    """
    -------
    Modules
    -------
    request
    ----------
    Parameters
    ----------
    handleservice_id : OneData handle service id
    share_id : file shared id
    host : OneData provider (e.g., ceta-ciemat-02.datahub.egi.eu).
    token : OneData personal access token.
    -------
    Returns
    -------
    handle_level1: handle info
    """

    # OJO onezone
    OneData_urlregisterHandle = "https://datahub.egi.eu/api/v3/onezone/user/handles"
    OneData_Header = "application/json"
    request_param = {'X-Auth-Token': token, "Content-Type": OneData_Header}

    OneData_metadata = metadata

    data_file_handle = {"handleServiceId": handleservice_id, "resourceType": "Share", "resourceId": share_id, "metadata": OneData_metadata}
    r_handle_level1 = requests.post(OneData_urlregisterHandle, headers=request_param, json=data_file_handle)

    # fails because API miss-implementation
    # handle_level1 = json.loads(r_handle_level1.text)
    print(r_handle_level1)
    # i have to request again the handle info:
    shareinfo = get_share_info(share_id, token)
    print(shareinfo)
    handleinfo = get_handle_info(shareinfo['handleId'], token)
    print(handleinfo)

    return handleinfo


def had_it_published(folder1_id, host, token, remove_unused_shares=False):
    """
    -------
    Modules
    -------
    request, json
    -----------
    Description
    -----------
    This function tests and gets the last publication attributes for a
    folder_id (or file_id), this is, its sharing and handling information).
    Otherwise, if it was not published, it returns a empty list [].
    If the file has been shared several times, the function can delete the ones
    without associated handle PiD.
    ----------
    Parameters
    ----------
    folder1_id : Onedata folder level 1 id (contained in level 0 folder).
    host : OneData provider (e.g., ceta-ciemat-02.datahub.egi.eu).
    token : OneData personal access token.
    remove_unused_shares : if you want to erase unpublished shares (without handle PiD)
    -------
    Returns
    -------
    shareinfo: Get the basic information about the published folder/file
    """

    OneData_urlgetAttrs = "https://" + host + '/api/v3/oneprovider/data/' + folder1_id + "?attribute=shares"
    request_param = {'X-Auth-Token': token}
    shareid_level1 = requests.get(OneData_urlgetAttrs, headers=request_param)
    attrs_level1 = json.loads(shareid_level1.text)
    print(attrs_level1)

    shareinfo = []
    if attrs_level1['shares']:
        for ii in range(len(attrs_level1['shares'])):
            n = len(attrs_level1['shares']) - 1
            shareinfo_level1 = get_share_info(attrs_level1['shares'][n-ii], token)
            # print(shareinfo_level1)
            # OJO BUG, PROBLEMAS para obtener el Share cuando se ha migrado el OneProvider
            if 'handleId' not in shareinfo_level1.keys():
                continue
            if shareinfo_level1['handleId']:
                print('handle exist already, it is already published!!!')
                print(shareinfo_level1['handleId'])
                shareinfo = shareinfo_level1
            else:
                print('handle is missing')
                if remove_unused_shares:
                    OneData_urldeleteShare = "https://" + host + '/api/v3/oneprovider/shares/' + attrs_level1['shares'][n-ii]
                    requests.delete(OneData_urldeleteShare, headers=request_param)
                    print("extra share deleted")
    else:
        print("folder not shared yet")

    return (shareinfo)


def get_share_info(share_id, token):

    # OneData_urlgetShareinfo = "https://" + host + '/api/v3/oneprovider/shares/' + share_id
    OneData_urlgetShareinfo = 'https://datahub.egi.eu/api/v3/onezone/shares/' + share_id
    request_param = {'X-Auth-Token': token}
    shareinfo = requests.get(OneData_urlgetShareinfo, headers=request_param)
    return json.loads(shareinfo.text)


def get_handle_info(handle_id, token):

    # ojo onezone
    OneData_urlgetHandleinfo = 'https://datahub.egi.eu/api/v3/onezone/user/handles/' + handle_id
    request_param = {'X-Auth-Token': token}
    handleinfo = requests.get(OneData_urlgetHandleinfo, headers=request_param)
    return json.loads(handleinfo.text)


def publish_catalog(remove_unused_shares, handleservice_id, filename, folder1_id, host, token):
    """
    -------
    Modules
    -------
    request, json
    -----------
    Description
    -----------
    ....????
    ----------
    Parameters
    ----------
    handleservice_id : OneData handle service id
    folder1_id : Onedata folder level 1 id (contained in level 0 folder).
    filename : Folder name to share and handle.
    host : OneData provider (e.g., ceta-ciemat-02.datahub.egi.eu).
    token : OneData personal access token.
    -------
    Returns
    -------
    ....????
    """

    all_level1 = get_json_metadata(folder1_id, host, token)

    # falta: una funcion que devuelva true o false si pasa o no unos minimos requisitos.
    # con spatial me aseguro que tiene metadatos enriquecidos
    if ('spatial' in all_level1) and ('dataset' in all_level1) and (filename.split('_')[0] == "S0"):

        # is it published?
        if had_it_published(folder1_id, host, token, remove_unused_shares):
            print('It had been published before.')
            # check if the embargo period had been overcomed (1 year)
            read_only_permissions(folder1_id, host, token, all_level1)
        else:
            try:
                share_level1 = OneData_sharing(filename, folder1_id, all_level1["description"], host, token)
                print(share_level1)
                OneData_metadata = create_dublincore_xml_file(all_level1)
                handle_level1 = OneData_createhandle(handleservice_id, share_level1["shareId"], OneData_metadata, host, token)
                print('share and handle just created')
                # it backups the final DublinCore metadata into a hidden .xml in the hidden .metadata dir
                print(handle_level1['metadata'])
                create_file_in_hidden_metadata_folder(handle_level1['metadata'], filename + '.xml', folder1_id, host, token)
                print('XML in ./metadata/ created')
                # it modifies the JSON-LD metadata both online (internal kept by OneData) and hidden in .metadata
                include_hadle_and_share_in_json_and_hidden_metadata(handle_level1['publicHandle'], share_level1['publicUrl'], filename, folder1_id, host, token)
                # if all is correct, data should be read-only forever
                read_only_permissions(folder1_id, host, token, all_level1)
                print('Catalog is now read-only')
            except Exception as inst:
                print("Exception catched: " + str(type(inst)))
                print(inst)
                pass

    else:
        print(filename + " Calculation not completed or metadate not enriched")


def get_json_metadata(onedata_id, host, token):

    OneData_urljson = "https://" + host + '/api/v3/oneprovider/data/' + onedata_id + "/metadata/json"
    r_json = requests.get(OneData_urljson, headers={'X-Auth-Token': token})
    return json.loads(r_json.text)


def put_json_metadata(new_json, onedata_id, host, token):

    OneData_urljson = "https://" + host + '/api/v3/oneprovider/data/' + onedata_id + "/metadata/json"
    request_param = {'X-Auth-Token': token, 'Content-Type': 'application/json'}
    r_id = requests.put(OneData_urljson, headers=request_param, json=new_json)
    print(r_id)


def updating_terms_in_json_metadata(additional_json, onedata_id, host, token):

    old_json = get_json_metadata(onedata_id, host, token)
    new_json = mdUtils.add_json(old_json, additional_json)
    # careful!!! modifiying metadata
    put_json_metadata(new_json, onedata_id, host, token)
    return new_json


def updating_id_terms_in_json_metadata(json_dict_id, onedata_id, host, token):

    old_json = get_json_metadata(onedata_id, host, token)
    new_json = mdUtils.replace_only_json_id_items(old_json, json_dict_id)
    # careful!!! modifiying metadata
    put_json_metadata(new_json, onedata_id, host, token)
    return new_json


def include_hadle_and_share_in_json_and_hidden_metadata(handle_link, share_link, folder_name, folder_id, host, token):

    handle_share_list = [handle_link, share_link]

    # Catalogue
    id_json = {'@id': "/" + folder_name,
               'homepage': handle_share_list
               }
    new_json = updating_id_terms_in_json_metadata(id_json, folder_id, host, token)
    create_file_in_hidden_metadata_folder(json.dumps(new_json), folder_name + '.jsonld', folder_id, host, token)

    # DataSets
    all_level0 = folder0_content(folder_id, host, token)
    # REMOVE .metadata!!!
    for p in all_level0['children']:
        # new_json = updating_terms_in_json_metadata({'landingPage': handle_share_list}, p['id'], host, token)
        id_json = {'@id': "/" + folder_name + "/" + p['name'],
                   'landingPage': handle_share_list
                   }
        updating_id_terms_in_json_metadata(id_json, p['id'], host, token)
        id_json = {'@id': "/" + folder_name + "/" + p['name'] + "#distribution",
                   'accessURL': handle_share_list
                   }
        print(id_json)
        new_json = updating_id_terms_in_json_metadata(id_json, p['id'], host, token)
        # * Distribution accessURL !!!!
        # "distribution": "/S0_and_100_77402_QGSII_volu_defaults/DAT000703-0703-00000000479.lst.bz2#distribution"
        # dist_json_pruned = ?? new_json[???]
        # new_json = updating_terms_in_json_metadata(dist_json_pruned, folder_id, host, token)
        create_file_in_hidden_metadata_folder(json.dumps(new_json), p['name'] + '.jsonld', folder_id, host, token)


# ###############
# MAIN CODE
# ###############


def main():
    # External arguments for command line use
    parser = argparse.ArgumentParser(description='Arguments for publishing data')
    parser.add_argument('--token', help='')
    parser.add_argument('--host', help='')  # OneData Provider !!!
    parser.add_argument('--folder_id', help='')  # INCOMPATIBLE CON --myspace_path
    parser.add_argument('--myspace_path', help='Only Catalgues or paths that contain sub-catalogues')  # INCOMPATIBLE CON --folder_id
    parser.add_argument('--handleservice_id', required=True, help='Alwasy required for creating the handle')
    parser.add_argument('--remove_unused_shares', action='store_true', default=None,
                        help="Remove additional shares if they do not contain a Handle PID)")
    parser.add_argument('--recursive', action='store_true', default=None,
                        help="Enable finding sub-catalogues and sharing the ones that weren\'t shared)")

    args = parser.parse_args()

    if args.myspace_path:
        args.folder_id = get_folder_id(args.myspace_path, args.host, args.token)
        if not args.folder_id:
            exit(-1)

    if args.recursive is True:
        all_level0 = folder0_content(args.folder_id, args.host, args.token)
        for p in all_level0['children']:
            print("Publish Catalogue for " + p['name'] + " id:" + p['id'])
            publish_catalog(args.remove_unused_shares, args.handleservice_id, p['name'], p['id'], args.host, args.token)
    else:
        filename = get_filename(args.folder_id, args.host, args.token)
        publish_catalog(args.remove_unused_shares, args.handleservice_id, filename, args.folder_id, args.host, args.token)


if __name__ == '__main__':
    sys.exit(main())
