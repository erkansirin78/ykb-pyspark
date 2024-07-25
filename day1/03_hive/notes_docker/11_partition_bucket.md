There are four main components for organizing data in Hive:
  
- databases 
- tables
- partitions 
- buckets  

Partitions and buckets improve query performance. Because tables are divided into smaller pieces that can be managed by partitions and/or buckets.

Partitioned table accelerates data access by keeping the data that can be queried together in the same folder to increase performance.

- database -> directory
- table -> directory
- partition -> directory
- bucket -> file segment


- Which rows will be included in which bucket is determined by the hash algorithm applied to the bucket column.

- Partition key column should have low cardinality which adversely affects performance.

- Columns to be used for partition should generally be column(s) that are often used as filters in data access.

- If buckets are used in a partition, it organizes the data by distributing it into file segments in the partition.

- Bucket size is usually hdfs block size or multiples. A simple formula: `Table size /
Number of buckets >= size of HDFS block` or `table size / 1 GB`

- Columns used for bucketing make a positive contribution to performance when used in group by or sort statements.

- Never partition by a unique ID, like user id, phone number.


**Tip:** During the create command, the partition column (sales_date in the example below) is never included in the other columns of the table.

## create a partitioned table
```
hive

create database test1;

CREATE TABLE IF NOT EXISTS 
test1.sales_partitioned_by_date (
sales_id int, 
country string, 
product_id int, 
product_name string, 
quantity int, 
unit_price float) 
partitioned by (sales_date date) row format delimited 
fields terminated by ',' 
lines terminated by '\n' 
stored as ORC;
```

# static and dynamic partition
There are two types of partitioning, static and dynamic.

- Static: Partition is created by the user and the partition is specified when entering the record.

- Dynamic: Hive dynamically partitions according to the specified column/s. The command to create a table for this is the same as the example above, that is, it is no different from static partitioning. Two properties need to be set for dynamic partition:

```
set hive.exec.dynamic.partition=true;
set hive.exec.dynamic.partition.mode=nonestrict;
```

**Tip:** When the dynamic partition is open, the partition column should be placed at the end of the insert command.

## When to use which? 
Static can be used when we know the data well, but it requires extra time of development.  

In dynamic partition hive sets partition event itself, but it is a bit slow compared to static. Also, the number of dynamic partitions is limited to 100 per node, otherwise you will get an error.

## Insert data into partitioned table
So how do we enter data into hive dynamic partitioned table? There are two key points to note.
- 1. In addition to the normal insert command, **PARTITION(column)** must be specified. 
- 2. Partition column values should be placed last.

```
INSERT INTO test1.sales_partitioned_by_date PARTITION (sales_date) 
VALUES (100001, 'UK', 2134562, 'String Tanbur', 1, 2389.99, '2020-04-20'),
(100002, 'USA', 2134563, 'Lackland Bass Quitar', 1, 1389.99, '2020-02-19'),
(100002, 'UK', 2134563, 'Lackland Bass Quitar', 1, 1389.99, '2020-02-19'),
(100004, 'TR', 2134563, 'Markbass Apmlifier', 1, 380.99, '2020-03-19'),
(100005, 'FR', 2133563, 'Drump Istanbul', 1, 889.99, '2020-04-11'),
(100006, 'UK', 2134563, 'Tamaha Bass Quitar', 1, 2359.99, '2020-04-14'),
(100007, 'USA', 2134513, 'Ibanez GRG170DX ', 1, 243.99, '2020-04-09'),
(100008, 'TR', 2134560, 'Yamaha ERG 121 GPII', 1, 248.99, '2020-04-03'),
(100009, 'UK', 2134569, 'Istanbul Samatya Cymbal Set', 1, 465.00, '2020-03-19'),
(100010, 'FR', 2134562, 'Zildjian K Cymbal Set', 1, 895.99, '2020-04-11');

select count(1) from test1.sales_partitioned_by_date;
+------+
| _c0  |
+------+
| 10   |
+------+
```

