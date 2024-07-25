## 1. Create database
` create database if not exists test1; ` 

## 2. List databases
```
show databases;
+----------------+
| database_name  |
+----------------+
| default        |
| test1          |
+----------------+
```

## 3. Describe database
```
 describe database test1;
+----------+----------+----------------------------------------------------+-------------+-------------+-------------+
| db_name  | comment  |                      location                      | owner_name  | owner_type  | parameters  |
+----------+----------+----------------------------------------------------+-------------+-------------+-------------+
| test1    |          | hdfs://cluster-master:9000/user/hive/warehouse/test1.db | root        | USER        |             |
+----------+----------+----------------------------------------------------+-------------+-------------+-------------+
1 row selected (0.324 seconds)
```

## 4. Drop database
```
0: jdbc:hive2://cluster-master:10000> drop database test1;
No rows affected (0.359 seconds)
0: jdbc:hive2://cluster-master:10000> show databases;
+----------------+
| database_name  |
+----------------+
| default        |
+----------------+
1 row selected (0.134 seconds)
```

- **If we want to delete database including the all tables in it**
` DROP DATABASE database_name CASCADE; `

## 5. We can add comments to databases
```
create database if not exists test1 comment 'This db is for big data training.';
No rows affected (0.085 seconds)
+----------+------------------------------------+----------------------------------------------------+-------------+-------------+-------------+
| db_name  |              comment               |                      location                      | owner_name  | owner_type  | parameters  |
+----------+------------------------------------+----------------------------------------------------+-------------+-------------+-------------+
| test1    | This db is for big data training.  | hdfs://cluster-master:9000/user/hive/warehouse/test1.db | root        | USER        |             |
+----------+------------------------------------+----------------------------------------------------+-------------+-------------+-------------+
1 row selected (0.113 seconds)
```

## 6. What happens when we create database?
- db hdfs location 
- Metadata
- File and metadata ownership