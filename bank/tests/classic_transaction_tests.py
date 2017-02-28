
def test_classic_transaction(account_table):
    from bank.app   import Account
    account_A = Account.find_by_name('A')
    account_B = Account.find_by_name('B')
    assert account_A
    assert account_B

    assert account_A.amount == 500
    assert account_B.amount == 500

    account_A.amount -= 100
    account_A.save()

    account_B.amount += 100
    account_B.save()

    account_A2 = Account.find_by_name('A')
    account_B2 = Account.find_by_name('B')
    assert account_A2.amount == 400
    assert account_B2.amount == 600