## see partitions
```
hdfs dfs -ls /user/hive/warehouse/test1.db/sales_partitioned_by_date
Found 7 items
drwxr-xr-x   - train hive          0 2020-11-02 22:53 /user/hive/warehouse/test1.db/sales_partitioned_by_date/sales_date=2020-02-19
drwxr-xr-x   - train hive          0 2020-11-02 22:53 /user/hive/warehouse/test1.db/sales_partitioned_by_date/sales_date=2020-03-19
drwxr-xr-x   - train hive          0 2020-11-02 22:53 /user/hive/warehouse/test1.db/sales_partitioned_by_date/sales_date=2020-04-03
drwxr-xr-x   - train hive          0 2020-11-02 22:53 /user/hive/warehouse/test1.db/sales_partitioned_by_date/sales_date=2020-04-09
drwxr-xr-x   - train hive          0 2020-11-02 22:53 /user/hive/warehouse/test1.db/sales_partitioned_by_date/sales_date=2020-04-11
drwxr-xr-x   - train hive          0 2020-11-02 22:53 /user/hive/warehouse/test1.db/sales_partitioned_by_date/sales_date=2020-04-14
drwxr-xr-x   - train hive          0 2020-11-02 22:53 /user/hive/warehouse/test1.db/sales_partitioned_by_date/sales_date=2020-04-20
```
Another way
```
SHOW partitions test1.sales_partitioned_by_date;
sales_date=2020-02-19
sales_date=2020-03-19
sales_date=2020-04-03
sales_date=2020-04-09
sales_date=2020-04-11
sales_date=2020-04-14
sales_date=2020-04-20
```
## Bucketing table
Bucketing is also about data organization. Just as partitioning keeps data in different folders, bucketing keeps data in different files within the partition or without partition. 

We have to specify how many buckets will be there while creating the table. Bucketing is good for **query and join performance**. It can be used especially for join columns. Before creating the bucketing table   

` set hive.enforce.bucketing = true;  `   

must be set. 


## Partitioning  + Bucketing Example
```
CREATE TABLE IF NOT EXISTS test1.sales_part_country_buck_prodcid (sales_id int, product_id int, product_name string, quantity int, unit_price float, sales_date date) 
partitioned by (country string) 
clustered by (product_id) into 2 buckets 
row format delimited 
fields terminated by ',' 
lines terminated by '\n' 
stored as textfile;
```
insert data
```
INSERT INTO test1.sales_part_country_buck_prodcid PARTITION (country) 
VALUES 
(100001,  2134562, 'String Tanbur', 1, 2389.99, '2020-04-20', 'UK'),
(100002,  2134563, 'Lackland Bass Quitar', 1, 1389.99, '2020-02-19', 'USA'),
(100003,  2134563, 'Lackland Bass Quitar', 1, 1389.99, '2020-02-19', 'UK'),
(100004,  2134563, 'Markbass Apmlifier', 1, 380.99, '2020-03-19', 'TR'),
(100005,  2133563, 'Drump Istanbul', 1, 889.99, '2020-04-11', 'FR'),
(100006,  2134563, 'Tamaha Bass Quitar', 1, 2359.99, '2020-04-14', 'UK'),
(100007,  2134513, 'Ibanez GRG170DX ', 1, 243.99, '2020-04-09', 'USA'),
(100008,  2134560, 'Yamaha ERG 121 GPII', 1, 248.99, '2020-04-03', 'TR'),
(100009,  2134569, 'Istanbul Samatya Cymbal Set', 1, 465.00, '2020-03-19', 'UK'),
(100010,  2134562, 'Zildjian K Cymbal Set', 1, 895.99, '2020-04-11', 'FR'),
(100011,  2134562, 'String Tanbur', 1, 2389.99, '2020-04-20', 'UK'),
(100012,  2134563, 'Lackland Bass Quitar', 1, 1389.99, '2020-02-19', 'USA'),
(100013,  2134563, 'Lackland Bass Quitar', 1, 1389.99, '2020-02-19', 'UK'),
(100014,  2134563, 'Markbass Apmlifier', 1, 380.99, '2020-03-19', 'TR'),
(100015,  2133563, 'Drump Istanbul', 1, 889.99, '2020-04-11', 'FR'),
(100016,  2134563, 'Tamaha Bass Quitar', 1, 2359.99, '2020-04-14', 'UK'),
(100017,  2134513, 'Ibanez GRG170DX ', 1, 243.99, '2020-04-09', 'USA'),
(100018,  2134560, 'Yamaha ERG 121 GPII', 1, 248.99, '2020-04-03', 'TR'),
(100019,  2134569, 'Istanbul Samatya Cymbal Set', 1, 465.00, '2020-03-19', 'UK'),
(100020,  2134562, 'Zildjian K Cymbal Set', 1, 895.99, '2020-04-11', 'FR'),
(100021,  2134562, 'String Tanbur', 1, 2389.99, '2020-04-20', 'UK'),
(100022,  2134563, 'Lackland Bass Quitar', 1, 1389.99, '2020-02-19', 'USA'),
(100023,  2134563, 'Lackland Bass Quitar', 1, 1389.99, '2020-02-19', 'UK'),
(100024,  2134563, 'Markbass Apmlifier', 1, 380.99, '2020-03-19', 'TR'),
(100025,  2133563, 'Drump Istanbul', 1, 889.99, '2020-04-11', 'FR'),
(100026,  2134563, 'Tamaha Bass Quitar', 1, 2359.99, '2020-04-14', 'UK'),
(100027,  2134513, 'Ibanez GRG170DX ', 1, 243.99, '2020-04-09', 'USA'),
(100028,  2134560, 'Yamaha ERG 121 GPII', 1, 248.99, '2020-04-03', 'TR'),
(100029,  2134569, 'Istanbul Samatya Cymbal Set', 1, 465.00, '2020-03-19', 'UK'),
(100030,  2134562, 'Zildjian K Cymbal Set', 1, 895.99, '2020-04-11', 'FR');
```

