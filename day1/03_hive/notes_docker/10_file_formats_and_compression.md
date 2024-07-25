
## Create a big table 
```
wget https://github.com/erkansirin78/datasets/raw/master/Hotel_Reviews.csv.gz
gzip -d Hotel_Reviews.csv.gz
docker cp Hotel_Reviews.csv cluster-master:/

create table if not exists test1.hotels (Hotel_Address string,
Additional_Number_of_Scoring integer,
Review_Date string,
Average_Score double,
Hotel_Name string,
Reviewer_Nationality string,
Negative_Review string,
Review_Total_Negative_Word_Counts integer,
Total_Number_of_Reviews integer,
Positive_Review string,
Review_Total_Positive_Word_Counts integer,
Total_Number_of_Reviews_Reviewer_Has_Given integer,
Reviewer_Score double,
Tags string,
days_since_review string,
lat string,
lng string)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile
tblproperties('skip.header.line.count'='1');




load data local inpath '/Hotel_Reviews.csv' overwrite into table test1.hotels;
```
## select db
```commandline
use test1;
```


## check
```commandline
select count(1) from test1.hotels;
515738

select hotel_name, average_score,review_date from test1.hotels limit 5;

hotel_name      average_score   review_date
Hotel Arena     7.7     8/3/2017
Hotel Arena     7.7     8/3/2017
Hotel Arena     7.7     7/31/2017
Hotel Arena     7.7     7/31/2017
Hotel Arena     7.7     7/24/2017
```

## Describe
```commandline
describe formatted test1.hotels;
```



## orc format
```
create table test1.hotels_orc stored as orc TBLPROPERTIES ('orc.compress'='NONE') 
as select * from test1.hotels ;

37.974 seconds
```

## parquet format
```commandline
create table test1.hotels_parquet stored as parquet TBLPROPERTIES ('parquet.compression'='UNCOMPRESSED')
as select * from test1.hotels ;

36.667 second
```


## textfile
```commandline
create table test1.hotels_text stored as textfile 
as select * from test1.hotels;

43.017 seconds
```


## with compression 
## orc_snappy
```commandline
## orc_snappy orc.compress = {NONE, ZLIB, SNAPPY} default ZLIB

create table test1.hotels_orc_snappy stored as orc TBLPROPERTIES ('orc.compress'='SNAPPY') 
as select * from test1.hotels;

42.338 seconds
```

## orc_zlib
```commandline
create table test1.hotels_orc_zlib stored as ORC TBLPROPERTIES ('orc.compress'='ZLIB') 
as select * from test1.hotels;

40.922 seconds
```

## parquet_snappy
```commandline
create table test1.hotels_parquet_snappy stored as parquet TBLPROPERTIES ('parquet.compression'='SNAPPY') 
as select * from test1.hotels;

41.447 seconds
```

## parquet_gzib
```commandline
create table test1.hotels_parquet_gzib stored as parquet TBLPROPERTIES ('parquet.compression'='GZIP') 
as select * from test1.hotels;

44.982 seconds
```

## text_snappy
```
SET hive.exec.compress.output=true;
SET io.textfile.compression.type=SNAPPY;

create table test1.hotels_text_snappy stored as textfile 
as select * from test1.hotels;

40.636 seconds
```


## see the disk usage
```commandline
hdfs dfs -du -h /user/hive/warehouse/test1.db

227.1 M  /user/hive/warehouse/test1.db/hotels
106.4 M  /user/hive/warehouse/test1.db/hotels_orc
54.7 M   /user/hive/warehouse/test1.db/hotels_orc_snappy
39.8 M   /user/hive/warehouse/test1.db/hotels_orc_zlib
102.0 M  /user/hive/warehouse/test1.db/hotels_parquet
35.2 M   /user/hive/warehouse/test1.db/hotels_parquet_gzib
58.6 M   /user/hive/warehouse/test1.db/hotels_parquet_snappy
201.8 M  /user/hive/warehouse/test1.db/hotels_text
42.2 M   /user/hive/warehouse/test1.db/hotels_text_snappy
```

- https://community.cloudera.com/t5/Support-Questions/Explain-hdfs-du-command-output/td-p/46586
```commandline
show tables;
drop table hotels_text_snappy;
```
- https://blog.yannickjaquier.com/hadoop/orc-versus-parquet-compression-and-response-time.html










