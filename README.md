
# udacity_log_analysis
log analysis....

## About the Project
It is a reporting tool which answers followin questions from new database
  1. What are the most popular three articles of all time?
  2. Who are the most popular article authors of all time?
  3. On which days did more than 1% of requests lead to errors?

## Requirements
- [x] Python 2
- [x] postgres sql
- [x] psycopg2 python library

## Procedure
1. Unzip the newsdata.zip to get the sql data file and make sure both python file and sql file in same directory
2. Then run the command ``` psql -d news -f newsdata.sql ```
3. You have successfully setup your data.
4. run the command ``` python udacitydb.py``` in the terminal to run the script.
5. You get the output..

## Creating view articlecount
```   
    create view articlecount as 
      select replace(split_part(path,'/',3),'-',' ') as pathtitle, count(*) as count 
      from log 
      where status like '200 OK' and  replace(split_part(path,'/',3),'-',' ') != ''
      group by path
      order by count desc;
 ```
 
 ## Creating view authorcount
 ```
  create view author count as
    select author,title,count from articlecount inner join articles 
    on upper(replace(replace(title,'''',''),'lot of','many')) 
    like upper(concat('%',split_part(pathtitle,' ',2),' ', split_part(pathtitle,' ',3),'%')) ;
 
 ```
