#  Global Docker file 

usage example:

``` 
cd varioustuff
docker build . \
 -f  DockerFile/Dockerfile \
 --build-arg SCRIPTDIR=kv_replicator \
 --build-arg RUNNABLE=replicator.py -t test:0.0.1
```


so, basicaly should build any script under varioustuff/* , if the directory layout is at minimum like:

```
script/
  script-runner.py
  PythonDeps/
    pip_req.txt
```

that's all folks!