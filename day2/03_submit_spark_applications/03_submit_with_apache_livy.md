# apache livy server installation 
## Download
`wget https://ftp.itu.edu.tr/Mirror/Apache/incubator/livy/0.7.1-incubating/apache-livy-0.7.1-incubating-bin.zip`

## Unzip
`unzip apache-livy-0.7.1-incubating-bin.zip `

## Link
`ln -s apache-livy-0.7.1-incubating-bin livy`

## Add environment
```
sudo vim /etc/environment 
export LIVY_HOME=/opt/manual/livy/
export LIVY_CONF_DIR=/opt/manual/livy/conf/

PATH $LIVY_HOME/bin 


source /etc/environment 

echo $LIVY_HOME 
```
## Configuration
```
cd /opt/manual/livy/conf/
cp livy.conf.template livy.conf
cp livy-env.sh.template livy-env.sh
```

- In livy.conf uncomment and change the value  
` livy.spark.master =  yarn `  


## Start Livy
` livy-server start `

## Status
```
[train@localhost ~]$ livy-server status
livy-server is running (pid: 5761)
```

## web ui
` http://localhost:8998/ui `

## Job submit
### Batch
- copy application file to hdfs

- submit
```
curl -X POST \
--data '{"file": "/user/train/forex_processing.py", "proxyUser":"abuzittin","name":"My Livy Example Session"}' \
-H "Content-Type: application/json" \
192.168.206.130:8998/batches
```

```
curl -X POST \
--data '{"file": "/user/train/main.py", "proxyUser":"abuzittin","name":"My Livy Example Session"}' \
-H "Content-Type: application/json" \
192.168.206.130:8998/batches
```