- partitions
```
hdfs dfs -ls /user/hive/warehouse/test1.db/sales_part_country_buck_prodcid
Found 4 items
drwxr-xr-x   - train hive          0 2020-11-02 23:28 /user/hive/warehouse/test1.db/sales_part_country_buck_prodcid/country=FR
drwxr-xr-x   - train hive          0 2020-11-02 23:28 /user/hive/warehouse/test1.db/sales_part_country_buck_prodcid/country=TR
drwxr-xr-x   - train hive          0 2020-11-02 23:28 /user/hive/warehouse/test1.db/sales_part_country_buck_prodcid/country=UK
drwxr-xr-x   - train hive          0 2020-11-02 23:28 /user/hive/warehouse/test1.db/sales_part_country_buck_prodcid/country=USA
```
- buckets
```
hdfs dfs -ls /user/hive/warehouse/test1.db/sales_part_country_buck_prodcid/country=FR
Found 2 items
-rw-r--r--   1 train hive        321 2020-11-02 23:28 /user/hive/warehouse/test1.db/sales_part_country_buck_prodcid/country=FR/000000_0
-rw-r--r--   1 train hive          0 2020-11-02 23:28 /user/hive/warehouse/test1.db/sales_part_country_buck_prodcid/country=FR/000001_0
```
see what is in the buckets
```
hdfs dfs -ls /user/hive/warehouse/test1.db/sales_part_country_buck_prodcid/country=FR
Found 2 items
-rw-r--r--   1 train hive        321 2020-11-02 23:28 /user/hive/warehouse/test1.db/sales_part_country_buck_prodcid/country=FR/000000_0
-rw-r--r--   1 train hive          0 2020-11-02 23:28 /user/hive/warehouse/test1.db/sales_part_country_buck_prodcid/country=FR/000001_0

hdfs dfs -cat /user/hive/warehouse/test1.db/sales_part_country_buck_prodcid/country=FR/000000_0
100030,2134562,Zildjian K Cymbal Set,1,895.99,2020-04-11
100025,2133563,Drump Istanbul,1,889.99,2020-04-11
100020,2134562,Zildjian K Cymbal Set,1,895.99,2020-04-11
100015,2133563,Drump Istanbul,1,889.99,2020-04-11
100010,2134562,Zildjian K Cymbal Set,1,895.99,2020-04-11
100005,2133563,Drump Istanbul,1,889.99,2020-04-11
```

