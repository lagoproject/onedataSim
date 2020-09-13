# onedataSim : packed tools for [ARTI](../arti) simulation and analisys on [OneData](https://github.com/onedata)

## Build and execute the onedataSim container

1. Build the container
```
sudo docker build --no-cache --build-arg ONECLIENT_ACCESS_TOKEN_TO_BUILD="<personal onedata token>" --build-arg ONECLIENT_PROVIDER_HOST_TO_BUILD="<nearest onedata provider>" -t  <container name> -f docker/Dockerfile https://github.com/lagoproject/onedataSim.git
```
  ```
  sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN="<personal onedata token>" -e ONECLIENT_PROVIDER_HOST="<nearest onedata provider>" -it <container name> bash -lc "do_onedata.py <ARTI do_* params>"
```


2. Execute a simulation
```
sudo docker build --no-cache --build-arg ONECLIENT_ACCESS_TOKEN_TO_BUILD="MDAxY2xvYwF00aW9uIGRhdG6odWIuZWdpLmV1CjAwMzZpZGVudGlmaWVyIDdiY2IwZGQzY2I00MmFjY2FmOGZiOTBmZjkzMTUxNTkyY2gyYzVlCjAwMWFjaWQgdGltZSA8IDE2MjMzMjA4MzAKMDAyZnNpZ25hdHVyZSAvZQrzvw2OtjS8bOtDgoOaRRvv18ZhXE4PTG2tcsgwYgo" --build-arg ONECLIENT_PROVIDER_HOST_TO_BUILD="https://mon01-tic.ciemat.es" -t lagocontainer:0.0.1 - < -f docker/Dockerfile https://github.com/lagoproject/onedataSim.git
```

```
  sudo docker run --privileged  -e  ONECLIENT_ACCESS_TOKEN="MDAxY2xvYwF00aW9uIGRhdG6odWIuZWdpLmV1CjAwMzZpZGVudGlmaWVyIDdiY2IwZGQzY2I00MmFjY2FmOGZiOTBmZjkzMTUxNTkyY2gyYzVlCjAwMWFjaWQgdGltZSA8IDE2MjMzMjA4MzAKMDAyZnNpZ25hdHVyZSAvZQrzvw2OtjS8bOtDgoOaRRvv18ZhXE4PTG2tcsgwYgo" -e ONECLIENT_PROVIDER_HOST="mon01-tic.ciemat.es" -it lagocontainer:0.0.1  bash -lc "do_onedata.py -t 10 -u 0000-0001-6497-753X -s sac -k 2.0e2 -h QGSII"
```
