## Join departments and categories in retail_db (~/datasets/retail_db)

## create table departments 
```
create table if not exists test1.departments
(departmentId int,departmentName string)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile
tblproperties('skip.header.line.count'='1');
```

## create table categories 
```
create table if not exists test1.categories
(categoryId int, categoryDepartmentId string, categoryName string)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile
tblproperties('skip.header.line.count'='1');
```

## load departments
```commandline
wget https://raw.githubusercontent.com/erkansirin78/datasets/master/retail_db/categories.csv
wget https://raw.githubusercontent.com/erkansirin78/datasets/master/retail_db/departments.csv

load data local inpath '/departments.csv' into table test1.departments;
```
  

```
hive> SELECT * from test1.departments ;
OK
2       Fitness
3       Footwear
4       Apparel
5       Golf
6       Outdoors
7       Fan Shop
```

## load categories
` load data local inpath '/categories.csv' into table test1.categories; ` 

```
hive> SELECT * from test1.categories limit 10;
OK
1       2       Football
2       2       Soccer
3       2       Baseball & Softball
4       2       Basketball
5       2       Lacrosse
6       2       Tennis & Racquet
7       2       Hockey
8       2       More Sports
9       3       Cardio Equipment
10      3       Strength Training
```

## JOIN 
```
SELECT * FROM test1.departments dep
JOIN test1.categories cat ON dep.departmentid = cat.categorydepartmentid 
LIMIT 20;


dep.departmentid        dep.departmentname      cat.categoryid  cat.categorydepartmentid        cat.categoryname
2       Fitness 1       2       Football
2       Fitness 2       2       Soccer
2       Fitness 3       2       Baseball & Softball
2       Fitness 4       2       Basketball
2       Fitness 5       2       Lacrosse
2       Fitness 6       2       Tennis & Racquet
2       Fitness 7       2       Hockey
2       Fitness 8       2       More Sports
3       Footwear        9       3       Cardio Equipment
3       Footwear        10      3       Strength Training
3       Footwear        11      3       Fitness Accessories
3       Footwear        12      3       Boxing & MMA
3       Footwear        13      3       Electronics
3       Footwear        14      3       Yoga & Pilates
3       Footwear        15      3       Training by Sport
3       Footwear        16      3       As Seen on  TV!
4       Apparel 17      4       Cleats
4       Apparel 18      4       Men's Footwear
4       Apparel 19      4       Women's Footwear
4       Apparel 20      4       Kids' Footwear
```


- Attention: departmentid and categorydepartmentid are the same on every rows.




