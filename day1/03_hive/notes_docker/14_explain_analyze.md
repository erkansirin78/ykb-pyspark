## EXPLAIN statement
Hive provides an EXPLAIN statement to return a query execution plan without running the
query. We can use it to analyze queries if we have concerns about their performance. 

`EXPLAIN [FORMATTED|EXTENDED|DEPENDENCY|AUTHORIZATION] hql_query`  

```
EXPLAIN select Hotel_Name, AVG(Average_Score) AS avg_count from test1.hotels_orc 
group by Hotel_Name
order by avg_count DESC ;
```

```
------------------------------------------------------------------------------------------------------------+
STAGE DEPENDENCIES:                                                                                         |
  Stage-1 is a root stage                                                                                   |
  Stage-2 depends on stages: Stage-1                                                                        |
  Stage-0 depends on stages: Stage-2                                                                        |
                                                                                                            |
STAGE PLANS:                                                                                                |
  Stage: Stage-1                                                                                            |
    Map Reduce                                                                                              |
      Map Operator Tree:                                                                                    |
          TableScan                                                                                         |
            alias: hotels_orc                                                                               |
            Statistics: Num rows: 515738 Data size: 667880710 Basic stats: COMPLETE Column stats: NONE      |
            Select Operator                                                                                 |
              expressions: average_score (type: double), hotel_name (type: string)                          |
              outputColumnNames: average_score, hotel_name                                                  |
              Statistics: Num rows: 515738 Data size: 667880710 Basic stats: COMPLETE Column stats: NONE    |
              Group By Operator                                                                             |
                aggregations: sum(average_score), count(average_score)                                      |
                keys: hotel_name (type: string)                                                             |
                mode: hash                                                                                  |
                outputColumnNames: _col0, _col1, _col2                                                      |
                Statistics: Num rows: 515738 Data size: 667880710 Basic stats: COMPLETE Column stats: NONE  |
                Reduce Output Operator                                                                      |
                  key expressions: _col0 (type: string)                                                     |
                  sort order: +                                                                             |
                  Map-reduce partition columns: _col0 (type: string)                                        |
                  Statistics: Num rows: 515738 Data size: 667880710 Basic stats: COMPLETE Column stats: NONE|
                  value expressions: _col1 (type: double), _col2 (type: bigint)                             |
      Execution mode: vectorized                                                                            |
      Reduce Operator Tree:                                                                                 |
        Group By Operator                                                                                   |
          aggregations: sum(VALUE._col0), count(VALUE._col1)                                                |
          keys: KEY._col0 (type: string)                                                                    |
          mode: mergepartial                                                                                |
          outputColumnNames: _col0, _col1, _col2                                                            |
          Statistics: Num rows: 257869 Data size: 333940355 Basic stats: COMPLETE Column stats: NONE        |
          Select Operator                                                                                   |
            expressions: _col0 (type: string), (_col1 / _col2) (type: double)                               |
            outputColumnNames: _col0, _col1                                                                 |
            Statistics: Num rows: 257869 Data size: 333940355 Basic stats: COMPLETE Column stats: NONE      |
            File Output Operator                                                                            |
              compressed: false                                                                             |
              table:                                                                                        |
                  input format: org.apache.hadoop.mapred.SequenceFileInputFormat                            |
                  output format: org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat                  |
                  serde: org.apache.hadoop.hive.serde2.lazybinary.LazyBinarySerDe                           |
                                                                                                            |
  Stage: Stage-2                                                                                            |
    Map Reduce                                                                                              |
      Map Operator Tree:                                                                                    |
          TableScan                                                                                         |
            Reduce Output Operator                                                                          |
              key expressions: _col1 (type: double)                                                         |
              sort order: -                                                                                 |
              Statistics: Num rows: 257869 Data size: 333940355 Basic stats: COMPLETE Column stats: NONE    |
              value expressions: _col0 (type: string)                                                       |
      Execution mode: vectorized                                                                            |
      Reduce Operator Tree:                                                                                 |
        Select Operator                                                                                     |
          expressions: VALUE._col0 (type: string), KEY.reducesinkkey0 (type: double)                        |
          outputColumnNames: _col0, _col1                                                                   |
          Statistics: Num rows: 257869 Data size: 333940355 Basic stats: COMPLETE Column stats: NONE        |
          File Output Operator                                                                              |
            compressed: false                                                                               |
            Statistics: Num rows: 257869 Data size: 333940355 Basic stats: COMPLETE Column stats: NONE      |
            table:                                                                                          |
                input format: org.apache.hadoop.mapred.SequenceFileInputFormat                              |
                output format: org.apache.hadoop.hive.ql.io.HiveSequenceFileOutputFormat                    |
                serde: org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe                                   |
                                                                                                            |
  Stage: Stage-0                                                                                            |
    Fetch Operator                                                                                          |
      limit: -1                                                                                             |
      Processor Tree:                                                                                       |
        ListSink                                                                                            |
                                                                                                            |
```

## ANALYZE statement
- Hive statistics are a collection of data that describes more details, such as the number of
rows, number of files, and raw data size of the objects in the database.

- Hive supports statistics at the table, partition, and column level. These statistics serve as an input to the Hive Cost-Based Optimizer (CBO), which is an optimizer used to pick the query plan with the lowest cost in terms of system resources required to complete the query.

` ANALYZE TABLE test1.hotels_orc COMPUTE STATISTICS;  `

- We can enable automatic gathering of statistics by specifying  
 
` SET hive.stats.autogather=true `. 

For new tables or partitions that are populated through the INSERT OVERWRITE/INTO statement (rather than the LOAD statement), statistics are automatically collected in the metastore.

