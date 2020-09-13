#!/usr/bin/env python3
#
################################################################################
# Original Author: A.J. Rubio-Montero (http://orcid.org/0000-0001-6497-753X),  #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track), #
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).         #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause)  #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)   #
################################################################################


# additional modules needed 
# apt-get install python3-xattr 
# or yum install -y python36-pyxattr 
import subprocess, os, shutil, xattr, json, datetime, fcntl, sys, shlex

from threading import Thread
from queue import Queue

#
from arguments import *



onedataSimPath = os.path.dirname(os.path.abspath(__file__))

#----- utils -----

def _run_Popen_interactive(command): 
    
    print (command+'\n')
    p = subprocess.Popen(shlex.split(command), env=os.environ, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    p.wait()


def _run_Popen(command):  
    print (command+'\n')      
    p = subprocess.Popen(command + ' 2>&1', shell = True, env=os.environ, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait()
    res = p.communicate()[0]
    if p.returncode != 0:
        print (str(res)+'\n')
        res=""
    return res

def _xsd_dateTime ():

    # xsd:dateTime
    # CCYY-MM-DDThh:mm:ss.sss[Z|(+|-)hh:mm]
    # The time zone may be specified as Z (UTC) or (+|-)hh:mm. 
    return str(datetime.datetime.utcnow()).replace(' ','T')+'Z'

# j is adding j_new terms to existing keys or adding keys.
# j and j_new must have same structure (pruned) tree
# (dict.update adds only when key not exist, otherwise replace)
def _add_json (j, j_new):
    
    if type(j) is list:
        if type(j_new) is list:
            j+=j_new
            return j
        return j.append(j_new)
    
    if (type(j) is dict) and (type(j_new) is dict):
        k_old=j.keys()
        for k,v in j_new.items():
            if k in k_old:
                j[k]=_add_json(j[k],v)
            else: 
                j[k]=v
        return j
    
    # is not a list or a dict, is a term. I change to list and call recursiveness
    return _add_json([j],j_new)
    
        
        
    
    
#####


def get_first_catalog_metadata_json (catcodename,orcid):

    with open(onedataSimPath+'/json_tpl/common_context.json', 'r') as file1: 
        with open(onedataSimPath+'/json_tpl/catalog_corsika.json', 'r') as file2:
                j=json.loads(file1.read())
                j=_add_json(j,json.loads(file2.read()))
                s=json.dumps(j)
                s=s.replace('CATCODENAME', catcodename)
                s=s.replace('ORCID', orcid)
                return json.loads(s)



def get_catalog_metadata_activity (startdate, enddate):

    with open(onedataSimPath+'/json_tpl/catalog_corsika_activity.json', 'r') as file1: 
        j=json.loads(file1.read())
        s=json.dumps(j)
        s=s.replace('CATCODENAME', catcodename)
        s=s.replace('STARTDATE', startdate)
        s=s.replace('ENDDATE', enddate)
        return s
        


######

def _get_common_metadata_aux ():

    with open(onedataSimPath+'/json_tpl/common_context.json', 'r') as file1: 
        with open(onedataSimPath+'/json_tpl/common_dataset.json', 'r') as file2:
                j=json.loads(file1.read())
                j=_add_json(j,json.loads(file2.read()))
                return j
                
                
def _get_input_metadata (filecode):

    with open(onedataSimPath+'/json_tpl/dataset_corsika_input.json', 'r') as file1: 
        j=_get_common_metadata_aux()
        j=_add_json(j,json.loads(file1.read()))
        s=json.dumps(j)
        s=s.replace('FILENAME', 'DAT'+filecode+'.input')
        #warning, corsikainput metadata must be included also...
        return s;
    
def _get_bin_output_metadata (filecode):
    with open(onedataSimPath+'/json_tpl/common_dataset_corsika_output.json', 'r') as file1: 
        with open(onedataSimPath+'/json_tpl/dataset_corsika_bin_output.json', 'r') as file2: 
            j=_get_common_metadata_aux()
            j=_add_json(j,json.loads(file1.read()))
            j=_add_json(j,json.loads(file2.read()))
            s=json.dumps(j)
            runnr=filecode.split('-')[0]
            s=s.replace('FILENAME', 'DAT'+runnr+'.bz2')
            return s;
        
 
def _get_lst_output_metadata (filecode):

    with open(onedataSimPath+'/json_tpl/common_dataset_corsika_output.json', 'r') as file1:
        with open(onedataSimPath+'/json_tpl/dataset_corsika_lst_output.json', 'r') as file2: 
            j=_get_common_metadata_aux()
            j=_add_json(j,json.loads(file1.read()))
            j=_add_json(j,json.loads(file2.read()))
            s=json.dumps(j)
            s=s.replace('FILENAME', 'DAT'+filecode+'.lst.bz2')
            #falta comprimir si fuera necesario
            return s;


def get_dataset_metadata (catcodename, filecode, startdate, end_date):

    mdlistaux=[_get_bin_output_metadata(filecode),_get_lst_output_metadata(filecode),_get_input_metadata(filecode)]
    mdlist=[]
    for s in mdlistaux:
        s = s.replace('CATCODENAME', catcodename)
        s = s.replace('NRUN', filecode)
        s = s.replace('STARTDATE', startdate)
        s = s.replace('ENDDATE', end_date)
        mdlist.append(s)
    return mdlist
   

   
#########

def _run_check_and_copy_results (catcodename, filecode, task, onedata_path): 
 
    start_date=_xsd_dateTime()

    try: 
        _run_Popen(task)
        metadatalist=get_dataset_metadata(catcodename, filecode, start_date, _xsd_dateTime())
        for md in metadatalist:
            id=json.loads(md)['@id']
            shutil.move('.' + id, onedata_path + id) 
            xattr.setxattr(onedata_path + id, 'onedata_json', md)
    except Exception as inst:
        raise inst

       
     

#------------ producer/consumer ---------

main_start_date = _xsd_dateTime()
q = Queue()


def _producer (catcodename, arti_params):
        
    cmd = 'do_sims.sh '+ arti_params
    _run_Popen_interactive(cmd)
    
    #WARNING, I HAD TO PATCH rain.pl FOR AVOID SCREEN !!!!
    cmd="sed 's/screen -d -m -a -S \$name \$script; screen -ls/\$script/' rain.pl -i"
    _run_Popen(cmd)
    #WARNING, I HAD TO PATCH rain.pl FOR AVOID .long files !!!
    cmd="sed 's/\$llongi /F /' rain.pl -i"
    _run_Popen(cmd)
    
    #-g only creates .input's
    #cmd="sed 's/\.\/rain.pl/echo \$i: \.\/rain.pl -g /' go-*.sh  -i"
    cmd="sed 's/\.\/rain.pl/echo \$i: \.\/rain.pl /' go-*.sh  -i"
    _run_Popen(cmd)
    cmd ="cat go-*.sh | bash  2>/dev/null"
    lines=_run_Popen(cmd).decode("utf-8").split('\n')
    for l in lines:
        if l !="" :
            print (l)
            l_aux=l.split(":")
            runnr=l_aux[0]
            #prmpar name only allows 4 characters, 
            # we use zfill to fill with 0's and limit to 4 characters if were needed.
            prmpar=str(int(runnr)).zfill(4)[-4:]
            task=l_aux[1]
            l_aux=task.split(catcodename)
            s_aux=l_aux[1].replace('/','')
            s_aux=l_aux[1].replace('.run','')
            l_aux=s_aux.split('-')
            filecode=runnr+'-'+prmpar+'-'+l_aux[1]
            q.put((filecode, task))





def _consumer (catcodename, onedata_path):
    while True:
        (filecode, task) = q.get()
        try:
            _run_check_and_copy_results(catcodename, filecode, task, onedata_path)
            print ('Completed NRUN: ' +str(filecode) +'  '+ task)
            q.task_done()
        except Exception as inst:
            q.put((filecode, task)) 
        


#------------ main stuff ---------

(arti_params, arti_params_dict, arti_params_json_md) = get_sys_args()
catcodename = arti_params_dict["p"] 
#onedata_path = '/mnt/LAGOsim'
onedata_path = '/mnt/test4/LAGOSIM'
catalog_path = onedata_path + '/' +catcodename

print (arti_params, arti_params_dict, arti_params_json_md)

try: 
    #mount OneData
    cmd="oneclient /mnt"
    _run_Popen(cmd)
    if os.path.exists(onedata_path): 
        if not os.path.exists(catalog_path):
            os.mkdir(catalog_path)
        else:
            # It is need manage this with some kind of versioning or completion of failed simulations
            raise Exception("Simulation already in OneData") 
    else:
        raise Exception("OneData not mounted")
except Exception as inst:
    raise inst


md=get_first_catalog_metadata_json(catcodename,arti_params_dict['u'])
md=_add_json(md,arti_params_json_md)
xattr.setxattr(catalog_path, 'onedata_json', json.dumps(md))

for i in range(arti_params_dict["j"]): #processors
    t = Thread(target=_consumer, args=(catcodename, onedata_path))
    t.daemon = True
    t.start()

_producer(catcodename, arti_params)
q.join()



md=_add_json(md,{'dataset':["/" + catcodename + "/" + s for s in os.listdir(catalog_path)]})
md=_add_json(md,json.loads(get_catalog_metadata_activity(main_start_date, _xsd_dateTime())))
xattr.setxattr(catalog_path, 'onedata_json', json.dumps(md))
    
    
              

