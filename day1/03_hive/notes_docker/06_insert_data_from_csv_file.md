### 1. Notification
Generally we load data to hive from hdfs. However, it is also possible to load from local but not practical. 

### 2. Load data from hdfs

2.1. Create a table that suits data in hdfs.  To learn what to create, better to see data first.
```
curl -O https://raw.githubusercontent.com/erkansirin78/datasets/master/Advertising.csv
 
hdfs dfs -mkdir -p /user/root/datasets

hdfs dfs -put Advertising.csv /user/root/datasets
```

#### 2.2. Create table. 
There is header line in the data. We have to specify during the creation statement as table properties.
```
# select test1 database
use test1;

# Drop table 
drop table test1.advertising;

# create table again
create table if not exists test1.advertising
(id int, tv float, radio float, newspaper float, sales float)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile
tblproperties('skip.header.line.count'='1');


# inspect table
 describe test1.advertising;


# Is there any record?
 select * from test1.advertising;
```

#### 2.3. Load data to hive table
```
load data inpath '/user/root/datasets/Advertising.csv' into table test1.advertising;

```
#### 2.4. See the data
```
 select * from test1.advertising limit 3;
```

#### 2.5. Check data in hdfs  
` hdfs dfs -ls /user/root/datasets | grep Advertising  `   
You will see the data has gone where is it now?  
It is in the default hive warehouse directory. Let's check it.
```
hdfs dfs -ls /user/hive/warehouse/test1.db/advertising
Found 1 items
-rw-r--r--   1 root supergroup       4556 2023-09-16 10:54 /user/hive/warehouse/test1.db/advertising/Advertising.csv
```

#### 2.6. If you see the result like this
```
 select * from test1.advertising limit 10;
+-----------------+-----------------+--------------------+------------------------+--------------------+
| advertising.id  | advertising.tv  | advertising.radio  | advertising.newspaper  | advertising.sales  |
+-----------------+-----------------+--------------------+------------------------+--------------------+
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
| NULL            | NULL            | NULL               | NULL                   | NULL               |
+-----------------+-----------------+--------------------+------------------------+--------------------+
```
It is possibly due to schema data conflict. Check your create table and properties.
If you try second time, don't forget to -put your data to hdfs again because it has already gone.


#### 2.7. load overwrite mode  
put data to hdfs 
`  hdfs dfs -put Advertising.csv /user/root/datasets  `

#### 2.9. Load again  

```
# Check record count
select count(1) from test1.advertising;
200


# load the same data overwrite
 load data inpath '/user/root/datasets/Advertising.csv' overwrite into table test1.advertising;


select count(1) from advertising;
200

```
See there is still 200 records.

#### 2.10. Load with append
-  put data hdfs again
` hdfs dfs -put Advertising.csv /user/root/datasets  `

```
load data inpath '/user/root/datasets/Advertising.csv' into table test1.advertising;


# count
select count(1) from test1.advertising;
400
```

**into appends, overwrite into overwrites.**  

### 3. Load data from local
```
load data local inpath '/Advertising.csv' into table test1.advertising;

# count
select count(1) from advertising;
600
```

### Load overwrite data again last time.
```
load data local inpath '/Advertising.csv' overwrite into table test1.advertising;
```