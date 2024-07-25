# Start Hive Services
- Connect to master node
```bash
docker exec -it cluster-master bash
```

# Note: Only for the first run
- Init schema
```bash  
schematool -initSchema -dbType postgres
```
- Start hive services
```bash
$HADOOP_HOME/start-hive.sh
```

- Connect beeline
```
$HIVE_HOME/bin/beeline -u jdbc:hive2://localhost:10000
```