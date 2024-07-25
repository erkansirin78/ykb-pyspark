### 1. Select test1 database
`use test1;`

### 2. Create simple table with default properties
```
create table if not exists test1.mytable(id int, user_name string, email array<string>);
```

### 3. Describe table
```
describe test1.mytable;
```

### 4. More information for table
```
describe formatted  test1.mytable;
```
### 5. drop table 
` drop table test1.mytable;`

### 6. Create table with properties

```
create table if not exists test1.mytable 
(id int, username string, email array<string>)
row format delimited
fields terminated by ','
collection items terminated by ':'
lines terminated by '\n'
stored as textfile;
```

### 7. generate create script from existing table
```
show create table test1.mytable;
```

## 8. Show tblproperties
```
 show tblproperties test1.mytable;
```