
def test_classic_transaction(account_table):
    from bank.app   import Account

    # 1) read(A)
    account_A = Account.find_by_name('A')
    assert account_A
    assert account_A.amount == 500

    # 2)
    account_A.amount -= 100

    # 3) write(A)
    account_A.save()

    # 4) read(B)
    raise Exception("Some Unkown Error")
    account_B = Account.find_by_name('B')
    assert account_B
    assert account_B.amount == 500

    # 5)
    account_B.amount += 100

    # 6) write(B)
    account_B.save()

    account_A2 = Account.find_by_name('A')
    account_B2 = Account.find_by_name('B')
    assert account_A2.amount == 400
    assert account_B2.amount == 600



