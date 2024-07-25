# Questions

## Q-1
- Use datasets (u.data ve u.item) in https://github.com/erkansirin78/datasets/tree/master/ml-100k

### 1.1. 
Load these two datasets as tables in `movielens` database in Hive.

### 1.2. 
Explain the relations between u.data and u.item.

## Q-2
 
### Business needs: 
- Frequently querying most popular movies of a month. 
- Queries need lowest latency as much as possible. 

### 2.1 Create a table named movie_ratings which satisfies business need. 

### 2.2. On this table prepare a query that finds top rate counts (most rated) movies in April 1998.

### 2.3. On this table prepare a query that finds top average movies in April 1998.

Hint: Hive join ise same as in SQL.


# Answers

## A-1

- Download datasets
`  wget -O ~/datasets/u.data https://raw.githubusercontent.com/erkansirin78/datasets/master/ml-100k/u.data `  

`  wget -O ~/datasets/u.item https://raw.githubusercontent.com/erkansirin78/datasets/master/ml-100k/u.item  `  

- Explore datasets 
``` 
[train@localhost ~]$ head ~/datasets/u.item
movieid|movietitle|releasedate|videoreleasedate|IMDbURL|unknown|Action|Adventure|Animation|Children's|Comedy|Crime|Documentary|Drama|Fantasy|Film-Noir|Horror|Musical|Mystery|Romance|Sci-Fi|Thriller|War|Western
1|ToyStory(1995)|01-Jan-1995||http://us.imdb.com/M/title-exact?Toy%20Story%20(1995)|0|0|0|1|1|1|0|0|0|0|0|0|0|0|0|0|0|0|0
2|GoldenEye(1995)|01-Jan-1995||http://us.imdb.com/M/title-exact?GoldenEye%20(1995)|0|1|1|0|0|0|0|0|0|0|0|0|0|0|0|0|1|0|0
3|FourRooms(1995)|01-Jan-1995||http://us.imdb.com/M/title-exact?Four%20Rooms%20(1995)|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|1|0|0
4|GetShorty(1995)|01-Jan-1995||http://us.imdb.com/M/title-exact?Get%20Shorty%20(1995)|0|1|0|0|0|1|0|0|1|0|0|0|0|0|0|0|0|0|0
5|Copycat(1995)|01-Jan-1995||http://us.imdb.com/M/title-exact?Copycat%20(1995)|0|0|0|0|0|0|1|0|1|0|0|0|0|0|0|0|1|0|0
6|ShanghaiTriad(Yaoayaoyaodaowaipoqiao)(1995)|01-Jan-1995||http://us.imdb.com/Title?Yao+a+yao+yao+dao+waipo+qiao+(1995)|0|0|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0
7|TwelveMonkeys(1995)|01-Jan-1995||http://us.imdb.com/M/title-exact?Twelve%20Monkeys%20(1995)|0|0|0|0|0|0|0|0|1|0|0|0|0|0|0|1|0|0|0
8|Babe(1995)|01-Jan-1995||http://us.imdb.com/M/title-exact?Babe%20(1995)|0|0|0|0|1|1|0|0|1|0|0|0|0|0|0|0|0|0|0
9|DeadManWalking(1995)|01-Jan-1995||http://us.imdb.com/M/title-exact?Dead%20Man%20Walking%20(1995)|0|0|0|0|0|0|0|0|1|0|0|0|0|0|0|0|0|0|0


[train@localhost ~]$ head ~/datasets/u.data
user_id item_id rating  timestamp
196     242     3       881250949
186     302     3       891717742
22      377     1       878887116
244     51      2       880606923
166     346     1       886397596
298     474     4       884182806
115     265     2       881171488
253     465     5       891628467
305     451     3       886324817
```


- Beeline

- Create database
```  
create database if not exists movielens;
```

### Load ratings (u.data)
- Understand u.data and create `ratings` table.
```
create table if not exists movielens.ratings (user_id int, item_id int, rating int,  rating_time bigint) 
row format delimited 
fields terminated by '\t' 
lines terminated by '\n' 
stored as textfile 
tblproperties('skip.header.line.count'='1');
```

-  Load from local
` load data local inpath '/home/train/datasets/u.data' into table movielens.ratings; `

