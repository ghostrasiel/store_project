create database if not exists store_db character set = utf8 collate =utf8_unicode_ci;
use store_db ;

#產品DB
create table if not exists product 
(product_id int not null Primary key, 
name text not null ,
price float not null ,
commodity varchar(45) not null ,
pz_url text ,
description text ,
N_comments int, 
star_comments float) ;

#會員DB
create table if not exists member_db
(member_id varchar(45) not null Primary key, 
name varchar(45) not null ,
age int,
marital_status varchar(45),
income  varchar(45) , 
hh_comp varchar(45),
customer_picture varchar(45),
homeowner varchar(45) ,
household_size varchar(45),
kid_category varchar(45) , 
household varchar(45)) ;

#購物籃db
create table if not exists barsket
(member_id varchar(45) not null , 
product_id int not null , 
quantity int default 1, 
date datetime DEFAULT CURRENT_TIMESTAMP , 
transaction_id varchar(45) ,
constraint bm_mm foreign key(member_id) references member_db(member_id) , 
constraint bp_pp foreign key(product_id) references product(product_id));

#消費紀錄
create table if not exists transaction
(transaction_id varchar(45) not null , 
date datetime not null DEFAULT CURRENT_TIMESTAMP , 
sales_value float not null);

#測試
-- insert 	into product(product_id , name , price ,  commodity) values(111111 , 'apple' , 4.99 , 'food') ;
-- insert into member_db(member_id  , name) values ('A_123456','eric' ) ; 
-- insert 	into barsket(member_id , product_id ,quantity  ) values('A_123456' , 111111 , 2 ) ;
-- insert 	into barsket(member_id , product_id ) values('A_123456' , 111111 ) ; 
-- insert 	into transaction(transaction_id  , sales_value ) values('adsdad3r3d' , 9.98 ) ; 



