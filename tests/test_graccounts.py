import os
import json
from unittest import TestCase
from tedutil import graccounts as gra

dir_path = os.path.dirname(os.path.realpath(__file__))


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
        # print(tr1.account_set, tr2.account_set)
        # print(tr2)
        acc = os.path.join(dir_path, 'acc.txt')
        book = gra.Book(acc)
        book.add_transaction_object(tr1)
        book.add_transaction_object(tr2)
        book.add_transaction_object(tr3)
        book.add_transaction_object(tr4)
        for trn in book.trans_ee():
            # print(trn.typos_set)
            # print(trn.is_ee, trn.is_fpa)
            pass
        # print(tr4, tr4.reverse('2021-02-17', 'pis34'))
        # print(tr4.as_dic)
        adi = {
            'dat': '2020-12-15',
            'par': 'ΑΛΠ21',
            'per': 'Δοκιμή',
            'z': [
                {'acc': '38.00', 'val': -1000},
                {'acc': '50.00', 'val': 1000}
            ]
        }
        ttt = gra.Transaction.from_dic(adi)
        # print(ttt)

    def test_json(self):
        fil = os.path.join(dir_path, 'graccount_data.json')
        acc = os.path.join(dir_path, 'acc.txt')
        with open(fil) as json_file:
            data = json.load(json_file)
        bok = gra.Book(acc)
        bok.add_trans_from_list_dic(data)
        # print(bok)
        # print(bok.as_list_of_dicts)
        # print('\n')
        # for trn in bok.transactions:
        #     print(trn.ee_type, trn.re)
        bok.check_account_validity()
        print(bok)
