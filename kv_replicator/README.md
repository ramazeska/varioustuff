# KV replicator

## WHY: i have a situation where consul-replicator is not helping, as i need to copy subset of keys to different, not connnected by wan consul clusters

## My arch:


consul A - httpTunnel -fw- httpTunnel - consul B 


### how this script should run:
1. fill out the config/config.json to your needs
2. by default, script assumes its running in dev, if you need to change env: 
        export RUN_ENV=prod
3. create a prefix_file as in config.json, with such syntax:
```
ORGA
SOMESTRUCTB
ETC
```
and it will try to find and copy all the keys and values that much pattern in "kv_prefix" in config.json

 