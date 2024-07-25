## 1. Check if hiveserver2 is running  
```
root@cluster-master:/# pgrep -f org.apache.hive.service.server.HiveServer2

1516
``` 

## 2. Check if hive metastore is running  
```
root@cluster-master:/# pgrep -f org.apache.hadoop.hive.metastore.HiveMetaStore
1515
```
## 3. Beeline connection  
` beeline -u jdbc:hive2://cluster-master:10000`
  
### Close logs  
`  set hive.server2.logging.operation.level=NONE;  `  

## 4. List databases
```
show databases;
```
##  5. exit from beeline
` !q `