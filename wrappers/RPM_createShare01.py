#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

OneData_Token = ""
OneData_Header = "application/json"
OneData_Host = "ceta-ciemat-02.datahub.egi.eu"
OneData_fileName = "S0_and_10_114.0_77402_QGSII_flat_defaults"
OneData_fileID = "00000000005281E067756964233730343132623535353365653631366231636266373163343162633936626462636863393266236462346433363738373132633065656137313137616538316434646139313664636866663063"
OneData_urlcreateShare = "https://" + OneData_Host + '/api/v3/oneprovider/shares'

request_param = {'X-Auth-Token': OneData_Token, "Content-Type": OneData_Header}
data_file = {'name': OneData_fileName, "fileId": OneData_fileID}

# SHARE
share_level1 = requests.post(OneData_urlcreateShare, headers=request_param, json=data_file)

print(share_level1)

#%%

OneData_urlregisterHandle = "https://datahub.egi.eu/api/v3/onezone/user/handles"
OneData_shareID = json.loads(share_level1.text)["shareId"]
OneData_metadata = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<metadata xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\">\n     <oai_dc:dc>\n      <dc:title>S0_and_10_114.0_77402_QGSII_flat_defaults</dc:title>\n      <dc:creator>RPM</dc:creator>\n      <dc:date>2021-09-01</dc:date>\n      <dc:publisher>lago:Organization</dc:publisher>\n      <dc:rights>cc4.0</dc:rights>\n     </oai_dc:dc>\n\n</metadata>\n"
OneData_handleServiceId = "986fe2ab97a6b749fac17eb9e9b38c37chb045"
data_file_handle = { "handleServiceId": OneData_handleServiceId, "resourceType": "Share", "resourceId": OneData_shareID, "metadata": OneData_metadata}

# HANDLE
handle_level1 = requests.post(OneData_urlregisterHandle, headers=request_param, json=data_file_handle)

print(handle_level1)
