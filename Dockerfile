################################################################################
# Original Author: A.J. Rubio-Montero (http://orcid.org/0000-0001-6497-753X),  #
#          CIEMAT - Sci-Track Group (http://rdgroups.ciemat.es/web/sci-track), #
#          for the EOSC-Synergy project (EU H2020 RI Grant No 857647).         #
# License (SPDX): BSD-3-Clause (https://opensource.org/licenses/BSD-3-Clause)  #
# Copyright (c): 2020-today, The LAGO Collaboration (http://lagoproject.net)   #
################################################################################

FROM centos:7.8.2003

# 
ARG ONECLIENT_ACCESS_TOKEN_TO_BUILD
ARG ONECLIENT_PROVIDER_HOST_TO_BUILD
ARG ONEDATASIM_BRANCH="master"

# user credentials when the container were used
ENV ONECLIENT_ACCESS_TOKEN=""
ENV ONECLIENT_PROVIDER_HOST=""

#to limit to this minor SO release
RUN echo '7.8.2003' > /etc/yum/vars/releasever
RUN sed -e '/mirrorlist=.*/d' \
    -e 's/#baseurl=/baseurl=/' \
    -e "s/\$releasever/7.8.2003/g" \
    -e "s/mirror.centos.org\\/centos/vault.centos.org/g" \
    -i /etc/yum.repos.d/CentOS-*
RUN yum -y update

# CORSIKA pre-requisites
RUN yum -y install gcc gcc-c++ gcc-gfortran \
        curl csh make perl perl-Data-Dumper \
        git perl-Switch

# CORSIKA autorished copy for internal distribution on the LAGO Collaboration (CDMI private link)
#RUN curl -k -H "X-Auth-Token: $ONECLIENT_ACCESS_TOKEN_TO_BUILD" \
#               "$ONECLIENT_PROVIDER_HOST_TO_BUILD/cdmi/test4/corsika/corsika-75600-lago.tar.gz" \
#               | tar xvz -C /opt              
RUN while ! curl -O -C- -k -H "X-Auth-Token: $ONECLIENT_ACCESS_TOKEN_TO_BUILD" \
                 "$ONECLIENT_PROVIDER_HOST_TO_BUILD/cdmi/LAGOsoft/corsika/corsika-75600-lago.tar.gz" ; \ 
                 do true ; done
RUN tar -xvzf ./corsika-75600-lago.tar.gz --directory /opt 
RUN rm -f corsika-75600-lago.tar.gz

RUN cd /opt/corsika-75600-lago && ./coconut -b

## testing corsika
## ./corsika75600Linux_QGSII_gheisha < all-inputs > output.txt


#dowload and compile ARTI LAGO crktools
RUN yum -y install bzip2
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
RUN mkdir -p /mnt/datahub.egi.eu && echo 'oneclient --force-proxy-io /mnt/datahub.egi.eu/' >> /root/.bashrc

#getfacl getfattr 
RUN yum -y install acl attr 

# xattr (this is  python2 but I had found the command only in python2)
RUN yum -y install  python2-pip python-devel libffi-devel 
# sometimes pip's upgrade fails
#RUN pip install --upgrade pip
RUN pip install xattr

#python3 and libraries for Lago processing with onedata
RUN yum -y install python3 python36-pyxattr

WORKDIR /opt/corsika-75600-lago/run
#ENTRYPOINT /opt/arti/sims/do_datahub.sh
CMD bash
