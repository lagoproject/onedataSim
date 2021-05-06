#
###############################################################################
# Original Author: A.J. Rubio-Montero (http://orcid.org/0000-0001-6497-753X), #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track),#
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).        #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause) #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)  #
###############################################################################


import os
import subprocess
import sys
import shlex


def run_Popen_interactive(command):

    print(command+'\n')
    p = subprocess.Popen(shlex.split(command), env=os.environ,
                         stdin=sys.stdin, stdout=sys.stdout,
                         stderr=sys.stderr)
    p.wait()

def run_Popen(command, timeout=None):

    print(command+'\n')
    p = subprocess.Popen(command + ' 2>&1', shell=True, env=os.environ,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait(timeout)
    res = ""
    if p.returncode != 0:
        print("Return code: "+str(res)+'\n')
    else:
        res = p.communicate()[0]
    return res


def _write_file(filepath, txt):
    
    with open(filepath, 'w+') as file1:
        file1.write(txt)
        









