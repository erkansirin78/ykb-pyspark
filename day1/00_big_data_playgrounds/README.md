# Docker hadoop yarn spark hive cluster

## Run compose

```bash
docker login

docker pull veribilimiokulu/ubuntu_hadoop_hive_sqoop:3.0

docker-compose up -d
```
### Wait hadoop services start
```commandline
 docker logs -f cluster-master
```
## Init Hive Metastore schema

```bash
docker exec -it cluster-master bash
```

## Note: Only for the first run

```bash  
schematool -initSchema -dbType postgres
```
### Start Hive
```bash
$HADOOP_HOME/start-hive.sh
```

## Check hive services
```commandline
pgrep -f org.apache.hive.service.server.HiveServer2

pgrep -f org.apache.hadoop.hive.metastore.HiveMetaStore
```

## Beeline
```commandline
$HIVE_HOME/bin/beeline -u jdbc:hive2://localhost:10000
```