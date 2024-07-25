### Let's backup mytable
` create table test1.mytable_bckp as select * from test1.mytable; `  

### 1. Change table name (rename)
```
alter table test1.

 show tables;
+--------------------------+
|         tab_name         |
+--------------------------+
| adv_lk                   |
| advertising              |
| advertising_sales_gt_20  |
| mytable                  |
| mytable_bckp             |
+--------------------------+


 alter table test1.mytable rename to test1.mytable_renamed;


 show tables;
+--------------------------+
|         tab_name         |
+--------------------------+
| adv_lk                   |
| advertising              |
| advertising_sales_gt_20  |
| mytable_bckp             |
| mytable_renamed          |
+--------------------------+

```

### 2. add new column
```
alter table test1.mytable_renamed add columns (added_col1 int);

select * from test1.mytable_renamed limit 3;
2       testuser2       ["testuser2@example.com"]       NULL
1       testuser1       ["testuser1@example.com"]       NULL
3       testuser3       ["testuser3@example.com","testuser3@gmail.com"] NULL
```

### 3. change column name, datatype
- We have decided that added_col1 should be phone_number.
```
alter table test1.mytable_renamed change added_col1 phone_number string;


# See the change
  describe test1.mytable_renamed;
OK
id                      int
username                string
email                   array<string>
phone_number            string
```

### 4. Add or change table properties.
```
 ALTER TABLE test1.mytable_renamed SET TBLPROPERTIES ('comment' = 'this is added via alter table');
No rows affected (0.112 seconds)

# alter comment
 show tblproperties test1.mytable_renamed;
+------------------------+--------------------------------+
|       prpt_name        |           prpt_value           |
+------------------------+--------------------------------+
| COLUMN_STATS_ACCURATE  | {"BASIC_STATS":"true"}         |
| bucketing_version      | 2                              |
| comment                | this is added via alter table  |
| last_modified_by       | train                          |
| last_modified_time     | 1604342471                     |
| numFiles               | 2                              |
| numRows                | 2                              |
| rawDataSize            | 66                             |
| totalSize              | 68                             |
| transient_lastDdlTime  | 1604342471                     |
+------------------------+--------------------------------+

# add new property
 ALTER TABLE test1.mytable_renamed SET TBLPROPERTIES ('some_freak_property' = 'some freak value');
No rows affected (0.112 seconds)

 show tblproperties test1.mytable_renamed;
+------------------------+--------------------------------+
|       prpt_name        |           prpt_value           |
+------------------------+--------------------------------+
| COLUMN_STATS_ACCURATE  | {"BASIC_STATS":"true"}         |
| bucketing_version      | 2                              |
| comment                | this is added via alter table  |
| last_modified_by       | train                          |
| last_modified_time     | 1604342563                     |
| numFiles               | 2                              |
| numRows                | 2                              |
| rawDataSize            | 66                             |
| some_freak_property    | some freak value               |
| totalSize              | 68                             |
| transient_lastDdlTime  | 1604342563                     |
+------------------------+--------------------------------+
```
