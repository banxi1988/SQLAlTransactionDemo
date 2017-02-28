# -*- coding: utf-8 -*-
import pytest
__author__ = 'banxi'

@pytest.fixture
def account_table():
    from bank.app import engine, metadata, account_table as accounts
    # 1) 重新创建表
    metadata.drop_all(engine)
    metadata.create_all(engine)

    # 2) 初始化表数据
    accounts.insert().values(name='A', amount=500)
    accounts.insert().values(name='B', amount=500)
    conn = engine.connect()
    conn.execute(accounts.insert(),[
        {'name': 'A','amount':500},
        {'name': 'B','amount':500},
    ])



    return accounts



