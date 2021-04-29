from tedutil import grscc_book as grb


def test_account_level():
    assert grb.Account('38.00.00.001').level == 4
    assert grb.Account('Ταμείο.Μετρητά.Τσέπη').level == 3


def test_account_omada():
    assert grb.Account('38.00.00.001').omada == '3'
    assert grb.Account('Ταμείο.Μετρητά.Τσέπη').omada == 'Ταμείο'


def test_tranline():
    tr1 = grb.TranLine(grb.Account('30.00.01'), 100)
    assert tr1.debit == 100
    assert tr1.credit == 0
    tr2 = grb.TranLine(grb.Account('30.00.01'), -100)
    assert tr2.debit == 0
    assert tr2.credit == 100
    tr3 = tr1.new_reversed_tranline()
    assert tr2 == tr3


def test_tran():
    tn1 = grb.Tran('2021-02-01', 'ΤΔΑ34', 'Αγορές')
    acc = grb.Account('38.00.00.001')
    tn1.add_line(acc, 100)


def test_flyweight_acc():
    ac1 = grb.Account('38.00')
    acs = []
    for _ in range(1000):
        acs.append(grb.Account('38.01'))
    # ac3 = grb.Account('38.01', 'Ταμείο Κεντρικό')
    for _ in range(1000):
        acs.append(grb.Account('38.01'))
    print(dict(ac1._pool))
