### 1. Terminal-2: Prepare for Map-Reduce job
- Create a folder for jar and fruit file
```
 mkdir my_big_data
cd my_big_data/
 pwd
/my_big_data
```
- Copy jar and fruit file from physical machine to vm into my_big_data folder using scp or MobaXterm UI
```commandline
(base) [train@localhost tmp]$ docker cp dried_fruits.txt cluster-master:/my_big_data
(base) [train@localhost tmp]$ docker cp mapreduce.wordcount.jar cluster-master:/my_big_data
```
- Now they are in master container
```
 ls
dried_fruits.txt  mapreduce.wordcount.jar
```

- Create a folder in hdfs for input to map-reduce job  
` hdfs dfs -mkdir -p /user/root/datasets/dried_fruits_input `  

- Copy fruits file to hdfs  
` hdfs dfs -mkdir -p  /user/root/datasets/dried_fruits_input `  


### 2. Run MapReduce job
```
yarn jar mapreduce.wordcount.jar \
com.veribilimiokulu.mapreduce.MR2WordCount \
/user/root/datasets/dried_fruits_input \
/user/root/datasets/dried_fruits_out
```
- See http://localhost:8088/cluster/apps/ACCEPTED in accpted state.  

### 3. Kill PySpark application
Terminal-1 `exit()` and see yarn application (mapreduce) chaged running state.   
Wait till mapreduce ends. 


### 4. See the application outputs  
```
 hdfs dfs -cat /user/root/datasets/dried_fruits_out/part-r-00000
ANTEP FISTIK    2244
CEVIZ   13020
FINDIK  7842
KAJU    6186
YER FISTIĞI     1866
ÇIĞ FINDIK      1866
ÜZÜM    7716
```

### 5. Resource Manager UI
Open Resource manager UI and see yarn application moved running state to finished one.   
See also PySparkshell application in killed state.  
