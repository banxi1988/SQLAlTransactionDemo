# -*- coding: utf-8 -*-

__author__ = 'banxi'

def test_sub_transaction_inner_rollback(account_table):
    """
       测试 这么一个过程, A 收到由 B 转过来的钱, 然后, A 还钱给 W.
       一开始他们都是 500 块钱.
       """
    from bank.app import engine, Account
    conn = engine.connect()
    Account._conn = conn
    ac_a = Account.find_by_name('A')
    ac_b = Account.find_by_name('B')
    ac_w = Account.find_by_name('W')

    assert ac_a.amount == 500
    assert ac_b.amount == 500
    assert ac_w.amount == 500

    def a_pay_money_to_w():
        with conn.begin_nested():
            ac_a.amount -= 100
            ac_a.save()
            ac_w.amount += 100
            ac_w.save()
            raise Exception("I Dont want to pay to W")

    def a_receive_salary_from_b():
        with conn.begin():
            ac_a.amount += 100
            ac_a.save()
            ac_b.amount -= 100
            ac_b.save()
            try:
                a_pay_money_to_w()
            except Exception as e:
                print(e)

    a_receive_salary_from_b()

    ac_a2 = Account.find_by_name('A')
    ac_b2 = Account.find_by_name('B')
    ac_w2 = Account.find_by_name('W')

    assert ac_a2.amount == 600
    assert ac_b2.amount == 400
    assert ac_w2.amount == 500


def test_sub_transaction_outer_rollback(account_table):
    """
       测试 这么一个过程, A 收到由 B 转过来的钱, 然后, A 还钱给 W.
       一开始他们都是 500 块钱.
       """
    from bank.app import engine, Account
    conn = engine.connect()
    Account._conn = conn
    ac_a = Account.find_by_name('A')
    ac_b = Account.find_by_name('B')
    ac_w = Account.find_by_name('W')

    assert ac_a.amount == 500
    assert ac_b.amount == 500
    assert ac_w.amount == 500

    def a_pay_money_to_w():
        with conn.begin_nested():
            ac_a.amount -= 100
            ac_a.save()
            ac_w.amount += 100
            ac_w.save()

    def a_receive_salary_from_b():
        with conn.begin():
            ac_a.amount += 100
            ac_a.save()
            ac_b.amount -= 100
            ac_b.save()
            a_pay_money_to_w()
            raise Exception("Bad Exception")


    try:
        a_receive_salary_from_b()
    except Exception as e:
        print(e)

    ac_a2 = Account.find_by_name('A')
    ac_b2 = Account.find_by_name('B')
    ac_w2 = Account.find_by_name('W')

    assert ac_a2.amount == 500
    assert ac_b2.amount == 500
    assert ac_w2.amount == 500