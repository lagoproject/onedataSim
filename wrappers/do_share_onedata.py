#
###############################################################################
# Original Author: R. Pagán Muñoz (https://orcid.org/0000-0002-6802-8179),    #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track),#
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).        #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause) #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)  #
###############################################################################


# additional modules needed
import requests
import json
from yattag import Doc, indent


# External arguments for command line use
# parser = argparse.ArgumentParser(description='Arguments for publishing data')
# parser.add_argument("--token")
# parser.add_argument("--host")
# parser.add_argument("--folder_id" )
# parser.add_argument("--local_folder" )
# parser.add_argument("--handleServiceId" )

# args = parser.parse_args()

# OneData_Token = args.token
# OneData_Host = args.host
# OneData_FolderLevel0_id = args.folder_id
# catalog_path_temp = args.local_folder
# catalog_path_temp = args.handleServiceId

OneData_Token = ""
OneData_Host = ""
OneData_FolderLevel0_id = ""
catalog_path_temp = ""    # LOCAL FOLDER TO SAVE THE XML FILES
OneData_handleServiceId = ""


# own functions

def folder0_content (folder0_id, host, token):
    """

    Parameters
    ----------
    folder0_id : Onedata folder id containing the data to publish.
    host : OneData provider (e.g., ceta-ciemat-02.datahub.egi.eu).
    token : OneData personal access token.

    Returns
    -------
    all_level0: "name" and "id" of the folders contained in the folder defined by "folder0_id"

    """
    OneData_urlchildren = "https://" + host + '/api/v3/oneprovider/data/' + folder0_id + "/children"
    request_param = {'X-Auth-Token': token}
    r_level0 = requests.get(OneData_urlchildren, headers=request_param)    
    all_level0 = json.loads(r_level0.text)
    
    return (all_level0)


def OneData_sharing (filename, file_id, host, token):
    """

    Parameters
    ----------
    filename : OneData provider (e.g., ceta-ciemat-02.datahub.egi.eu).
    file_id : OneData folder id containing the data to publish.
    host : OneData provider (e.g., ceta-ciemat-02.datahub.egi.eu).
    token : OneData personal access token.

    Returns
    -------
    share_level1: share info

    """
    OneData_Header = "application/json"
    OneData_urlcreateShare = "https://" + host + '/api/v3/oneprovider/shares'
    request_param = {'X-Auth-Token': token, "Content-Type": OneData_Header}
    data_file_share = {'name': filename, "fileId": file_id}            
    share_level1 = requests.post(OneData_urlcreateShare, headers=request_param, json=data_file_share)
    print(share_level1)
    print(filename)

    return (share_level1)


def OneData_createhandle (handleservice_id, share_id, local_path, filename, host, token):
    """

    Parameters
    ----------
    handleservice_id : OneData handle service id
    share_id : file shared id
    local_path : local path where the xlm files are stored
    filename : OneData provider (e.g., ceta-ciemat-02.datahub.egi.eu).
    host : OneData provider (e.g., ceta-ciemat-02.datahub.egi.eu).
    token : OneData personal access token.

    Returns
    -------
    handle_level1: handle info

    """
    OneData_urlregisterHandle = "https://datahub.egi.eu/api/v3/onezone/user/handles"
    OneData_Header = "application/json"
    request_param = {'X-Auth-Token': token, "Content-Type": OneData_Header}

    with open(local_path + filename + '.xml', 'r') as file:
        OneData_metadata = file.read()
        
    data_file_handle = { "handleServiceId": handleservice_id, "resourceType": "Share", "resourceId": share_id, "metadata": OneData_metadata}
    handle_level1 = requests.post(OneData_urlregisterHandle, headers=request_param, json=data_file_handle)
    print(handle_level1)
    
    return (OneData_metadata)
    

# MAIN CODE

all_level0 = folder0_content (OneData_FolderLevel0_id, OneData_Host, OneData_Token)


for p in all_level0['children']:
        
        OneData_urljson = "https://" + OneData_Host + '/api/v3/oneprovider/data/' + p['id'] + "/metadata/json"
        r_level1 = requests.get(OneData_urljson, headers={'X-Auth-Token': OneData_Token})
        all_level1 = json.loads(r_level1.text)

        if 'dataset' in all_level1:
            
            doc, tag, text = Doc().tagtext()
            
            with tag('metadata'):
                with tag('dc:title'):
                    text(all_level1['title'])
                with tag('dc:creator'):
                    text(all_level1["creator"]['@id'])
                with tag('dc:date'):
                    text(all_level1["@graph"][1]['prov:endedAtTime'])
                with tag('dc:subject'):
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
                with tag('dc:rights'):
                    text('CC BY 4.0')
                with tag('dc:rights'):
                    text('https://creativecommons.org/licenses/by/4.0/')
                with tag('dc:rights'):
                    text('LAGO rights')
                with tag('dc:rights'):
                    text('https://raw.githubusercontent.com/lagoproject/DMP/1.1/rights/lagoCommonRights.jsonld')
                with tag('dc:description'):
                    text(all_level1["description"])
                with tag('dc:contributor'):
                    text('EGI Datahub')
                with tag('dc:instrument'):
                    text('LAGO Observatory')
                with tag('dc:contact'):
                    text('lago-eosc(at)lagoproject.net')
                with tag('dc:discipline'):
                    text('Astrophysics and Astronomy')
                with tag('dc:publisher'):
                    text('LAGO Collaboration')

            result = indent(
                doc.getvalue(),
                indentation = ' '*4,
                newline = '\n'
            )

            file_object = open(catalog_path_temp + p['name'] + '.xml', 'w')
            file_object.write(result)
            file_object.close()
            print(p['name'] + " XML file created")
            
            # SHARE
            share_level1 = OneData_sharing (p['name'], p['id'], OneData_Host, OneData_Token)
            
            # HANDLE
            OneData_createhandle (OneData_handleServiceId, json.loads(share_level1.text)["shareId"], catalog_path_temp, p['name'], OneData_Host, OneData_Token)
           
          
        else:
            print(p['name'] + " Calculation not completed")
