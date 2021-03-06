# -*- coding: utf-8 -*-
__author__ = 'banxi'

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, BigInteger, String, MetaData

SQLALCHEMY_DATABASE_URI = 'postgresql://bankapp:2017bank@localhost:5432/bank'

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

metadata = MetaData(engine)

account_table = Table('account',metadata,
                 Column('name',String, primary_key=True),
                 Column('amount', BigInteger, nullable=False, default=0)
                 )
metadata.create_all()


class Account(object):
    _conn = None

    @classmethod
    def get_conn(cls):
        if cls._conn and not cls._conn.closed:
            return cls._conn
        return engine.connect()

    def __init__(self,name, amount):
        self.name  = name
        self.amount = amount

    @classmethod
    def find_by_name(cls,name):
        from sqlalchemy.sql import select
        conn = cls.get_conn()
        stmt = select([account_table]).where(account_table.c.name == name)
        result = conn.execute(stmt)
        row = result.first()
        if row is None:
            return None
        return Account(row[account_table.c.name], row[account_table.c.amount])

    def save(self):
        stmt = account_table.update()\
            .where(account_table.c.name == self.name)\
            .values(amount=self.amount)
        conn = self.get_conn()
        result = conn.execute(stmt)
        return result.rowcount == 1


