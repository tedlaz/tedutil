# from unittest import TestCase
import os
from tedutil import accounting as acc
# from tedutil.dec import dic_print


if __name__ == "__main__":
    dirc = os.path.dirname(__file__)
    book1 = acc.book_from_file(os.path.join(dirc, 'lines.txt'))
    book1.journal_print(date_to='2019-03-25')
    book2 = acc.book_from_file(os.path.join(dirc, 'anoigma.txt'))
    book2.journal_print()
    book3 = acc.book_from_file(os.path.join(dirc, 'linsa.txt'))
    book3.journal_print()
    b4 = book1 + book2 + book3
    b4.journal_print()
    b4.isozygio_print(date_from='2019-04-01', date_to='2019-12-31')
    b4.isozygio_kinoymenon_print()
    # print(book1.chart, book1.partners)
    # print(book1.trans[0].to_line())
    # b4.isozygio_partner_print(['30.00.0000', '50.00.0000'])
