# QUESTIONS
### Q-1: 
- Download and put `https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv` dataset in hdfs `/user/train/hdfs_odev` directory.

### Q-2:
- Copy this hdfs file `/user/root/hdfs_odev/Wine.csv` to `/tmp/hdfs_odev` hdfs directory.

### Q-3:
- Delete `/tmp/hdfs_odev` directory with skipping the trash. 

### Q-4:
-  Explore `/user/root/hdfs_odev/Wine.csv` file from web hdfs.   


# ANSWERS

### A-1: 
- Download dataset 
` wget https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv  `

-  Create hdfs directory  
`  hdfs dfs -mkdir /user/root/hdfs_odev  `  

- Put Wine.csv file to hdfs  
`  hdfs dfs -put Wine.csv /user/root/hdfs_odev  `  

### A-2:
- Create hdfs directory  
`  hdfs dfs -mkdir /tmp/hdfs_odev  ` 

- Copy file  
`  hdfs dfs -cp /user/root/hdfs_odev/Wine.csv /tmp/hdfs_odev  `  

### A-3:
- Delete
` hdfs dfs -rm -R -skipTrash /tmp/hdfs_odev  ` 

### A-4:
- Open browser.
- Enter namenode address: ` http://localhost:5070/explorer.html#/user/root/hdfs_odev  `.
