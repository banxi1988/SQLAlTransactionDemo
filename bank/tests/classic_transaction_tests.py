
def test_classic_transaction_step1(account_table):
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


def test_classic_transaction_issue1(account_table):
    from bank.app   import Account
    # 1) read(A)
    account_A = Account.find_by_name('A')
    assert account_A
    assert account_A.amount == 500

    # 2)
    account_A.amount -= 100

    # 3) write(A)
    account_A.save()

    try:
        # 4) read(B)
        account_B = Account.find_by_name('B')
        raise Exception("Simulator read(B) Exception")
        assert account_B
        assert account_B.amount == 500

        # 5)
        account_B.amount += 100

        # 6) write(B)
        account_B.save()
    except Exception as e:
        print(e)

    account_A2 = Account.find_by_name('A')
    account_B2 = Account.find_by_name('B')
    assert account_A2.amount == 400
    assert account_B2.amount == 500


def test_classic_transaction_fix1(account_table):
    from bank.app   import Account, engine
    try:
        with engine.begin() as conn:
            Account._conn = conn
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
    except Exception as e:
        print(e)

    account_A2 = Account.find_by_name('A')
    account_B2 = Account.find_by_name('B')
    assert account_A2.amount == 500
    assert account_B2.amount == 500



