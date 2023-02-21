#
###############################################################################
# Original Author: A.J. Rubio-Montero (http://orcid.org/0000-0001-6497-753X), #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track),#
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).        #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause) #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)  #
###############################################################################


import argparse
import requests
import json
import sys

import do_share_onedata as mdaux
import osUtils



# You need Ozone admin privilege oz_shares_list, it do not will work for users
def get_all_shares(token):

    # curl -u admin:password -X GET https://$HOST/api/v3/onezone/shares
    OneData_urlgetShareinfo = 'https://datahub.egi.eu/api/v3/onezone/shares'
    request_param = {'X-Auth-Token': token}
    shareinfo = requests.get(OneData_urlgetShareinfo, headers=request_param)
    return json.loads(shareinfo.text)


# ###############
# MAIN CODE
# ###############


def main():
    # External arguments for command line use
    parser = argparse.ArgumentParser(description='Arguments to testing linking between shares and data')
    parser.add_argument('--token', help='')
    parser.add_argument('--host', help='')  # OneData Provider !!!
    parser.add_argument('--myspace_path', help='Only Primary Catalgues, i.e. LAGOsim, LAGOraw...')



    args = parser.parse_args()
    
#     shares = get_all_shares(args.token)
#     print (shares)
#     dict_share_file_ids = {}
#     
#     for share_id in shares['shares']:
#         share_info = mdaux.get_share_info(share_id, args.token)
#         dict_aux = {}
#         dict_aux['name'] =  share_info['name']
#         dict_aux['rootFileId_onezone'] = share_info['rootFileId']
#         dict_aux['rootFileId_oneprovider'] = mdaux.get_folder_id(args.myspace_path+'/'+share_info['name'], args.host, args.token)
#         
#         dict_share_file_ids[share_id] =  dict_aux
        
        
    dict_share_file_ids = {}
    dict_share_file_ids_extended = {}
    dict_file_id_tests = {}    
    folder_id = mdaux.get_folder_id(args.myspace_path, args.host, args.token)    
    all_level0 = mdaux.folder0_content(folder_id, args.host, args.token)
    
    for p in all_level0['children']:
        print(p['name'])
        fileid = p['id']
        json_aux = mdaux.get_latest_file_in_hidden_metadata_folder(p['name'], fileid, args.host, args.token)
        dict_file_id_tests[fileid] = {}
        dict_file_id_tests[fileid]['name'] = p['name'] # official name in oneprovider
        if json_aux == None:
            print("There is not metadata backup!!!")
        else:
            dict_file_id_tests[fileid]['title'] = json_aux['title'] # title in last json backup
            if p['name'] != json_aux['title']:
                print("Careful!!!, title and name is not identical")
            
            if 'homepage' in json_aux.keys():
                dict_file_id_tests[fileid]['homepage'] = json_aux['homepage'] # handle and share in last json backup
        
                if len(json_aux['homepage']) != 2: # something wrong?
                    print("Something wrong with publishing!!!!")
                elif len(json_aux['homepage']) == 2:  # published
                    print(("Published!!!!"))
                    shareid = json_aux['homepage'][1][len('"https://datahub.egi.eu/share/')-1:]
                    print (shareid)
                    dict_share_file_ids[shareid] = fileid
                    
                    # test if shareid is being used and the info matches
                    shared_info = mdaux.get_share_info(shareid, args.token)
                    dict_share_file_ids_extended[shareid] = {}
                    #dict_share_file_ids_extended[shareid]['spaceId'] = {} 
                    #dict_share_file_ids_extended[shareid]['spaceId']['current'] =  shared_info['spaceId']
                    #dict_share_file_ids_extended[shareid]['spaceId']['actual'] = XXXX! 
                    #dict_share_file_ids_extended[shareid]['spaceId']['match'] = (shared_info['spaceId'] == XXX!)                 
                    dict_share_file_ids_extended[shareid]['rootFileId'] = {} 
                    dict_share_file_ids_extended[shareid]['rootFileId']['current'] =  shared_info['rootFileId']
                    dict_share_file_ids_extended[shareid]['rootFileId']['actual'] =  fileid
                    dict_share_file_ids_extended[shareid]['rootFileId']['match'] = (shared_info['rootFileId'] == fileid)
                    dict_share_file_ids_extended[shareid]['name'] = {}
                    dict_share_file_ids_extended[shareid]['name']['current'] =  shared_info['name'] 
                    dict_share_file_ids_extended[shareid]['name']['actual'] = p['name']
                    dict_share_file_ids_extended[shareid]['name']['backed-up'] = json_aux['title']
                    dict_share_file_ids_extended[shareid]['name']['match'] = (shared_info['name'] == p['name'] == json_aux['title'] )
                    # test handle 
                    handle_info = mdaux.get_handle_info(shared_info['handleId'], args.token)
                    dict_share_file_ids_extended[shareid]['publicHandle'] = {}
                    dict_share_file_ids_extended[shareid]['publicHandle']['current'] =  handle_info['publicHandle']
                    dict_share_file_ids_extended[shareid]['publicHandle']['backed-up'] = json_aux['homepage'][0]
                    dict_share_file_ids_extended[shareid]['publicHandle']['match'] = (handle_info['publicHandle'] == json_aux['homepage'][0])
                    
                    print(dict_share_file_ids_extended[shareid])

            else:
                print("Not published")
        
        
    #print (dict_file_id_tests)
    osUtils._write_file('.dict_file_id_tests.json', json.dumps(dict_file_id_tests))
    #print (dict_share_file_ids)
    osUtils._write_file('.dict_share_file_ids.json', json.dumps(dict_share_file_ids))
    #print (dict_share_file_ids)
    osUtils._write_file('.dict_share_file_ids_extended.json', json.dumps(dict_share_file_ids_extended))
    

if __name__ == '__main__':
    sys.exit(main())
