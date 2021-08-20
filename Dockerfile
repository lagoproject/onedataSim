################################################################################
# Original Author: A.J. Rubio-Montero (http://orcid.org/0000-0001-6497-753X),  #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track), #
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).         #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause)  #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)   #
################################################################################

#I need some distribution to RUN if-then-else
FROM centos:7
#--build-arg TYPE=S0, S1 or S2, is mandatory
ARG TYPE
# BASE_OS private,  only for development purposes
ENV BASE_OS=""
RUN if [ "$TYPE" = "S0" ] ; \
    then BASE_OS="lagoproject.net/corsika:xxxx" ; \
    elif [ "$TYPE" = "S1" ] ; \
    then BASE_OS="centos:7" ; \
    elif [ "$TYPE" = "S2" ] ; \
    then BASE_OS="lagoproject.net/geant4:xxxx" ; \
    else echo "Error: --build-arg TYPE=S0, S1 or S2, is mandatory "; \
    fi

#An ARG declared before a FROM is outside of a build stage, so it can’t be used in any instruction after a FROM
FROM $BASE_OS
#
ARG ONEDATASIM_BRANCH="master"
# user credentials when the container were used
ENV ONECLIENT_ACCESS_TOKEN=""
ENV ONECLIENT_PROVIDER_HOST=""

RUN yum -y update

#dowload and compile ARTI LAGO crktools
RUN yum -y install git bzip2
# we use the ones tested with onedataSim package
# RUN cd /opt && git clone https://github.com/lagoproject/arti.git
RUN cd /opt && git clone --branch $ONEDATASIM_BRANCH --recursive https://github.com/lagoproject/onedataSim.git
RUN cd /opt/onedataSim/arti && make
#set paths and permissions for onedataSim
RUN cd /opt/onedataSim && bash install.sh

#Onedata and tools needed by onedataSim

#download and install oneclient
#We did not use oneclient for downloading corsika-lago to isolate from its compiling
# and because it were need use privileged mode.
RUN curl -sS http://get.onedata.org/oneclient-2002.sh | bash
RUN mkdir -p /mnt/datahub.egi.eu && echo 'nice -n -10 oneclient --force-proxy-io /mnt/datahub.egi.eu/' >> /root/.bashrc

#getfacl getfattr
RUN yum -y install acl attr

# xattr (this is  python2 but I had found the command only in python2)
RUN yum -y install  python2-pip python-devel libffi-devel
# sometimes pip's upgrade fails and doesn't find "typing" module
# RUN pip install --upgrade pip
# RUN pip install typing
RUN pip install cffi
RUN pip install xattr


#python3 and libraries for Lago processing with onedata
RUN yum -y install python3 python36-pyxattr

WORKDIR /opt/corsika-77402-lago/run
#ENTRYPOINT /opt/arti/sims/do_datahub.sh
CMD bash
