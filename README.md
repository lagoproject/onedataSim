# LAGO onedataSim : packed tools for [ARTI](../arti) simulation and analisys on [OneData](https://github.com/onedata)

## Description

LAGO onedataSim packets all requeriments for runnig [ARTI](../arti) into a Docker container, giving researcher the advantage of obtaining results on any plataform that supports Docker (Linux, Windows and MacOs on personal computers, HTC/HPC clusters or cloud plublic/private providers).

However, the main objective of onedataSim is to standardise the simulation and its analisys in [LAGO Collaboration](http://lagoproject.net) in order to curate, re-use and publish the results. 



## Build and execute the onedataSim container
1. Build the container
```
sudo docker build --no-cache --build-arg ONECLIENT_ACCESS_TOKEN_TO_BUILD="<personal onedata token>" --build-arg ONECLIENT_PROVIDER_HOST_TO_BUILD="<nearest onedata provider>" -t  <container name> https://github.com/lagoproject/onedataSim.git
```
```
sudo docker build --no-cache --build-arg ONECLIENT_ACCESS_TOKEN_TO_BUILD="MDAxY2xvYwF00aW9uIGRhdG6odWIuZWdpLmV1CjAwMzZpZGVudGlmaWVyIDdiY2IwZGQzY2I00MmFjY2FmOGZiOTBmZjkzMTUxNTkyY2gyYzVlCjAwMWFjaWQgdGltZSA8IDE2MjMzMjA4MzAKMDAyZnNpZ25hdHVyZSAvZQrzvw2OtjS8bOtDgoOaRRvv18ZhXE4PTG2tcsgwYgo" --build-arg ONECLIENT_PROVIDER_HOST_TO_BUILD="https://mon01-tic.ciemat.es" -t lagocontainer:0.0.1  https://github.com/lagoproject/onedataSim.git
```
2. Execute a stardandised simulation to be estored in OneData repositories for LAGO
```
sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN="<personal onedata token>" -e ONECLIENT_PROVIDER_HOST="<nearest onedata provider>" -it <container name> bash -lc "do_onedata.py <ARTI do_* params>"
```
```
  sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN="MDAxY2xvYwF00aW9uIGRhdG6odWIuZWdpLmV1CjAwMzZpZGVudGlmaWVyIDdiY2IwZGQzY2I00MmFjY2FmOGZiOTBmZjkzMTUxNTkyY2gyYzVlCjAwMWFjaWQgdGltZSA8IDE2MjMzMjA4MzAKMDAyZnNpZ25hdHVyZSAvZQrzvw2OtjS8bOtDgoOaRRvv18ZhXE4PTG2tcsgwYgo" -e ONECLIENT_PROVIDER_HOST="mon01-tic.ciemat.es" -it lagocontainer:0.0.1  bash -lc "do_onedata.py -t 10 -u 0000-0001-6497-753X -s sac -k 2.0e2 -h QGSII"
```
