# LAGO onedataSim : packed tools for [ARTI](https://github.com/lagoproject/arti) simulation and analisys on [OneData](https://github.com/onedata)

| Plain tests in dev branch: 
[![Build Status](https://jenkins.eosc-synergy.eu/buildStatus/icon?job=eosc-synergy-org%2FonedataSim%2Fdev)]
(https://jenkins.eosc-synergy.eu/job/eosc-synergy-org/job/onedataSim/job/dev/) | 
onedatasim-s0 image: 
[![Build Status](https://jenkins.eosc-synergy.eu/buildStatus/icon?job=eosc-synergy-org%2FonedataSim%2Fbuild-S0)]
(https://jenkins.eosc-synergy.eu/job/eosc-synergy-org/job/onedataSim/job/build-S0/) | 
onedatasim-s1 image: 
[![Build Status](https://jenkins.eosc-synergy.eu/buildStatus/icon?job=eosc-synergy-org%2FonedataSim%2Fbuild-S1)]
(https://jenkins.eosc-synergy.eu/job/eosc-synergy-org/job/onedataSim/job/build-S1/) |
|------|------|-------|

## About

onedataSim standardises the simulations and their analysis in LAGO Collaboration to curate, re-use and publish the results, following the Data Management Plan (DMP) established (https://lagoproject.github.io/DMP/). For this purpose, onedataSim packets ARTI and related software into a Docker image, giving researchers the advantage of obtaining results on any plataform and publishing them on LAGO repositories.

### Citing

When using onedataSim or the data and metadata that it outputs, please cite the current main reference reported below:

   A. J. Rubio-Montero, R. Pagán-Muñoz, R. Mayo-García, A. Pardo-Diaz, I. Sidelnik and H. Asorey, "*A Novel Cloud-Based Framework For Standardized Simulations In The Latin American Giant Observatory (LAGO)*," 2021 Winter Simulation Conference (WSC), 2021, pp. 1-12, doi: [10.1109/WSC52266.2021.9715360](https://doi.org/10.1109/WSC52266.2021.9715360)

### Acknowledgment

This work is financed by [EOSC-Synergy](https://www.eosc-synergy.eu/) project (EU H2020 RI Grant No 857647), but it is also currently supported by human and computational resources under the [EOSC](https://www.eosc-portal.eu/) umbrella (specially [EGI](https://www.egi.eu), [GEANT](https://geant.org) ) and the [members](http://lagoproject.net/collab.html) of the LAGO Collaboration.

## Description

LAGO onedataSim packets all requeriments for runnig [ARTI](https://github.com/lagoproject/arti) into a Docker container, giving researcher the advantage of obtaining results on any plataform that supports Docker (Linux, Windows and MacOs on personal computers, HTC/HPC clusters or cloud plublic/private providers).

However, the main objective of onedataSim is to standardise the simulation and its analisys in [LAGO Collaboration](http://lagoproject.net) in order to curate, re-use and publish the results, following the [Data Management Plan (DPM)](https://lagoproject.github.io/DMP/) established. For this purpose, onedataSim includes two main programs:

1. **``do_sims_onedata.py``** that:
  - executes simulations as ``do_sims.sh``, exactly with same parameters;
  - caches partial results as local scratch and then copies them to the official [LAGO repository](https://datahub.egi.eu) based on [OneData](https://github.com/onedata);
  - makes standardised metadata for every inputs and results and includes them as extended attributes in OneData filesystem.
2. **``do_showers_onedata.py``** that:
  - executes analysis as ``do_showers.sh`` does.
  - caches the selected simulation to be analisyed in local from the official [LAGO repository](https://datahub.egi.eu) and then stores again the results to the repository;
  - makes also standardised metadata for these results and updates the corresponding catalog on OneData.

Storing results on the official repository with standardised metadata enables:
  - sharing results with other LAGO members;
  - future searches and publishing through institutional/goverment catalog providers and virtual observatories such as the [B2FIND](https://b2find.eudat.eu/group/lago);
  - properly citing scientific data and diseminating results through internet through Handle.net' PiDs;
  - building new results based on data minig or big data techniques thanks to linked metadata.

Therefore, we encourage LAGO researchers to use these programs for their simulations.

## Pre-requisites

1. Be acredited in [LAGO Virtual Organisation](https://lagoproject.github.io/DMP/docs/howtos/how_to_join_LAGO_VO/) to obtain a OneData personal [token.](https://lagoproject.github.io/DMP/docs/howtos/how_to_login_into_OneData/).

2. Had [Docker](https://www.docker.com/) (or [Singularity](https://singularity.lbl.gov/) or [udocker](https://pypi.org/project/udocker/)) installed on your PC (or HPC/HTC facility).

It is only needed [Docker Engine](https://docs.docker.com/engine/install/) to run onedataSim container, this is, the *SERVER* mode. However, the *DESKTOP* mode is the only available for Windows and MacOs, it includes the Docker Engine but also more functionalities.

On linux, the recommended way is to remove all docker packages included by default in your distro and to make use of Docker repositories.

For example, for a old Debian based distribution such as Ubuntu:
```sh
  sudo apt-get remove docker wmdocker docker-registry [...etc...]
  curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
  sudo add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/debian"
  sudo apt-get install docker-ce docker-ce-cli containerd.io
```

On an newly Debian release with the last Docker:

```sh
  sudo apt-get update
  sudo apt-get install -y docker.io
```

On CentOS 7 with root:

```sh
  yum remove docker docker-client docker-[...etc...]
  # check first if centos7-extras is enabled
  yum update
  yum install -y yum-utils
  yum-config-manager  --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
  yum update
  yum install docker-ce docker-ce-cli containerd.io
  systemctl enable docker
  systemctl start docker
```

## Downloading the official docker images to run onedataSim

onedataSim, ARTI and required software (CORSIKA, GEANT4, ROOT) are built, tested and packed into Docker images, following a in a [CI/CD fashion](https://jenkins.eosc-synergy.eu/job/eosc-synergy-org/job/onedataSim/). When whole steps of the CI/CD pipeline are sucesfully completed, the images are certified and stored in the space of LAGO Collaboration at [Docker-Hub](https://hub.docker.com/u/lagocollaboration). The process assures the quality of the software published.

Depending on the type of data that you want generate and/or processs (i.e. [S0, S1, S2](https://lagoproject.github.io/DMP/DMP/#types-and-formats-of-generatedcollected-data)), you should pull different image, because their size.

- **``onedatasim-s0``** is mainly for generate S0 datasets (simulations with ``do_sims_onedata.py``), but also allows S1 analysis. Therefore it includes the modified CORSIKA for LAGO, which it results in a heavy image (~911.7 MB).
- **``onedatasim-s1``** is only for generate S1 datasets (analysis with ``do_showers_onedata.py``), but the image is smaller (currently, ~473.29 MB).
- ( Future: ``onedatasim-s2`` will be mainly for generate S2 datasets (detector response). It will include GEANt4/ROOT, and consequently, heaviest (~ 1GB)).

```sh
sudo docker pull lagocollaboration/onedatasim-s0:dev
```

```sh
sudo docker pull lagocollaboration/onedatasim-s1:dev
```

(Currently for our DockerHub space, downloads are limited to 100/day per IP. If you are many nodes under a NAT, you should consider distributing internally the docker image through ``docker save`` and ``load commands``).

## Executing a stardandised simulation & analisys to be stored in OneData repositories for LAGO

This automatised execution is the preferred one in LAGO collaboration.

You can execute ``do_sims_onedata.py`` or ``do_showers_onedata.py`` in a single command, without the needed of log into the container. If there is a lack of paramenters, it prompts you for them, if not this starts and the current progress is shown while the results are automatically stored in OneData.

```sh
export TOKEN="<personal OneData token (oneclient enabled)>"
export ONEPROVIDER="<nearest OneData provider>"

sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN=$TOKEN \
                -e ONECLIENT_PROVIDER_HOST=$ONEPROVIDER \
                -it <container name> bash -lc "do_*_onedata.py <ARTI do_* params>"
```

### Running simulations (generating S0 data)

1. Export credentials:

```sh
export TOKEN="MDAxY...LAo"
export ONEPROVIDER="ceta-ciemat-01.datahub.egi.eu"
```

2. Showing parameters:

```sh
sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN=$TOKEN \
                -e ONECLIENT_PROVIDER_HOST=$ONEPROVIDER \
                -it lagocollaboration/onedatasim-s0:dev  bash -lc "do_sims_onedata.py -?"
```

3. Simple simulation example:

```sh
sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN=$TOKEN \
                -e ONECLIENT_PROVIDER_HOST=$ONEPROVIDER \
                -it lagocollaboration/onedatasim-s0:dev  bash -lc "do_sims_onedata.py -t 10 -u 0000-0001-6497-753X -s and -k 2.0e2 -h QGSII -x"
```

3. Executing on a multi-processor server.

If you count on an standalone server for computing or a virtual machine instantiated with enough procesors memory and disk, you only need add the **-j \<procs\>** param to enable multi-processing:

```sh
sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN=$TOKEN \
                -e ONECLIENT_PROVIDER_HOST=$ONEPROVIDER \
                -it <container name> bash -lc "do_sims_onedata.py <other ARTI do_* params> -j <procs>"
```

### Analysing S0 datasets (generating S1 data)

1. Export credentials

```sh
export TOKEN="MDAxY...LAo"
export ONEPROVIDER="ceta-ciemat-01.datahub.egi.eu"
```

2. Showing parameters:

```sh
sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN=$TOKEN \
                -e ONECLIENT_PROVIDER_HOST=$ONEPROVIDER \
                -it lagocollaboration/onedatasim-s1:dev  bash -lc "do_showers_onedata.py -?"
```

3. Executing an analysis:

```sh
sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN=$TOKEN \
                -e ONECLIENT_PROVIDER_HOST=$ONEPROVIDER \
                -it <container name> bash -lc "do_showers_onedata.py -o XXXX  -u 0000-0001-6497-753X"
```

## Advanced use cases

### Executing on HTC clusters

If you has enough permissions (sudo) to run Docker in privileged mode on a cluster and get the computing nodes in exclusive mode, you can run many simulations at time.

For example on the Slurm batch systems.

```sh
sudo docker pull lagocollaboration/onedatasim-s0:dev
sudo docker save -o <shared dir>/onedatasim-s0.tar onedatasim-s0:dev
export TOKEN="<personal OneData token (oneclient enabled)>"
export ONEPROVIDER="<nearest OneData provider>"
sbatch simulation.sbatch
```

```sh
#!/bin/bash
#SBATCH --export=ALL
#SBATCH --exclusive
#SBATCH-o %j.log
sudo docker stop $(docker ps -aq)
sudo docker rm $(docker ps -aq)
sudo docker load -i -o  /home/cloudadm/onedatasim-s0.tar
sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN=$TOKEN \
                -e ONECLIENT_PROVIDER_HOST=$ONEPROVIDER \
                -it onedatasim-s0:dev bash -lc "do_*_onedata.py <ARTI do_* params>"
```

### Executing on clusters instantiated by oneself in IaaS cloud providers

1. First you has to create and configure a cluster in the cloud:
   - Using the EOSC public cloud, that enables the pre-configuration of Slurm and other schedulers (Kubernetes). [See EOSC-Synergy training for LAGO](https://moodle.learn.eosc-synergy.eu/course/view.php?id=16)
   - Using commercial public clouds (Amazon, Azure, Google, etc).
   - Using private clouds (institutional orchestators as OpenStack, OpenNebula, XenServer, VMware, etc).
2.  Example for an Slurm instantiated on EOSC resources (pre-configured by IM):
   You can access to head node through SSH, using ``cloudadm`` account, but then you can gain root privileges with ``sudo``. Slurm and a directory shared by NFS are already configured (/home), but some configruation has to be done: to share the users' directories and to install spackages needed for Docker:

```sh
sudo mkdir /home/cloudadm
sudo chown cloudadm /home/cloudadm
sudo docker pull lagocollaboration/onedatasim-s0:dev
sudo docker save -o /home/cloudadm/onedatasim-s0.tar lagocollaboration/onedatasim-s0:dev
```

Then, you can launch simulations through ``sbatch``. The environment varialbles will be exported to execution nodes. Thus:

```sh
export TOKEN="MDAxY...LAo"
export ONEPROVIDER="ceta-ciemat-01.datahub.egi.eu"
cd /home/cloudadm
sbatch simulation.sbatch
```

A simulation.sbatch file for testing functionality can be one that will write the allowed parameters in <job number>.log:

```sh
#!/bin/bash
#SBATCH --export=ALL
#SBATCH --exclusive
#SBATCH-o %j.log
date
hostname
sudo apt-get -y update
sudo apt-get install -y docker.io
sudo docker stop $(docker ps -aq)
sudo docker rm $(docker ps -aq)
sudo docker load -i -o  /home/cloudadm/onedatasim-s0.tar
sudo docker run --privileged -e ONECLIENT_ACCESS_TOKEN=$TOKEN -e ONECLIENT_PROVIDER_HOST=$ONEPROVIDER -i onedatasim-s0:dev bash -lc "do_sims_onedata.py -?"
```

## Instructions only for developers

### Building the onedataSim container

Every container has different requrirements. To build the ``onedatasim-s0`` container is needed to provide as parameter an official ``lago-corsika`` image as base installation. This is so because ARTI simulations currently call [CORSIKA 7](https://www.ikp.kit.edu/corsika/79.php), which source code is licensed only for the internal use of LAGO collaborators. On the other hand, ``onedatasim-s2`` requires GEANT4/Root, and other official images must be used.

On the other hand, other parameters allow choosing ARTI and onedataSim branches, which is fundamental for developing.

#### Example: building images from default branches (currently "dev")

You must indicate the BASE_OS parameter if you want creating S0 or S2 images:

```sh
sudo docker build --build-arg BASE_OS="lagocollaboration/lago-corsika:77402" \
                  -t onedatasim-s1:local-test https://github.com/lagoproject/onedatasim.git
```
```sh
sudo docker build -t onedatasim-s1:local-test https://github.com/lagoproject/onedatasim.git
```
```sh
sudo docker build --build-arg BASE_OS="lagocollaboration/geant4:TBD" \
                  -t onedatasim-s2:local-test https://github.com/lagoproject/onedatasim.git
```

#### Example: building ``onedatasim-s0`` from featured branches

If you have the newer releases of *git* installed in your machine, you can build the container with one command. Note that afther the *.git* link, there hare an '#' followed of again the ONEDATASIM_BRANCH name.

```sh
sudo docker build --build-arg ONEDATASIM_BRANCH="dev-ajrubio-montero" \
                  --build-arg ARTI_BRANCH="dev-asoreyh" \
                  --build-arg BASE_OS="lagocollaboration/lago-corsika:77402-dev"
                  -t onedatasim-s0:dev-ajrubio-montero \
                  https://github.com/lagoproject/onedatasim.git#dev-ajrubio-montero
```

### Logging into container for developing purposes

1. Runing scripts & attaching a local directory at login.
   To log into the container only has to run bash without parameters, positioned alwasy at the end of the command. Additionally, You can mount a local directory inside the container the with the parameter **--volume \<local path\>:\<container path\>**. For example:
```sh
 [pepe@mypc tmp]# ls /home/pepe/workspace
 onedataSim  samples geant4-dev
 [pepe@mypc tmp]# sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN="MDAxY2xv...iXm8jowGgo" \
           -e ONECLIENT_PROVIDER_HOST="mon01-tic.ciemat.es" \
           --volume /home/pepe/workspace:/root -it lagocontainer:0.0.1  bash
 [root@c42dc622f7eb run]# ls /root
 onedataSim  samples geant4-dev
```
2. Explore OneData repository within the container.
   Firstly test if the repository is already mounted and force mount if necessary:
```sh
[root@c42dc622f7eb run]# ls -alh /mnt/datahub.egi.eu
[root@c42dc622f7eb run]# ls -alh /mnt/datahub.egi.eu/LAGOsim
total 0
drwxrwxr-x 1 root    root   0 Sep 17 13:52 .
drwxrwxr-x 1 root    root   0 Sep 15 08:47 ..
[root@c42dc622f7eb run]# oneclient -- force-proxy-io /mnt/datahub.egi.eu
Connecting to provider 'mon01-tic.ciemat.es:443' using session ID: '4998286443844254461'...
Getting configuration...
Oneclient has been successfully mounted in '/mnt/datahub.egi.eu'.
```

   Then, you can explore the repository:
```sh
[root@c42dc622f7eb run]# ls -alh /mnt/datahub.egi.eu
total 0
drwxr-xr-x 1 root root  0 Sep 15 08:46 .
drwxr-xr-x 1 root root 29 Sep 17 15:10 ..
drwxrwxr-x 1 root root  0 Jun 16 13:23 PLAYGROUND
drwxrwxr-x 1 root root  0 Jun 16 13:23 notebooks-training
drwxrwxr-x 1 root root  0 Sep 15 08:47 LAGOsim
[root@c42dc622f7eb run]# ls -alh /mnt/datahub.egi.eu/LAGOsim
total 0
drwxrwxr-x 1 1034995 638198 0 Sep 17 13:52 .
drwxrwxr-x 1 root    root   0 Sep 15 08:47 ..
drwxr-xr-x 1 1034995 638198 0 Sep  7 18:41 S0_sac_10_100.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 13 12:59 S0_sac_10_110.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 13 13:04 S0_sac_10_120.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 13 13:05 S0_sac_10_130.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 13 13:06 S0_sac_10_140.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 13 13:11 S0_sac_10_150.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 13 16:21 S0_sac_10_200.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 14 15:28 S0_sac_10_300.0_75600_QGSII_flat
drwxr-xr-x 1  398931 638198 0 Sep 17 13:41 S0_sac_10_500.0_75600_QGSII_flat
drwxr-xr-x 1  398931 638198 0 Sep 17 13:52 S0_sac_10_600.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep  8 12:30 S0_sac_1_100.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 13 16:17 S0_sac_60_200.0_75600_QGSII_flat
...
...
```

### Storing data on testing spaces based on OneData

You can use testing spaces such as ``test8`` to store testing runs during development. For this purpose you should the suitable OneData provider and use the the ``--onedata_path`` parameter to select the correct path.

For ``test8``, you should choose ceta-ciemat-**02**.datahub.egi.eu and any directory <dir> under the ``--onedata_path /mnt/datahub.egi.eu/test8/<dir>`` path:

```sh
export TOKEN="MDAxY...LAo"
export ONEPROVIDER="ceta-ciemat-02.datahub.egi.eu"

[pepe@mypc tmp]# sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN="$TOKEN" \
            -e ONECLIENT_PROVIDER_HOST="$ONEPROVIDER" \
            -it lagocollaboration/onedatasim-s0:dev bash

[root@9db2578a3e28 run]# do_sims_onedata.py -t 13 -u 0000-0001-6497-753X -s and -k 2.0e2 -h QGSII -x --onedata_path /mnt/datahub.egi.eu/test8/LAGOSIM_test_20220210 -j 4

```
