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
    
    urljson = "https://raw.githubusercontent.com/lagoproject/DMP/1.1.0/defs/sitesLago.1.1.jsonld"
    r_json = mdaux.requests.get(urljson)
    j =  json.loads(r_json.text)
    
    return mdUtils.get_item_by_id(j, site)

def enrich_catalog(only_test, folder_name, folder_id, host, token):
    
    # get current schema
    r_json = mdaux.requests.get("https://raw.githubusercontent.com/lagoproject/DMP/1.1.0/schema/lagoSchema.1.1.jsonld")
    schema = json.loads(r_json.text)
    
    # get current metadata
    old_json = mdaux.get_json_metadata(folder_id, host, token)
    
    #only works if complete catalogue:
    if "dataset" not in old_json.keys():
        print("\n Can\'t enrich: " + folder_name + "\n") 
        return 

    artiparams =  mdUtils.get_item_by_id(old_json, "/" + folder_name + "#artiParams")
    
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
    # what simulation S0, S1, S2
    s = folder_name.split('_')[0]


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
    isdefaultalt = False
    print(artiparams)
    if "lago:obsLev" in artiparams.keys():
        new_spatial['geometry']['geo:altitude'] = str(float(artiparams["lago:obsLev"])/100)
    else: 
        new_spatial['geometry']['geo:altitude'] = j_site['geometry']['geo:altitude']
        isdefaultalt = True
    
    #new  temporalCoverage
    # "endDate": "2021-05-19T15:01:26" -> bDate + "lago:fluxTime"
    if s == "S0":
        bDate = j_site["lago:magnet"]["@default"]['lago:bDate']
        new_temporalCoverage = {
                "startDate": bDate+"T00:00:00Z",  # is UTC
                "endDate": mdUtils.xsd_dateTime_add_elapsed(bDate,artiparams["lago:fluxTime"]) 
            }
    else:
        # temporal coverage source dataset (S0 or S1)
        # anonter_j_site[]... FALTA PARCHEAR EL SOURCE DATASET
        print("\n Can\'t enrich: " + folder_name + "\n") 
        return 

    #
    # make new description ....
    #
    new_desc = ""
    
    sim_type = {'S0' : 'plain simulation',
                'S1' : 'analyzed simulation',
                'S2' : 'detector response simulation'}
    sim_desc = {'S0' : 'CORSIKA inputs and outputs, which are described in the official documentation ( https://www.iap.kit.edu/corsika/70.php ).',
                'S1' : 'ARTI analysis and outputs of previous S0 Datasets, containing the expected flux of secondary particles at the ground.', 
                'S2' : 'outputs of ARTI detector simulation module, containing a complete, detailed and adjustable Geant4 model of the LAGO detectors. The main output is the expected signals in the detector, allowing site characterization and comparison with all the measured data sets (L*) at each site.'}

    new_desc = " This Catalogue contains a complete LAGO (" + s + ") " + sim_type[s]
    #OJO, SERIA MEJOR TENER UN 'label' en vez de un '@id'
    if j_site["lago:belongsLago"]:
        new_desc += " for the LAGO '" + j_site['@id'] + "' site"
        if  j_site["qualifiedAttribution"]["name"] != "":
            new_desc += " managed by the "+ j_site["qualifiedAttribution"]["name"] + " institution; "
    else:
        new_desc +=  " for a virtual detector called as '" + j_site['@id'] + "'"

    new_desc += " located in " + j_site['name'] + ", on the " 
    new_desc += j_site['geometry']['geo:latitude'] + " latitude,"
    new_desc += " " + j_site['geometry']['geo:longitude'] + " longitude"
    
    # altitude vs. obsLevel
    #if artiparams["lago:obsLev"]/100 == j_site['geometry']['altitude']:
    if isdefaultalt:
        new_desc += " and "
    else:
        new_desc += ", but using an observation level different to the default, in this case "         

    new_desc += new_spatial['geometry']['geo:altitude'] + " meters in altitude."    
    
    # validity vs. temporal coverage vs. geomagnetic coords.
    new_desc += " Moreover, the data was generated for the geomagnetic field corresponding to the period between " 
    new_desc += new_temporalCoverage["startDate"] + " and "+ new_temporalCoverage["endDate"] + "."  
        
    new_desc += "\n\n The Datasets are " + sim_desc[s]
    
    new_desc += " These Datasets were generated for a flux time of " + artiparams["lago:fluxTime"].replace("P","").replace("S","") + " seconds"
    
    if "lago:highEnergyIntModel" in artiparams.keys():
        new_desc += ", following the high energy integration model " + artiparams["lago:highEnergyIntModel"]

    if "lago:flatArray" in artiparams.keys():
        new_desc += ", in flat array mode."
    else: 
        ", in volumetric detector mode."

    if "lago:highEnergyCutsSecondaries" in artiparams.keys(): 
        new_desc += " Additionally, high energy cuts for secondaries were used, so there are no secondary particles with energies E < " +  artiparams["lago:highEnergyCutsSecondaries"] + " GeV."    

    if "lago:modatm" in artiparams.keys(): 
        new_desc += " The " + artiparams["lago:modatm"] + " external atmosphere file was used for this site." 
    else:
        new_desc += " The default atmosphere (" + j_site["lago:atmcrd"]["lago:modatm"]["@default"] + ") was used for this site."

    if "lago:tMin" not in artiparams.keys():
        artiparams["lago:tMin"] = mdUtils.get_item_by_id(schema,"lago:tMin")["@default"]
    if "lago:tMax" not in artiparams.keys(): 
        artiparams["lago:tMax"] = mdUtils.get_item_by_id(schema,"lago:tMax")["@default"]

    new_desc += " The zenith range used was set to [" + str(artiparams["lago:tMin"]) + "," + str(artiparams["lago:tMax"]) +"] degrees."    

