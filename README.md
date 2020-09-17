# LAGO onedataSim : packed tools for [ARTI](https://github.com/lagoproject/arti) simulation and analisys on [OneData](https://github.com/onedata)

## Description

LAGO onedataSim packets all requeriments for runnig [ARTI](https://github.com/lagoproject/arti) into a Docker container, giving researcher the advantage of obtaining results on any plataform that supports Docker (Linux, Windows and MacOs on personal computers, HTC/HPC clusters or cloud plublic/private providers).

However, the main objective of onedataSim is to standardise the simulation and its analisys in [LAGO Collaboration](http://lagoproject.net) in order to curate, re-use and publish the results, following the [Data Management Plant (DPM)](https://github.com/lagoproject/arti) established. For this purpose, onedataSim includes two main programs:

1. **do_sims_onedata.py** that:
  - executes simulations as do_sims.sh, exactly with same parameters;
  - caches partial results as local scratch and then copies them to the official LAGO repository based on [OneData](https://github.com/onedata);
  - makes standardised metadata for every inputs and results and includes them as extended attributes in OneData filesystem. 
2. **do_analysis_onedata.py** that:
  - executes analysis as do_analysis.sh does.
  - caches the selected simulation to be analisyed in local and then store results at the official LAGO repository on [OneData](https://github.com/onedata);
  - makes also standardised metadata for these results and updates the corresponding catalog on OneData.

Storing results on the official repository with standardised metadata enables:
  - sharing results with other LAGO members; 
  - future searches and publishing through institutional/goverment catalog providers and virtual observatories; 
  - properly citing scientific data and diseminating results through internet; 
  - building new results based on data minig or big data techniques thanks to linked metadata.

Therefore, we encourage LAGO researchers to use these programs for their simulations. 

## Pre-requisites

1. Be acredited in LAGO Virtual Organisation to obtain a OneData personal token.

2. Had [Docker](https://www.docker.com/) (or [Singularity](https://singularity.lbl.gov/) or [udocker](https://pypi.org/project/udocker/)) installed on your PC (or HPC/HTC facility) 

It is only needed [Docker Engine](https://docs.docker.com/engine/install/) to run onedataSim container, this is, the *SERVER* mode. However, the *DESKTOP* mode is the only available for Windows and MacOs, it includes the Docker Engine but also more functionalities.  

On linux, the recommended way is to remove all docker packages included by default in your distro and to make use of Docker repositories.

For example, for a Debian based distribution such as Ubuntu:
```sh
  sudo apt-get remove docker wmdocker docker-registry [...etc...]
  curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
  sudo add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/debian"
  sudo apt-get install docker-ce docker-ce-cli containerd.io
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



## Building the onedataSim container

To build the container is needed had a OneData token and to indicate any provider enroled as LAGO repository. This is so because ARTI currently calls [CORSIKA 7](https://www.ikp.kit.edu/corsika/79.php), which is licensed only for internal use of LAGO collaborators. As this software is stored at LAGO repository with closed permisions, its download requires to previously check if the user belongs to LAGO Virtual Organisation. 

If you have the newer releases of *git*, you can build the container with one command:

```sh
sudo docker build --no-cache --build-arg ONECLIENT_ACCESS_TOKEN_TO_BUILD="<personal OneData token>" \ 
                  --build-arg ONECLIENT_PROVIDER_HOST_TO_BUILD="<nearest OneData provider>" \
                  -t  <container name> https://github.com/lagoproject/onedataSim.git
```

If not, you should download first the Dockerfile

```sh
wget https://raw.githubusercontent.com/lagoproject/onedataSim/master/Dockerfile
sudo docker build --no-cache --build-arg ONECLIENT_ACCESS_TOKEN_TO_BUILD="<personal OneData token>" \ 
                  --build-arg ONECLIENT_PROVIDER_HOST_TO_BUILD="<nearest OneData provider>" \
                  -t  <container name> - < ./Dockerfile
```


As an example:

```sh
sudo docker build --no-cache --build-arg ONECLIENT_ACCESS_TOKEN_TO_BUILD="MDAxY2xv...iXm8jowGgo" \
                  --build-arg ONECLIENT_PROVIDER_HOST_TO_BUILD="https://mon01-tic.ciemat.es" \
                  -t lagocontainer:0.0.1  https://github.com/lagoproject/onedataSim.git
```




## Executing a stardandised simulation & analisys to be stored in OneData repositories for LAGO

This automatised execution is the preferred one in LAGO collaboration.

You can execute do_sims_onedata.py or do_analysis_onedata.py in a single command, without the needed of log into the container. If there is a lack of paramenters, it prompts you for them, if not this starts and the current progress is shown while the results are automatically stored in OneData. 

1. Simple command example:

```sh
sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN="<personal onedata token>" \
                -e ONECLIENT_PROVIDER_HOST="<nearest onedata provider>" \ 
                -it <container name> bash -lc "do_sims_onedata.py <ARTI do_* params>"
```

```sh
sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN="MDAxY2xv...iXm8jowGgo" \
                -e ONECLIENT_PROVIDER_HOST="mon01-tic.ciemat.es" \
                -it lagocontainer:0.0.1  bash -lc "do_sims_onedata.py -t 10 -u 0000-0001-6497-753X -s sac -k 2.0e2 -h QGSII"
```

2. Executing on a multi-processor server

If you count on an standalone server for computing or a virtual machine instantiated with enough procesors memory and disk, you only need add the **-j \<procs\>** param to enable multi-processing:

```sh
sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN="<personal onedata token>" \
                -e ONECLIENT_PROVIDER_HOST="<nearest onedata provider>" \
                -it <container name> bash -lc "do_sims_onedata.py -j <procs> <other ARTI do_* params>"
```


## Advanced use cases

1. Executing on HTC clusters

2. Executing on resurces instantiated by IaaS public/private cloud providers

3. Executing on Kubernettes


## Logging into container for developing purposes

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

```sh
[root@c42dc622f7eb run]# oneclient /mnt
Connecting to provider 'mon01-tic.ciemat.es:443' using session ID: '4998286443844254461'...
Getting configuration...
Oneclient has been successfully mounted in '/mnt'.
[root@c42dc622f7eb run]# ls -alh /mnt/
total 0
drwxr-xr-x 1 root root  0 Sep 15 08:46 .
drwxr-xr-x 1 root root 29 Sep 17 15:10 ..
drwxrwxr-x 1 root root  0 Jun 16 13:23 PLAYGROUND
drwxrwxr-x 1 root root  0 Jun 16 13:23 notebooks-training
drwxrwxr-x 1 root root  0 Sep 15 08:47 LAGOsim
[root@c42dc622f7eb run]# ls -alh /mnt/LAGOsim
total 0
drwxrwxr-x 1 1034995 638198 0 Sep 17 13:52 .
drwxrwxr-x 1 root    root   0 Sep 15 08:47 ..
drwxr-xr-x 1 1034995 638198 0 Sep  7 18:41 sac_10_100.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 13 12:59 sac_10_110.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 13 13:04 sac_10_120.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 13 13:05 sac_10_130.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 13 13:06 sac_10_140.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 13 13:11 sac_10_150.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 13 16:21 sac_10_200.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 14 15:28 sac_10_300.0_75600_QGSII_flat
drwxr-xr-x 1  398931 638198 0 Sep 17 13:41 sac_10_500.0_75600_QGSII_flat
drwxr-xr-x 1  398931 638198 0 Sep 17 13:52 sac_10_600.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep  8 12:30 sac_1_100.0_75600_QGSII_flat
drwxr-xr-x 1 1034995 638198 0 Sep 13 16:17 sac_60_200.0_75600_QGSII_flat
...
...
```



## Acknowledgment 

This work is financed by [EOSC-Synergy](https://www.eosc-synergy.eu/) project (EU H2020 RI Grant No 857647), but it is also currently supported by human and computational resources under the [EOSC](https://www.eosc-portal.eu/) umbrella (specially [EGI](https://www.egi.eu), [GEANT](https://geant.org) ) and the [members](http://lagoproject.net/collab.html) of the LAGO Collaboration.








