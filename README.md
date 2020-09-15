# LAGO onedataSim : packed tools for [ARTI](https://github.com/lagoproject/arti) simulation and analisys on [OneData](https://github.com/onedata)

## Description

LAGO onedataSim packets all requeriments for runnig [ARTI](https://github.com/lagoproject/arti) into a Docker container, giving researcher the advantage of obtaining results on any plataform that supports Docker (Linux, Windows and MacOs on personal computers, HTC/HPC clusters or cloud plublic/private providers).

However, the main objective of onedataSim is to standardise the simulation and its analisys in [LAGO Collaboration](http://lagoproject.net) in order to curate, re-use and publish the results, following the [Data Management Plant (DPM)](https://github.com/lagoproject/arti) established. For this purpose, onedataSim includes two main programs:

1. do_sims_onedata.py that:
  - executes simulations as do_sims.sh, exactly with same parameters;
  - caches partial results as local scratch and then copies them to the official LAGO repository based on [OneData](https://github.com/onedata);
  - makes standardised metadata for every inputs and results and includes them as extended attributes in OneData filesystem. 
2. do_analysis_onedata.py that:
  - executes analysis as do_analysis.sh does.
  - caches the selected simulation to be analisyed in local and then store results at the official LAGO repository on [OneData](https://github.com/onedata);
  - makes also standardised metadata for these results and updates the corresponding catalog on OneData.

Storing results on the official repository with standardised metadata enables:
  - sharing results with other LAGO members; 
  - future searches and publishing through institutional/goverment catalog providers and virtual observatories; 
  - properly citing scientific data and diseminating results through internet; 
  - building new results based on data minig or big data techniques thanks to linked metadata.

Therefore, we encourage LAGO researchers to use these programs for their simulations, but 

## Pre-requisites

1. Be acredited in LAGO Virtual Organisation to obtain a OneData personal token.

2. Had Docker (or Singularity) installed on your PC (or HPC/HTC facility) 



## Building the onedataSim container

To build the container is needed had a OneData token and to indicate any provider enroled as LAGO repository. This is so because ARTI currently calls [CORSIKA 7](https://www.ikp.kit.edu/corsika/79.php), which is licensed only for internal use of LAGO collaborators. As this software is stored at LAGO repository with closed permisions, its download requires to previously check if the user belogns to LAGO Virtual Organisation. 


```
sudo docker build --no-cache --build-arg ONECLIENT_ACCESS_TOKEN_TO_BUILD="<personal OneData token>" --build-arg ONECLIENT_PROVIDER_HOST_TO_BUILD="<nearest OneData provider>" -t  <container name> https://github.com/lagoproject/onedataSim.git
```
```
sudo docker build --no-cache --build-arg ONECLIENT_ACCESS_TOKEN_TO_BUILD="MDAxY2xvYwF00aW9uIGRhdG6odWIuZWdpLmV1CjAwMzZpZGVudGlmaWVyIDdiY2IwZGQzY2I00MmFjY2FmOGZiOTBmZjkzMTUxNTkyY2gyYzVlCjAwMWFjaWQgdGltZSA8IDE2MjMzMjA4MzAKMDAyZnNpZ25hdHVyZSAvZQrzvw2OtjS8bOtDgoOaRRvv18ZhXE4PTG2tcsgwYgo" --build-arg ONECLIENT_PROVIDER_HOST_TO_BUILD="https://mon01-tic.ciemat.es" -t lagocontainer:0.0.1  https://github.com/lagoproject/onedataSim.git
```
## Executing a stardandised simulation & analisys to be stored in OneData repositories for LAGO

This automatised execution is the preferred one in LAGO collaboration.

You can execute do_sims_onedata.py or do_analysis_onedata.py in a single command, without the needed of log into the container. If there is a lack of paramenters, it promps you for them, if not this starts and the current progress is shown while the results are automatically stored in OneData. 

1. Simple command example:

```
sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN="<personal onedata token>" -e ONECLIENT_PROVIDER_HOST="<nearest onedata provider>" -it <container name> bash -lc "do_sims_onedata.py <ARTI do_* params>"
```

```
sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN="MDAxY2xvYwF00aW9uIGRhdG6odWIuZWdpLmV1CjAwMzZpZGVudGlmaWVyIDdiY2IwZGQzY2I00MmFjY2FmOGZiOTBmZjkzMTUxNTkyY2gyYzVlCjAwMWFjaWQgdGltZSA8IDE2MjMzMjA4MzAKMDAyZnNpZ25hdHVyZSAvZQrzvw2OtjS8bOtDgoOaRRvv18ZhXE4PTG2tcsgwYgo" -e ONECLIENT_PROVIDER_HOST="mon01-tic.ciemat.es" -it lagocontainer:0.0.1  bash -lc "do_sims_onedata.py -t 10 -u 0000-0001-6497-753X -s sac -k 2.0e2 -h QGSII"
```

2. Executing on a multi-processor server

If you count on an standalone server for computing or a virtual machine instantiated with enough procesors memory and disk, you only need add the "-j <procs>" param to enable multi-processing:

```
sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN="<personal onedata token>" -e ONECLIENT_PROVIDER_HOST="<nearest onedata provider>" -it <container name> bash -lc "do_sims_onedata.py -j <procs> <other ARTI do_* params>"
```


## Advanced use cases

1. Executing on HTC clusters

2. Executing on resurces instantiated by IaaS public/private cloud providers

3. Executing on Kubernettes


## Logging into container for developing purposes

1. Run scripts.

2. Attach a local directory

3. Explore OneData reposotory


## Acknowledgment 

This work is financed by [EOSC-Synergy](https://www.eosc-synergy.eu/) project (EU H2020 RI Grant No 857647), but it is also currently supported by human and computational resources under the [EOSC](https://www.eosc-portal.eu/) umbrella (specially [EGI](https://www.egi.eu), [GEANT](https://geant.org) ) and the [members](http://lagoproject.net/collab.html) of the LAGO Collaboration.