#BUG llimit ulimit -> lLimit uLimit
    # lower and upper limit and rigidity:
    if "lago:lLimit" not in artiparams.keys():
        artiparams["lago:lLimit" ] = mdUtils.get_item_by_id(schema,"lago:lLimit")["@default"]  
     
    if "lago:uLimit" not in artiparams.keys(): 
        artiparams["lago:uLimit" ] = mdUtils.get_item_by_id(schema,"lago:uLimit")["@default"]
 
    new_desc += " The primary integration energy range used was set to [" + artiparams["lago:lLimit" ] + "," + artiparams["lago:uLimit"] +"] GeV."
        
    # la rigidez es GV y no GeV (porque la rigidez se define como función de la carga: E_cut = p * c * Z, donde p es el momento de la partícula, c la velocidad de la luz, 1, y Z es la carga). 
    if "lago:rigidity" in artiparams.keys(): 
        new_desc += " The local rigidity cutoff was set to " + artiparams["lago:rigidity" ] + " GV."

    new_desc += "\n\n The completeness of the simulation and the requirements for its storing and publishing was guaranteed by the onedataSim software ( https://github.com/lagoproject/onedataSim ), relying on the ARTI software ( https://github.com/lagoproject/arti )."
    new_desc += " A detailed description of the type and generation of the Datasets and Metadata contained in this Catalogue is in the Data Management Plan of LAGO at https://lagoproject.github.io/DMP/"
    
    new_desc += "\n\n Please, you properly cite this Catalogue with its PiD as well as with the main papers currently listed in the previous pages as reference works."
        
    # Enrich metadata Catalogue
    id_json = {'@id': "/" + folder_name,
               'description': new_desc,
               'spatial': new_spatial,
               'temporalCoverage': new_temporalCoverage
               }
    
    print('\n\n')
    print(folder_name)
    print('\n')
    if only_test:
        print(id_json)
    else:
        new_json = mdaux.updating_id_terms_in_json_metadata(id_json, folder_id, host, token)
        print(new_json)
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
parser.add_argument('--only_test', action='store_true', default=False,
                     help="If it is set, only test the changes and outputs)")

args = parser.parse_args()

if args.myspace_path:
    args.folder_id = mdaux.get_folder_id(args.myspace_path, args.host, args.token) 

#solo un nivel de recursividad, preparado para que desde un Space, se cambien solo los metadata del catalogo
if args.recursive is True:
    all_level0 = mdaux.folder0_content(args.folder_id, args.host, args.token)
    for p in all_level0['children']:
        enrich_catalog(args.only_test, p['name'], p['id'], args.host, args.token)
else:
    if args.folder_id:
        filename = mdaux.get_filename(args.folder_id, args.host, args.token)
    enrich_catalog(args.only_test, filename, args.folder_id, args.host, args.token)