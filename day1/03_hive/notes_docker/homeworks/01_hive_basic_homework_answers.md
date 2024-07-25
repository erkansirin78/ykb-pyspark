# Questions

### Q-1: 
- Create a hive database `hive_odev` and load this data https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv into `wine` table.

### Q-2
- In `wine` table filter records that `Alcohol`greater than 13.00 then insert these records into `wine_alc_gt_13` table.

### Q-3
- Drop `hive_odev` including underlying table in a single command.

### Q-4 
- https://raw.githubusercontent.com/erkansirin78/datasets/master/hive/employee.txt veri setindeki veriyi `company` adında bir hive veri tabanı `employee` adında tabloya yazınız. 

### Soru-5
- Find the employees that Python skill is greter than 70.






# ANSWERS

### A-1: 
- Download data
```
[train@localhost ~]$ wget -O ~/datasets/Wine.csv https://raw.githubusercontent.com/erkansirin78/datasets/master/Wine.csv
```


- Beeline 
` [train@localhost ~]$ beeline -n train -u jdbc:hive2://localhost:10000  ` 

- Database  
` create database if not exists hive_odev; `

- Select DB
` use hive_odev; ` 

- Table
```
create table if not exists hive_odev.wine (
    Alcohol float, 
    Malic_Acid float,
    Ash float,
    Ash_Alcanity float, 
    Magnesium int,
    Total_Phenols float,
    Flavanoids float,
    Nonflavanoid_Phenols float,
    Proanthocyanins float,
    Color_Intensity float,
    Hue float, 
    OD280 float,
    Proline float, 
    Customer_Segment int
)
row format delimited
fields terminated by ','
collection items terminated by ':'
lines terminated by '\n'
stored as textfile
tblproperties('skip.header.line.count'='1');
```

-Load data into table
	
- **local**: ` load  data local inpath '/home/train/datasets/Wine.csv' into table hive_odev.wine; ` 

- **hdfs**: ` load data inpath '/user/train/hdfs_odev/Wine.csv' into table hive_odev.wine; `  

	
- Select all  
```
select ash, alcohol from hive_odev.wine limit 5;
+-------+----------+
|  ash  | alcohol  |
+-------+----------+
| 2.43  | 14.23    |
| 2.14  | 13.2     |
| 2.67  | 13.16    |
| 2.5   | 14.37    |
| 2.87  | 13.24    |
+-------+----------+
```


### A-2

- Create table using query

` create table hive_odev.wine_alc_gt_13 as select * from hive_odev.wine where alcohol > 13.00;  ` 


### A-3
` drop database hive_odev cascade;  ` 


### A-4 
- Download data

` wget -O ~/datasets/employee.txt  https://raw.githubusercontent.com/erkansirin78/datasets/master/hive/employee.txt `  

- See data
```
cat ~/datasets/employee.txt 
name|work_place|gender_age|skills_score
Michael|Montreal,Toronto|Male,30|DB:80,Network:88
Will|Montreal|Male,35|Perl:85,Scala:82
Shelley|New York|Female,27|Python:80,Spark:95
Lucy|Vancouver|Female,57|Sales:89,HR:94
```
- Create database and table
```
CREATE database if not exists company;


CREATE TABLE company.employee (
name STRING,
work_place ARRAY<STRING>,
gender_age STRUCT<gender:STRING,age:INT>,
skills_score MAP<STRING,INT>
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':'
STORED AS TEXTFILE
tblproperties('skip.header.line.count'='1');
```

- Load data from local

` LOAD DATA LOCAL INPATH '/home/train/datasets/employee.txt' OVERWRITE INTO TABLE company.employee; ` 

- Select 
```
SELECT * from company.employee;

+----------------+-------------------------+-------------------------------+---------------------------+
| employee.name  |   employee.work_place   |      employee.gender_age      |   employee.skills_score   |
+----------------+-------------------------+-------------------------------+---------------------------+
| Michael        | ["Montreal","Toronto"]  | {"gender":"Male","age":30}    | {"DB":80,"Network":88}    |
| Will           | ["Montreal"]            | {"gender":"Male","age":35}    | {"Perl":85,"Scala":82}    |
| Shelley        | ["New York"]            | {"gender":"Female","age":27}  | {"Python":80,"Spark":95}  |
| Lucy           | ["Vancouver"]           | {"gender":"Female","age":57}  | {"Sales":89,"HR":94}      |
+----------------+-------------------------+-------------------------------+---------------------------+
```

### A-5
#### Method-1 
``` 
SELECT name, skills_score['Python'] as Python 
FROM company.employee 
WHERE skills_score['Python'] > 70; 
``` 
- Output
```
+----------+---------+
|   name   | python  |
+----------+---------+
| Shelley  | 80      |
+----------+---------+
```

#### Method-2
```
SELECT * FROM (
SELECT name, skills_score['Python'] as Python 
FROM company.employee) as t1
WHERE Python > 70;
```
- Output 
```
+----------+------------+
| t1.name  | t1.python  |
+----------+------------+
| Shelley  | 80         |
+----------+------------+
```




