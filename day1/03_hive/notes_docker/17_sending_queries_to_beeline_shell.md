### 1. Sending queries to beeline shell
` hive -e "set hive.server2.logging.operation.level=NONE; select count(1) from test1.advertising;" `  

### 2. Running multiple queries in a SQL file using beeline
- Prepare your queries
```
cat<<EOF | tee hive_query.sql
set hive.server2.logging.operation.level=NONE;
drop table if exists test1.advertising_sales_gt_20;
use test1;
show tables;
create table if not exists test1.advertising_sales_gt_20 as select * from test1.advertising where sales > 20;
show tables;
select * from test1.advertising_sales_gt_20 limit 5;
EOF
```

- Run your query file
` hive -f ./beeline_query.sql  ` 