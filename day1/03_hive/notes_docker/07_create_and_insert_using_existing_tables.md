### 1. create table using another table
- We can create a table from scratch just with the returning result of a query.
```
create table test1.advertising_sales_gt_20 as select * from test1.advertising where sales > 20;
```
### 2. Check the result
count new table
```
select count(1) from test1.advertising_sales_gt_20;
31
```

### 3. Append new data (insert into) to existing table

- Delete `as` replace `create` with `ìnsert into`  
```
insert into table test1.advertising_sales_gt_20 select * from test1.advertising where sales > 20;

select count(1) from test1.advertising_sales_gt_20;
62
```

### 4. overwrite existing table with select (insert overwrite)
- Just replace `into` with `overwrite` 
```
insert overwrite table test1.advertising_sales_gt_20 select * from test1.advertising where sales > 20;

select count(1) from test1.advertising_sales_gt_20;
31
```

### 5. Create an empty table using another one.
```
create table if not exists test1.adv_lk like test1.advertising;

describe test1.adv_lk;
```