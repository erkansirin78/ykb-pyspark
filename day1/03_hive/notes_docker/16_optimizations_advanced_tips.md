## 
SQL-on-Hadoop systems are significantly popular solutions for querying data available in a Hadoop cluster, of which several can be highlighted: 

## Long run, heavy loads, high latency on very large data.
- Hive (Apache) 
- Spark SQL (Apache)

## Interactive, low latency but limited data size.
- Presto (Facebook) -> 
- Drill (Apache)
- Impala (Cloudera)



## Hive variables
```

# Assign yesterday to a var
SET hivevar:YESTERDAY = regexp_replace( cast(date_sub(CURRENT_DATE, 1 ) AS STRING), "-","");


# Using var in select statement
select ${hivevar:YESTERDAY};


+-----------+
|    _c0    |
+-----------+
| 20201102  |
+-----------+
```

## Close a table to query
` alter table salaries_temp enable offline; `


## HIVE JOIN PERFORMANCE TIPS
During the hive join operation, the first table is buffered in memory (buffering) and the second is streamed over it. Because memory is limited, it is necessary to stream the large table. You can do this either by specifying it explicitly or by leaving the large table on the right. Below is an example of clearly stating it.
```
SELECT /*+ STREAMTABLE (products) */ categoryname, productname from azhadoop.categories cat 
JOIN default.products prd ON  cat.categoryid = prd.productcategoryid 
LIMIT 10;
```

## HIVE EXTERNAL TABLE

In case of internal table, both metadata and data are managed by hive.
- If we want to access this table data, we can only do it via hive.
- Metadata and data are deleted when internal table is dropped.
- Create table command creates internal table by default.
- The default address for these tables is “/user/hive/warehouse/<database-name>/<table-name>”.

In case of external table, only metadata is managed by hive.
- Syntax is the same as internal table. It is only created with `create external table `.
- If no address is specified, these tables are also stored in the "/user/hive/warehouse/table-name" directory.
- The metadata of these tables is managed by hive and the data is managed by hdfs. This is the biggest difference between internal and internal.
- When external table is dropped, metadata is deleted but data remains in hdfs.

## PERFORMANCE TIPS
### 1. Use Tez or Spark execution engine if possible.

### 2. Don't use other formats but ORC, unless you have to.
- It takes up little space and has fast query performance.

### 3. Use partitioning but use it properly.
- Not for just use but when you really need it.

### 4. Use bucketing especially on join and sort columns.

### 5. Vectorization: Increases performance by allowing batch processing instead of line-by-line processing.
SET hive.vectorized.execution.enabled=true;

### 6. Cost based optimization: 
Before a query is run, logical and physical query plans are prepared.
```
SET hive.cbo.enable=true; -- default true after v0.14.0
SET hive.compute.query.using.stats=true; -- default false
SET hive.stats.fetch.column.stats=true; -- default false
SET hive.stats.fetch.partition.stats=true; -- default true
```

### 7. Indexing: Removed as of Hive 3.0. Alternatively, materialized views can be used.
https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Indexing#LanguageManualIndexing-IndexingIsRemovedsince3.0
