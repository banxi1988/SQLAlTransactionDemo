# SQLAlchemy 事务

## 环境配置
1. 创建数据库

```bash
➜  ~ psql
psql (9.5.4)
Type "help" for help.

banxi=# create user bankapp with password '2017bank';
CREATE ROLE
banxi=# create database bank owner bankapp;
CREATE DATABASE
banxi=# grant all privileges on database bank to bankapp;
GRANT
banxi=#
```

2. 创建初始表

```sql
CREATE TABLE "public"."account" (
    "name" text,
    "amount" numeric(19,2) DEFAULT '0',
    PRIMARY KEY ("name")
);


```

3. 插入初始测试数据

```sql
INSERT INTO "public"."account"("name", "amount") VALUES('A', 500) RETURNING "name", "amount";
INSERT INTO "public"."account"("name", "amount") VALUES('B', 500) RETURNING "name", "amount";
```

上面的 步骤 2,3 在测试中会自动处理.


## 经典事务例子
 如上插入的数据:
 
 >账号 A: 余额 500 元
 账号 B: 余额 500 元
 
 现在需要从账号A 向 账号 B 转 100元.