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
 
现在需要从账号A 向 账号 B 转 100元. 需要六个步骤, 伪代码表示如下:
 
```sql
BEGIN 
1. read(A)
2. A:= A - 100
3. write(A)
4. read(B)
5. B:= B + 100
6. write(B) 
COMMIT 
```
 
 
1. 直接操作不用事务, 也没有异常. 见代码 `step1`
 
2. 在 步骤 4 时出错, 直接模拟抛出一个异常, 执行测试之后. 
  `A:400`, `B:500` 也就是 A 的余额减少了,但是由于操作错误, B 中的余额没有增加. 见代码 `issue1`

3. 为了避免上面的错误. 使用事务来处理,这样即使出错,也是整个操作回滚. 见代码 `fix1` 中的 `test_classic_transaction_fix1`

### 小结
对于 SQLAlchemy Core 来说,典型的事物使用方法如下:

```python
connection = engine.connect()
trans = connection.begin()
try:
    # execute some thing
    trans.commit()
except:
    trans.rallback()
    raise 
```
可以通过使用 context manager 来简化:

1. 直接使用 `engine.begin()`
```python
with engine.begin() as conn:
    # exectue some thing
```

2. 使用 `connection.begin()`

```python
with connection.begin() as trans:
    # execute some thing
```



## 嵌套事务
在 `test_nested_transaction` 中 有嵌套的事务. 实际执行之后,观察到输出如下:

```python
2017-02-28 16:52:23,930 INFO sqlalchemy.engine.base.Engine BEGIN (implicit)
2017-02-28 16:52:23,930 INFO sqlalchemy.engine.base.Engine UPDATE account SET amount=%(amount)s WHERE account.name = %(name_1)s
2017-02-28 16:52:23,930 INFO sqlalchemy.engine.base.Engine {'amount': 600L, 'name_1': u'A'}
2017-02-28 16:52:23,931 INFO sqlalchemy.engine.base.Engine UPDATE account SET amount=%(amount)s WHERE account.name = %(name_1)s
2017-02-28 16:52:23,931 INFO sqlalchemy.engine.base.Engine {'amount': 400L, 'name_1': u'B'}
2017-02-28 16:52:23,931 INFO sqlalchemy.engine.base.Engine UPDATE account SET amount=%(amount)s WHERE account.name = %(name_1)s
2017-02-28 16:52:23,931 INFO sqlalchemy.engine.base.Engine {'amount': 500L, 'name_1': u'A'}
2017-02-28 16:52:23,932 INFO sqlalchemy.engine.base.Engine UPDATE account SET amount=%(amount)s WHERE account.name = %(name_1)s
2017-02-28 16:52:23,932 INFO sqlalchemy.engine.base.Engine {'amount': 600L, 'name_1': u'W'}
2017-02-28 16:52:23,932 INFO sqlalchemy.engine.base.Engine COMMIT
```
可见在嵌套的事务中,最终是被摊平了.内层的 commit 并不是引导整个事务的 commit.

但是 内层的 事务的 rollback 会导致外层事务的 rollback. 见 testcase `test_nested_transaction_inner_rollback`