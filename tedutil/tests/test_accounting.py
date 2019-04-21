from unittest import TestCase
import os
from tedutil import accounting as acc


class TestAccounting(TestCase):
    def test_acc1(self):
        dirc = os.path.dirname(__file__)
        pb0 = os.path.join(dirc, 'anoigma.txt')
        pb1 = os.path.join(dirc, 'lines.txt')
        pb2 = os.path.join(dirc, 'linsa.txt')
        book = acc.book_from_file(pb1)
        book.load_from_file(pb2)
        book.journal_print()
        b00 = acc.book_from_file(pb0)
        b00.isozygio_kinoymenon_print()
        fin = b00 + book
        fin.isozygio_kinoymenon_print()
        back = fin - b00
        book.isozygio_kinoymenon_print()
        back.isozygio_print()
        fin.isozygio_partner_print() # ('30.00.0000', '50.00.0000'))
        # fin.journal_print()
