#
###############################################################################
# Original Author: A.J. Rubio-Montero (http://orcid.org/0000-0001-6497-753X), #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track),#
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).        #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause) #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)  #
###############################################################################

# additional modules needed
import argparse
import requests
import json

import mdUtils
import do_share_onedata as mdaux

from fileinput import filename


def find_site_metadata(site):

    # get updated sitesLago.jsonld
    # from https://raw.githubusercontent.com/lagoproject/DMP/dev/defs/sitesLago.jsonld
    
    return get_item_by_id(j, site)

def enrich_catalog(folder_name, folder_id, host, token):
    
    # get current metadata
    old_json = get_json_metadata(folder_id, host, token)
    
    artiparams =  get_item_by_id(j, folder_name + "#artiParams")
    
# # example of artiparams
#     {
#       "lago:obsLev": 114,   # OJO OJO EN CM
#       "lago:highEnergyIntModel": "QGSII",
#       "lago:fluxTime": "P10S",
#       "lago:flatArray": true,
#       "lago:detectorSite": "https://github.com/lagoproject/DMP/blob/1.1/defs/sitesLago.jsonld#and",
#       "lago:defaults": true,
#       "@type": "lago:ArtiParams",
#       "@id": "/S0_and_10_114.0_77402_QGSII_flat_defaults#artiParams"
#     },
   
    # obtain site from "lago:detectorSite":,
    # or from folder_name
    
    site = folder_name.split('_')[1]
    print(site)  


# # example of site
#      {
#       "@id": "and",
#       "@type": "lago:DetectorSite",
#       "name": "Andes, Argentina",
#       "lago:belongsLago": false,
#       "qualifiedAttribution": {
#         "@type": "lago:Organisation",
#         "name": ""
#       },
#       "geometry": {
#         "@id": "and#geometry",
#         "@type": "geo:Point",
#         "geo:latitude": "-30.19",
#         "geo:longitude": "-69.82",
#         "geo:altitude": "4200" # OJO OJO EN METROS
#       },
#       "lago:obsLev": {
#         "@default": "420000"
#       },
#       "lago:atmcrd": {
#         "@type": {
#           "@default": "lago:Atmod"
#         },
#         "lago:modatm": {
#           "@default": "E2"
#         }
#       },
#       "lago:magnet": {
#         "@default": {
#           "lago:bDate": "2021-04-08",
#           "conformsTo": {
#             "@id": "https://doi.org/10.1186/s40623-020-01288-x",
#             "@type": [
#               "dct:Standard",
#               "DataSet"
#             ],
#             "title": "IGRF",
#             "description": "International Geomagnetic Reference Field",
#             "landingpage": "https://www.ngdc.noaa.gov/IAGA/vmod/igrf.html",
#             "version": "13",
#             "dataservice": {
#               "title": "Geomagnetic Model Web Service",
#               "endpointURL": "http://geomag.bgs.ac.uk/web_service/GMModels/"
#             },
#             "temporalCoverage": {
#               "startDate": "2020-01-01",
#               "endDate": "2024-12-31"
#             },
#             "temporalResolution": "P1D"
#           },
#           "lago:bx": "19.658",
#           "lago:bz": "-11.951",
#           "lago:bi": "23.011"
#         }
#       }
#     },
    
    # get fixed metadata for the site 
    
    j_site = find_site_metadata(site)

    # new spatial 
    # change default altitude to the one simulated "lago:obsLev" OJO: CM->Meters
    new_spatial = {'geometry': j_site['geometry']}
    new_spatial['geometry']['geo:altitude'] = artiparams["lago:obsLev"]/100
    
    #new  temporalCoverage
    # "endDate": "2021-05-19T15:01:26" -> bDate + "lago:fluxTime"
    bDate = j_site["lago:magnet"]["@default"]['lago:bDate']
    new_temporalCoverage = {
            "startDate": bDate,
            "endDate": xsd_dateTime_add_elapsed(bDate,artiparams["lago:fluxTime"]) 
        }

    #
    # make new description ....
    #
    new_desc = ""
    
    # what simulation S0, S1, S2
    s = folder_name.split('_')[0]
    sim_type = {'S0' : 'plain simulation',
                'S1' : 'analyzed simulation',
                'S2' : 'detector response simulation'}

    sim_desc = {'S0' : 'CORSIKA outputs, which are described in the official documentation.',
                'S1' : 'ARTI analysis and outputs of previous S0 Datasets, containing the expected flux of secondary particles at the ground).',
                'S2' : 'outputs of ARTI detector simulation module, containing a complete, detailed and adjustable Geant4 model of the LAGO detectors.The main output is the expected signals in the detector, allowing site characterization and comparison with L2 and L3 data sets at each site).'}

    new_desc = "This Catalogue contains a complete LAGO (" + s + ") " + sim_type[s]
    #OJO, SERIA MEJOR TENER UN 'label' en vez de un '@id'
    if j_site["lago:belongsLago"]:
        new_desc = + " for the LAGO '" + j_site['@id'] + "' site"
        if  j_site["qualifiedAttribution"]["name"] != "":
            new_desc = + " managed by the "+ j_site["qualifiedAttribution"]["name"] + " institution; "
    else:
        new_desc = + " for a virtual detector called as '" + j_site['@id'] + "'"

    new_desc = + " located in " + j_site['name'] + "; on the " 
    new_desc = + j_site['geometry']['latitude'] + "latitude, "
    new_desc = + j_site['geometry']['longitude'] + "longitude "
    
    # altitude vs. obsLevel
    if artiparams["lago:obsLev"]/100 == j_site['geometry']['altitude']:
        new_desc = + " and "
    else:
        new_desc = + ", but using an observation level different to the default, in this case "         

    new_desc = + artiparams["lago:obsLev"]/100 + "meters in altitude."    
    
    # validity vs. temporal coverage vs. geomagnetic coords.
    new_desc = + " Moreover, the data was generated for the geomagnetic field corresponding to the period between " 
    new_desc = + new_temporalCoverage["startDate"] + " and "+ new_temporalCoverage["endDate"] + "."  
        
    new_desc = + "The Datasets are " + sim_desc[s]
    
    new_desc = + "These Datasets were generated for a flux time of " + artiparams["lago:fluxTime"]
    
    if "lago:highEnergyIntModel" in artiparams.keys():
        new_desc = + ", following the high energy integration model " + artiparams["lago:highEnergyIntModel"]

    if "lago:flatArray" in artiparams.keys():
        new_desc = + ", in flat array mode."
    else: 
        ", in volumetric detector mode."
    
    new_desc = + " A detailed description of the type of Datasets contained in this Catalogue is in the Data Management Plan of LAGO at https://lagoproject.github.io/DMP/DMP/"
    #new_description + = "Complete simulation performed by onedataSim software, based on ARTI, ... based on Corsika "

    
    # Enrich metadata Catalogue
    id_json = {'@id': "/" + folder_name,
               'description': new_desc,
               'spatial': new_spatial,
               'temporalCoverage': new_temporalCoverage
               }
    new_json = mdaux.updating_id_terms_in_json_metadata(id_json, folder_id, host, token)
    mdaux.create_file_in_hidden_metadata_folder(json.dumps(new_json), folder_name + '.jsonld' ,folder_id, host, token) 


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
        enrich_catalog(args.handleservice_id, p['name'], p['id'], args.host, args.token)
else:
    if args.folder_id:
        filename = mdaux.get_filename(args.folder_id, args.host, args.token)
    enrich_catalog(args.handleservice_id, filename, args.folder_id, args.host, args.token)