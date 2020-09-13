#
################################################################################
# Original Author: A.J. Rubio-Montero (http://orcid.org/0000-0001-6497-753X),  #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track), #
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).         #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause)  #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)   #
################################################################################



#set LAGO onedataSim env
LAGO_ONEDATASIM=${PWD}
date=$(date -u)
echo "
#
## Changes added by the LAGO onedataSim suite on $date
#
export LAGO_ONEDATASIM=\"${LAGO_ONEDATASIM}\"
export PATH=\"\${LAGO_ONEDATASIM}/wrappers/:\$PATH\"
" >> ${HOME}/.bashrc

#add execution permissions:
chmod +x $LAGO_ONEDATASIM/wrappers/do_onedata.py

