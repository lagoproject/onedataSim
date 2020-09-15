# LAGO onedataSim : packed tools for [ARTI](https://github.com/lagoproject/arti) simulation and analisys on [OneData](https://github.com/onedata)

## Description

LAGO onedataSim packets all requeriments for runnig [ARTI](https://github.com/lagoproject/arti) into a Docker container, giving researcher the advantage of obtaining results on any plataform that supports Docker (Linux, Windows and MacOs on personal computers, HTC/HPC clusters or cloud plublic/private providers).

However, the main objective of onedataSim is to standardise the simulation and its analisys in [LAGO Collaboration](http://lagoproject.net) in order to curate, re-use and publish the results, following the [Data Management Plant (DPM)](https://github.com/lagoproject/arti) established. For this purpose, onedataSim includes two main programs:

1. do_sims_onedata.py that:
  1. executes simulations as do_sims.sh, exactly with same parameters;
  2. caches partial results as local scratch and then copies them to the official LAGO repository based on [OneData](https://github.com/onedata);
  3. makes standardised metadata for every inputs and results and includes them as extended attributes in OneData filesystem. 
2. do_analysis_onedata.py that:
  1. executes analysis as do_analysis.sh does.
  2. caches the selected simulation to be analisyed in local and then store results at the official LAGO repository on [OneData](https://github.com/onedata);
  3. makes also standardised metadata for these results and updates the corresponding catalog on OneData.

Storing results on the official repository with standardised metadata enables:
  1. sharing results with other LAGO members; 
  2. future searches and publishing through institutional/goverment catalog providers and virtual observatories; 
  2  properly citing scientific data and diseminating results through internet; 
  3. building new results based on data minig or big data techniques thanks to linked metadata.

Therefore, we encourage LAGO researchers to use these programs for their simulations, but 

## Pre-requisites

1. Be acredited in LAGO Virtual Organisation to obtain a OneData personal token.

2. Had Docker (or Singularity) installed on your PC (or HPC/HTC facility) 



## Build and execute the onedataSim container
1. Build the container
```
sudo docker build --no-cache --build-arg ONECLIENT_ACCESS_TOKEN_TO_BUILD="<personal onedata token>" --build-arg ONECLIENT_PROVIDER_HOST_TO_BUILD="<nearest onedata provider>" -t  <container name> https://github.com/lagoproject/onedataSim.git
```
```
sudo docker build --no-cache --build-arg ONECLIENT_ACCESS_TOKEN_TO_BUILD="MDAxY2xvYwF00aW9uIGRhdG6odWIuZWdpLmV1CjAwMzZpZGVudGlmaWVyIDdiY2IwZGQzY2I00MmFjY2FmOGZiOTBmZjkzMTUxNTkyY2gyYzVlCjAwMWFjaWQgdGltZSA8IDE2MjMzMjA4MzAKMDAyZnNpZ25hdHVyZSAvZQrzvw2OtjS8bOtDgoOaRRvv18ZhXE4PTG2tcsgwYgo" --build-arg ONECLIENT_PROVIDER_HOST_TO_BUILD="https://mon01-tic.ciemat.es" -t lagocontainer:0.0.1  https://github.com/lagoproject/onedataSim.git
```
2. Execute a stardandised simulation to be stored in OneData repositories for LAGO
```
sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN="<personal onedata token>" -e ONECLIENT_PROVIDER_HOST="<nearest onedata provider>" -it <container name> bash -lc "do_onedata.py <ARTI do_* params>"
```
```
  sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN="MDAxY2xvYwF00aW9uIGRhdG6odWIuZWdpLmV1CjAwMzZpZGVudGlmaWVyIDdiY2IwZGQzY2I00MmFjY2FmOGZiOTBmZjkzMTUxNTkyY2gyYzVlCjAwMWFjaWQgdGltZSA8IDE2MjMzMjA4MzAKMDAyZnNpZ25hdHVyZSAvZQrzvw2OtjS8bOtDgoOaRRvv18ZhXE4PTG2tcsgwYgo" -e ONECLIENT_PROVIDER_HOST="mon01-tic.ciemat.es" -it lagocontainer:0.0.1  bash -lc "do_onedata.py -t 10 -u 0000-0001-6497-753X -s sac -k 2.0e2 -h QGSII"
```
