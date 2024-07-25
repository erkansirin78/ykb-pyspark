-- select db
use test1;

/*
 * Prepare data. It must be in a folder. 
 * [train@localhost play]$ hdfs dfs -mkdir -p /user/root/datasets/hiveExternal/advertising
 * [train@localhost play]$ hdfs dfs -put /Advertising.csv /user/root/datasets/hiveExternal/advertising
 */

-- create table that fits data. We use another table which has the same schema.
create external table if not exists test1.adv_ext
(id int, tv float, radio float, newspaper float, sales float)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile
LOCATION '/user/root/datasets/hiveExternal/advertising';

-- check
select count(1) FROM test1.adv_ext;
-- 201

select * from adv_ext limit 5;
/*
id|tv   |radio|newspaper|sales|
--|-----|-----|---------|-----|
  |     |     |         |     |
 1|230.1| 37.8|     69.2| 22.1|
 2| 44.5| 39.3|     45.1| 10.4|
 3| 17.2| 45.9|     69.3|  9.3|
 4|151.5| 41.3|     58.5| 18.5|
*/

-- First line is null. We have to specify skip first line in table properties

ALTER TABLE test1.adv_ext SET TBLPROPERTIES ("skip.header.line.count"="1");


select * from adv_ext limit 5;
/*
 * 
id|tv   |radio|newspaper|sales|
--|-----|-----|---------|-----|
 1|230.1| 37.8|     69.2| 22.1|
 2| 44.5| 39.3|     45.1| 10.4|
 3| 17.2| 45.9|     69.3|  9.3|
 4|151.5| 41.3|     58.5| 18.5|
 5|180.8| 10.8|     58.4| 12.9|
 */

SELECT count(1) from test1.adv_ext;
-- 200

-- drop and see if the data still exists
drop table test1.adv_ext;

/*
[train@localhost big_data]$ hdfs dfs -ls /user/train/datasets/hiveExternal/advertising
Found 1 items
-rw-r--r--   1 train supergroup       4556 2020-09-17 11:30 /user/train/datasets/hiveExternal/advertising/Advertising.csv
 */

-- As you see table has gone but data is still there.


-- https://dwgeek.com/hive-create-external-tables-examples.html/








