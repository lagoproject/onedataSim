#
###############################################################################
# Original Author: A.J. Rubio-Montero (http://orcid.org/0000-0001-6497-753X), #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track),#
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).        #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause) #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)  #
###############################################################################


# additional modules needed
# apt-get install python3-xattr
# or yum install -y python36-pyxattr
import os
import xattr
import json
import shutil
import time

from threading import Thread
from queue import Queue

# own functions
from utils import _run_Popen, _run_Popen_interactive, _write_file,
    _xsd_dateTime, _add_json, 
    get_first_catalog_metadata_json,get_catalog_metadata_activity 





class ARTIwrapper(self):    

    
    def __init__(self, get_sys_args, get_dataset_metadata, producer):
        self._q = None
        self._q_onedata = None
        # passed functions
        self._get_sys_args = get_sys_args
        self._get_dataset_metadata = get_dataset_metadata
        self._producer = producer
        
    # ---- queued operations through OneClient -----------
    
    def _consumer_onedata_cp(self, onedata_path):
        
        while True:
            md = self._q_onedata.get()
            try:
                id = json.loads(md)['@id']
                # oneclient change the filename owner when you move it to
                # onedata and this action raise exceptions with shutil.move()
                # shutil.move('.' + id, onedata_path + id)
                #  
                # copy if the file exists, if not can be because corsika failed
                if os.path.exists("." + id):
                    cmd = "cp ." + id + " " + onedata_path + id
                    _run_Popen(cmd)
                    time.sleep(0.1)
                    # test if effectively copied to copy metadata
                    if os.path.exists(onedata_path + id):
                        xattr.setxattr(onedata_path + id, 'onedata_json', md)
                        id_hidden = '/' + id.lstrip('/').replace('/','/.metadata/.')
                        _write_file(onedata_path + id_hidden + '.jsonld', md)
                    else:
                        print('CAUTION: '+ id +' is not in onedata, requeuing...' )
                        raise inst
                    # thus, I can remove local file 
                    cmd = "rm -f ." + id
                    _run_Popen(cmd)
                else:
                    print('ERROR: '+ id +' was not calculated')
    
                self._q_onedata.task_done()
    
            except Exception as inst:
                print(id + ': copy queued again')
                self._q_onedata.put(md)
                time.sleep(2)
    
    
    def _run_check_and_copy_results(self, catcodename, filecode, task, onedata_path,
                                    arti_params_dict):
    
        # check if the results are already in onedata before running the task
        runtask = False
        mdlist_prev = self._get_dataset_metadata(catcodename, filecode,
                                                _xsd_dateTime(), _xsd_dateTime(),
                                                arti_params_dict)
        for md in mdlist_prev:
            id = json.loads(md)['@id']
            # We should also check if the existent metadata is well formed
            f = onedata_path + id
            # print("Check if exist: " + f)  
            if not os.path.exists(f):
                print("This result does not exist in onedata: " + f)
                print("Thus... I will RUN : " + filecode)
                runtask = True
                break
    
        if not runtask:
            print("Results already in OneData, none to do with RUN : " + filecode)
        else:
            try:
                start_date = _xsd_dateTime()
                _run_Popen(task)
                metadatalist = self._get_dataset_metadata(catcodename, filecode, 
                                                          start_date, _xsd_dateTime(),
                                                          arti_params_dict)
                
                for md in metadatalist:
                    self._q_onedata.put(md)
            except Exception as inst:
                raise inst
            
    # ---- END: queued operations through OneClient -----------
    
    # ---- producer/consumer of executions ---------
    
    # Introduced as param in init()
    # function inputs: catcodename, arti_params
    #          output: Queue() with (filecode, task) elements
    #def _producer(self, catcodename, arti_params):
    
    
    def _consumer(self, catcodename, onedata_path, arti_params_dict):
        while True:
            (filecode, task) = q.get()
            try:
                _run_check_and_copy_results(catcodename, filecode, task,
                                            onedata_path, arti_params_dict)
                print('Completed NRUN: ' + str(filecode) + '  ' + task)
                self._q.task_done()
            except Exception as inst:
                self._q.put((filecode, task))
    
    # ---- END: producer/consumer of executions ---------
    
    
    # ---- MAIN PROGRAM ---------
    
    def run(self):

        main_start_date = _xsd_dateTime()
        (arti_params, arti_params_dict, arti_params_json_md) = self._get_sys_args()
        catcodename = arti_params_dict["p"]
        # onedata_path = '/mnt/datahub.egi.eu/LAGOsim'
        onedata_path = '/mnt/datahub.egi.eu/test8/LAGOSIM'
        catalog_path = onedata_path + '/' + catcodename
        
        print(arti_params, arti_params_dict, arti_params_json_md)
        
        try:
            # mount OneData (fails in python although you wait forever):
            # removed, currently in Dockerfile.
            # cmd = "oneclient --force-proxy-io /mnt"
            # _run_Popen(cmd, timeout=10)
            if os.path.exists(onedata_path):
                if not os.path.exists(catalog_path):
                    os.mkdir(catalog_path, mode=0o755) # this should change to 0700
                    os.mkdir(catalog_path + '/.metadata', mode=0o755) # idem to 0700
                    md = get_first_catalog_metadata_json(catcodename, 
                                                         arti_params_dict)
                    md = _add_json(md, arti_params_json_md)
                    _write_file(catalog_path + '/.metadata/.' + catcodename + '.jsonld',
                                json.dumps(md))
                    xattr.setxattr(catalog_path, 'onedata_json', json.dumps(md))
                else: 
                    if not os.access(catalog_path, os.W_OK):
                        # It is needed managing this with some kind of versioning
                        # or completion of failed simulations
                        raise Exception("Simulation blocked by other user in" + \
                                        " OneData: " + catalog_path)
            else:
                raise Exception("OneData not mounted")
        except Exception as inst:
            raise inst
        
        for i in range(int(arti_params_dict["j"])):  # processors
            t = Thread(target=self._consumer, args=(catcodename, onedata_path,
                                               arti_params_dict))
            t.daemon = True
            t.start()
        
        self._q = self._producer(catcodename, arti_params)
        
        t = Thread(target=self._consumer_onedata_cp, args=(onedata_path,))
        t.daemon = True
        t.start()
        
        self._q.join()
        self._q_onedata.join()
        
        
        md = json.loads(xattr.getxattr(catalog_path, 'onedata_json'))
        
        # I'm replacing, not adding datasets. 
        md['dataset'] = ["/" + catcodename + "/" + s for s in 
                         os.listdir(catalog_path) if not s.startswith('.')]
        
        md = _add_json(md, json.loads(get_catalog_metadata_activity(main_start_date,
                                                                    _xsd_dateTime(),
                                                                    arti_params_dict)))
        
        _write_file(catalog_path + '/.metadata/.' + catcodename + '.jsonld',
                    json.dumps(md))
        xattr.setxattr(catalog_path, 'onedata_json', json.dumps(md))
        
        