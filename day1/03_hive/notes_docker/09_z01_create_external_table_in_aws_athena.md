## Upload Advertising.csv data to s3 bucket

## Open Athena

## Create table
```commandline
create external table if not exists adv_ext
(id int, tv float, radio float, newspaper float, sales float)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile
LOCATION 's3://vbo-de-bootcamp/advertising'
tblproperties('skip.header.line.count'='1');
```

## Query the data