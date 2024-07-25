### 1. insert a record with values  
`insert into test1.mytable values(2, "testuser2", array("testuser2@example.com")); `

### 2. insert a record with SELECT  
` insert into test1.mytable SELECT 1, "testuser1", array("testuser1@example.com"); `

### 3. insert a record with multiple array elements  
` insert into test1.mytable values(3, 'testuser3', array('testuser3@example.com:testuser3@gmail.com'));  `

### 4. insert multiple records
```
insert into table test1.mytable values 
(4, 'testuser4', array('testuser4@example.com:testuser4@gmail.com')),  
(5, 'testuser5', array('testuser5@example.com:testuser5@gmail.com'));
```

### 5. See inserted records
```
select * from test1.mytable;
```
