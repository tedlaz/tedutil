from unittest import TestCase
from tedutil import graccounts as gra


class TestGraccounts(TestCase):
    def test_levels(self):
        self.assertEqual(
            gra.levels('10.00.00'), ('1', '10', '10.00', '10.00.00')
        )
        self.assertEqual(
            gra.levels_reverse('10.00.00'), ('10.00.00', '10.00', '10', '1')
        )
        self.assertEqual(
            gra.levels('this.is.it'), ('this', 'this.is', 'this.is.it')
        )

    def test_transaction_line(self):
        tr1 = gra.TransactionLine('10.00', -10)
        self.assertEqual(tr1.debit, 0)
        self.assertEqual(tr1.credit, 10)
        self.assertEqual(tr1.debit_negative, -10)
        self.assertEqual(tr1.credit_negative, 0)
        tr2 = gra.TransactionLine('10.00', 10)
        self.assertEqual(tr2.debit, 10)
        self.assertEqual(tr2.credit, 0)
        self.assertEqual(tr2.debit_negative, 0)
        self.assertEqual(tr2.credit_negative, -10)

    def test_transaction(self):
        tr1 = gra.Transaction('2021-01-12', 'TDA23', 'Test1')
        self.assertFalse(tr1.is_ok)
        tr1.add_line('20.00.00.024', 100)
        tr1.add_line('54.00.20.024', 24)
        tr1.add_line('50.00.00.001', -124)
        self.assertTrue(tr1.is_ok)
        tr2 = gra.Transaction('2021-02-15', 'TDA44', 'Test2')
        tr2.add_line('70.00.00.024', -100)
        tr2.add_line('54.00.70.024', -24)
        tr2.add_final_line('30.00.00.001')
        self.assertTrue(tr2.is_ok)
        tr3 = gra.Transaction('2021-02-16', 'LE', 'test3')
        tr3.add_line('38.00.00.001', 100)
        tr3.add_final_line('50.00.00.001')
        tr4 = gra.Transaction('2021-02-17', 'L3', 'test4')
        tr4.add_lines([('20.00.00', 100), ('38.03.00',)])
        print(tr1.account_set, tr2.account_set)
        print(tr2)
        book = gra.Book(2021)
        book.add_transaction_object(tr1)
        book.add_transaction_object(tr2)
        book.add_transaction_object(tr3)
        book.add_transaction_object(tr4)
        for trn in book.trans_ee():
            print(trn.typos_set)
            print(trn.is_ee, trn.is_fpa)
