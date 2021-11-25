#
###############################################################################
# Original Author: A.J. Rubio-Montero (http://orcid.org/0000-0001-6497-753X), #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track),#
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).        #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause) #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)  #
###############################################################################

import os
import json
import datetime

# own modules
import osUtils


def get_git_commit(repopath):

    cmd = "git --git-dir " + repopath + "/.git rev-parse --verify HEAD"
    lines = osUtils.run_Popen(cmd).decode("utf-8").split('\n')
    if str(lines[0]) != "":
        return str(lines[0])
    else:
        raise Exception("Git release of software not found")


def xsd_dateTime():

    # xsd:dateTime
    # CCYY-MM-DDThh:mm:ss.sss[Z|(+|-)hh:mm]
    # The time zone may be specified as Z (UTC) or (+|-)hh:mm.
    return str(datetime.datetime.utcnow()).replace(' ', 'T')+'Z'


# j is adding j_new terms to existing keys or adding keys.
# j and j_new must have same structure (pruned) tree
# (dict.update adds only when key not exist, otherwise replace)
def add_json(j, j_new):

    if type(j) is list:
        if type(j_new) is list:
            j += j_new
            return j
        return j.append(j_new)

    if (type(j) is dict) and (type(j_new) is dict):
        k_old = j.keys()
        for k, v in j_new.items():
            if k in k_old:
                j[k] = add_json(j[k], v)
            else:
                j[k] = v
        return j

    # is not a list or a dict, is a term.
    # I change to list and call recursiveness
    return add_json([j], j_new)


def replace_common_patterns(s, catcodename, arti_params_dict):

    s = s.replace('CATCODENAME', catcodename)
    s = s.replace('ORCID', arti_params_dict['u'])
    if 'v' in arti_params_dict :
        s = s.replace('CORSIKA_VER', arti_params_dict['v'])
        s = s.replace('COMMITSHACORSIKA', arti_params_dict['priv_corsikacommit'])
    # other private generated without arguments (arg_xxx.py)
    s = s.replace('COMMITSHAARTI', arti_params_dict['priv_articommit'])
    s = s.replace('COMMITSHAODSIM', arti_params_dict['priv_odsimcommit'])
    s = s.replace('HANDLEJSONAPI', arti_params_dict['priv_handlejsonapi'])
    s = s.replace('HANDLECDMI', arti_params_dict['priv_handlecdmi'])
    s = s.replace('LANDINGPAGE', arti_params_dict['priv_landingpage'])
    return s


template_path = os.path.dirname(os.path.abspath(__file__)) + '/json_tpl/'


def get_metadata_for_dataset(args=[]):
    
    common = ['common_context.json', 'common_dataset.json']
    templates = common + args
    j={}
    for temp in templates:
        with open(template_path + temp, 'r') as file_aux:
            j = add_json(j, json.loads(file_aux.read()))
    s = json.dumps(j)
    return s


# warning: this returns json.loads
def get_first_catalog_metadata_json(catcodename, arti_params_dict):

    with open(template_path+'common_context.json', 'r') as file1:
        with open(template_path+'common_catalog.json', 'r') as file2:
            j = json.loads(file1.read())
            j = add_json(j, json.loads(file2.read()))
            s = json.dumps(j)
            s = replace_common_patterns(s, catcodename, arti_params_dict)
            return json.loads(s)


def get_catalog_metadata_activity(startdate, enddate, catcodename, arti_params_dict):

    with open(template_path+'common_activity.json', 'r') as file1:
        j = json.loads(file1.read())
        s = json.dumps(j)
        s = s.replace('STARTDATE', startdate)
        s = s.replace('ENDDATE', enddate)
        s = replace_common_patterns(s, catcodename, arti_params_dict)
        return s
