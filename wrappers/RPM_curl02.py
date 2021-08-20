#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 07:51:22 2021

@author: rpm
"""

import requests
import json
import xml.etree.ElementTree as ET

def _write_file(filepath, txt):    
    with open(filepath, 'w+', encoding="utf-8") as file1:
        file1.write(txt)



OneData_Token = "MDAxY2xvY2F00aW9uIGRhdGFodWIuZWdpLmV1CjAwMzZpZGVudGlmaWVyIDJhYzMwMDNkODkwOTQ4NDFiMTExODIyOGE4OGNjMjk4Y2g3NTc2CjAwMWFjaWQgdGltZSA8IDE2MzgyNjY1NjYKMDAyZnNpZ25hdHVyZSAUlaITPwFIWROJF1D3TUA7VXFM2iDo9JBRO01C5Y6hcoAo"
OneData_Host = "ceta-ciemat-02.datahub.egi.eu"
OneData_FolderLevel0_id = "000000000052614367756964236637333730343236313536636638353937383637323234373463323137633337636863356338236462346433363738373132633065656137313137616538316434646139313664636866663063"
OneData_urlchildren = "https://" + OneData_Host + '/api/v3/oneprovider/data/' + OneData_FolderLevel0_id + "/children"

request_param = {'X-Auth-Token': OneData_Token}
r_level0 = requests.get(OneData_urlchildren, headers=request_param)

all_level0 = json.loads(r_level0.text)

# FOLDER TO SAVE THE XML FILES
catalog_path_temp = "Test/"

for p in all_level0['children']:
        
        OneData_urljson = "https://" + OneData_Host + '/api/v3/oneprovider/data/' + p['id'] + "/metadata/json"
        r_level1 = requests.get(OneData_urljson, headers=request_param)
        all_level1 = json.loads(r_level1.text)

        if 'dataset' in all_level1:
            # Writing xml file  
            xmlns_oaci_dc = "http://www.openarchives.org/OAI/2.0/oai_dc/"
            xmlns_dc = "http://purl.org/dc/elements/1.1/"
            xmlns_xsi = "http://www.w3.org/2001/XMLSchema-instance"
            xsi_schemaLocation = "http://www.openarchives.org/OAI/2.0/oai_dc/ http://www.openarchives.org/OAI/2.0/oai_dc.xsd"
      
            tree = ET.ElementTree("tree")
            
            metadata = ET.Element("metadata")
            oai_dc = ET.SubElement(metadata, "oai_dc:dc", {'xmlns:oai_dc':xmlns_oaci_dc, 'xmlns:dc':xmlns_dc, 'xmlns:xsi':xmlns_xsi, 'xsi:schemaLocation':xsi_schemaLocation,})
            node1 = ET.SubElement(oai_dc, "dc:title")
            node1.text = all_level1['title']
            node2 = ET.SubElement(oai_dc, "dc:creator")
            node2.text = all_level1["creator"]['@id']
            node3 = ET.SubElement(oai_dc, "dc:date")
            node3.text = all_level1["@graph"][1]["prov:startedAtTime"]
            node4 = ET.SubElement(oai_dc, "dc:publisher")
            node4.text = all_level1["publisher"]["@type"]
            node5 = ET.SubElement(oai_dc, "dc:rights")
            node5.text = all_level1["license"]
          
            tree._setroot(metadata)
            tree.write(catalog_path_temp + p['name'] + '.xml', encoding = "UTF-8", xml_declaration = True)  
            print(p['name'] + " XML file created")
            
            # CREATE SHARE OF FINISHED CALCULATIONS (TO CONTINUE FROM RPM_createShare)
            # ...
          
        else:
            print(p['name'] + " Calculation not completed")