- Select
```
select * from movielens.ratings limit 4;
+------------------+------------------+-----------------+----------------------+
| ratings.user_id  | ratings.item_id  | ratings.rating  | ratings.rating_time  |
+------------------+------------------+-----------------+----------------------+
| 196              | 242              | 3               | 881250949            |
| 186              | 302              | 3               | 891717742            |
| 22               | 377              | 1               | 878887116            |
| 244              | 51               | 2               | 880606923            |
+------------------+------------------+-----------------+----------------------+

 select count(1) from movielens.ratings;
+---------+
|   _c0   |
+---------+
| 100000  |
+---------+

 select count(distinct user_id) from movielens.ratings;
+------+
| _c0  |
+------+
| 943  |
+------+
```

### Load movies (u.item)

- Create table 
```
create table if not exists  movielens.movies (
    movieid int, 
    movietitle string, 
    releasedate string,
    videoreleasedate string,
    IMDbURL string, 
    unknown tinyint,
    Action tinyint,
    Adventure tinyint,
    Animation tinyint,
    Childrens tinyint,
    Comedy tinyint,
    Crime tinyint,
    Documentary tinyint,
    Drama tinyint,
    Fantasy tinyint,
    FilmNoir tinyint,
    Horror tinyint,
    Musical tinyint,
    Mystery tinyint,
    Romance tinyint,
    SciFi tinyint,
    Thriller tinyint,
    War tinyint,
    Western  tinyint)
    row format delimited 
fields terminated by '|' 
lines terminated by '\n' 
stored as textfile 
tblproperties('skip.header.line.count'='1');
```

-  Load from loacal
` load data local inpath '/home/train/datasets/u.item' into table movielens.movies; `

- Select
```
select movieid, movietitle, releasedate from  movielens.movies limit 5;
+----------+------------------+--------------+
| movieid  |    movietitle    | releasedate  |
+----------+------------------+--------------+
| 1        | ToyStory(1995)   | 01-Jan-1995  |
| 2        | GoldenEye(1995)  | 01-Jan-1995  |
| 3        | FourRooms(1995)  | 01-Jan-1995  |
| 4        | GetShorty(1995)  | 01-Jan-1995  |
| 5        | Copycat(1995)    | 01-Jan-1995  |
+----------+------------------+--------------+

select count(1) from movielens.movies;
+-------+
|  _c0  |
+-------+
| 1682  |
+-------+
```
### 1.2. u.data and u.item relations

- In movies movieid is primary key, in ratings item_id foreign key.
There is 1-M relation. 
1682 movie rated by 943 users. There are 100000 ratings.
releasedate is release date whereas rating_time ise rated date by user.

## A-2 

### 2.1 

- Partition by year and month, bucket by movie titles

```
create table if not exists movielens.movie_ratings ( 
user_id int,
rating int,
rating_time bigint,
movieid int,
movietitle string,
videoreleasedate string,
imdburl string)
partitioned by (review_year int, review_month int)
clustered by (movietitle) into 4 buckets 
stored as orc;
```

- Open dynamic partitioning
```
set hive.exec.dynamic.partition=true;
set hive.exec.dynamic.partition.mode=nonstrict;
set hive.enforce.bucketing=true;
```

- Load data
```
insert overwrite table movielens.movie_ratings PARTITION(review_year, review_month)  
select user_id,
rating,
rating_time,
movieid,
movietitle,
videoreleasedate,
imdburl,
YEAR(from_unixtime(rating_time, 'yyyy-MM-dd')) as review_year,
MONTH(from_unixtime(rating_time, 'yyyy-MM-dd')) as review_month
from movielens.ratings r join movielens.movies m on r.item_id = m.movieid;

No rows affected (174.211 seconds)
```

- Check
```
select count(1) from movielens.movie_ratings;
+---------+
|   _c0   |
+---------+
| 100000  |
+---------+


show partitions movielens.movie_ratings;
+-----------------------------------+
|             partition             |
+-----------------------------------+
| review_year=1997/review_month=10  |
| review_year=1997/review_month=11  |
| review_year=1997/review_month=12  |
| review_year=1997/review_month=9   |
| review_year=1998/review_month=1   |
| review_year=1998/review_month=2   |
| review_year=1998/review_month=3   |
| review_year=1998/review_month=4   |
+-----------------------------------+

describe movielens.movie_ratings;
+--------------------------+------------+----------+
|         col_name         | data_type  | comment  |
+--------------------------+------------+----------+
| user_id                  | int        |          |
| rating                   | int        |          |
| rating_time              | bigint     |          |
| movieid                  | int        |          |
| movietitle               | string     |          |
| videoreleasedate         | string     |          |
| imdburl                  | string     |          |
| review_year              | int        |          |
| review_month             | int        |          |
|                          | NULL       | NULL     |
| # Partition Information  | NULL       | NULL     |
| # col_name               | data_type  | comment  |
| review_year              | int        |          |
| review_month             | int        |          |
+--------------------------+------------+----------+


select distinct (review_year, review_month) from movielens.movie_ratings;
+--------------------------+
|           _c0            |
+--------------------------+
| {"col1":1997,"col2":9}   |
| {"col1":1997,"col2":10}  |
| {"col1":1997,"col2":11}  |
| {"col1":1997,"col2":12}  |
| {"col1":1998,"col2":1}   |
| {"col1":1998,"col2":2}   |
| {"col1":1998,"col2":3}   |
| {"col1":1998,"col2":4}   |
+--------------------------+
```

### 2.2.
```
select  count(*) total_count,  movietitle 
from movielens.movie_ratings 
where review_year=1998 AND review_month=4 
group by movietitle order by total_count desc limit 20;
+--------------+------------------------------+
| total_count  |          movietitle          |
+--------------+------------------------------+
| 63           | Titanic(1997)                |
| 52           | AirForceOne(1997)            |
| 50           | Contact(1997)                |
| 49           | FullMonty,The(1997)          |
| 49           | StarWars(1977)               |
| 42           | GoodWillHunting(1997)        |
| 41           | LiarLiar(1997)               |
| 41           | EnglishPatient,The(1996)     |
| 39           | AsGoodAsItGets(1997)         |
| 39           | ConspiracyTheory(1997)       |
| 37           | Scream(1996)                 |
| 36           | ToyStory(1995)               |
| 36           | Fargo(1996)                  |
| 36           | ReturnoftheJedi(1983)        |
| 35           | L.A.Confidential(1997)       |
| 34           | ChasingAmy(1997)             |
| 34           | Godfather,The(1972)          |
| 33           | Braveheart(1995)             |
| 33           | StarshipTroopers(1997)       |
| 33           | SilenceoftheLambs,The(1991)  |
+--------------+------------------------------+
```

### 2.3.
```
select avg(rating) as avg_rating, count(*) total_count,  movietitle 
from movielens.movie_ratings 
where review_year=1998 AND review_month=4 
group by movietitle order by avg_rating desc limit 20;

+-------------+--------------+-------------------------------------------+
| avg_rating  | total_count  |                movietitle                 |
+-------------+--------------+-------------------------------------------+
| 5.0         | 3            | CelluloidCloset,The(1995)                 |
| 5.0         | 1            | Boys,Les(1997)                            |
| 5.0         | 1            | Flirt(1995)                               |
| 5.0         | 1            | FreeWilly2:TheAdventureHome(1995)         |
| 5.0         | 1            | DeltaofVenus(1994)                        |
| 5.0         | 1            | CutthroatIsland(1995)                     |
| 5.0         | 1            | DunstonChecksIn(1996)                     |
| 5.0         | 2            | Diexueshuangxiong(Killer,The)(1989)       |
| 5.0         | 1            | Lassie(1994)                              |
| 5.0         | 1            | Innocents,The(1961)                       |
| 5.0         | 1            | Stalingrad(1993)                          |
| 5.0         | 1            | FearofaBlackHat(1993)                     |
| 5.0         | 1            | Trust(1990)                               |
| 5.0         | 1            | BoxingHelena(1993)                        |
| 5.0         | 1            | DavyCrockett,KingoftheWildFrontier(1955)  |
| 5.0         | 1            | BitterSugar(AzucarAmargo)(1996)           |
| 5.0         | 1            | BlueSky(1994)                             |
| 5.0         | 1            | Daylight(1996)                            |
| 5.0         | 2            | Prefontaine(1997)                         |
| 5.0         | 1            | 8Seconds(1994)                            |
+-------------+--------------+-------------------------------------------+
```



