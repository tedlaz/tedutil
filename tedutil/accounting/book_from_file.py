"""Greek accounting module"""
from tedutil.dec import dec
from tedutil.files import file2data
from tedutil.accounting.book import Book
from tedutil.accounting.book import Transaction
from tedutil.accounting.config import COLSSP
from tedutil.accounting.config import HEADSP
from tedutil.accounting.config import LINSSP


def book_from_file(filename):
    """Read book from text file

    :param filename:
    :return:
    """
    data = file2data(filename)
    iter_lines = iter(data.split('\n'))
    book_data = [i.strip() for i in next(iter_lines).split(COLSSP)]
    _, afm, company_name, book_name, *_ = book_data
    book = Book(afm, company_name, book_name)

    for tr_line in iter_lines:

        if len(tr_line) < 5:
            continue

        if tr_line.startswith('1'):
            _, pafm, pname, *_ = [i.strip() for i in tr_line.split(COLSSP)]
            book.partners[pafm] = pname

        elif tr_line.startswith('2'):
            _, acode, acname, *_ = [i.strip() for i in tr_line.split(COLSSP)]
            book.chart[acode] = acname

        elif tr_line.startswith('9'):
            header, lines_data = tr_line.split(HEADSP)
            # print(header)
            lines = lines_data.split(LINSSP)
            # print(lines)
            hdata = [i.strip() for i in header.split(COLSSP)]
            line_code, atyp, date, par, per, main_partner, *_ = hdata
            trx = Transaction(date, par, per, main_partner, atyp)
            # trx = book.new_transaction(date, par, per, main_partner, atyp)
            # print(f"{date}, {par}, {per}, {main_partner}")
            for trd in lines:
                ldata = [i.strip() for i in trd.split(COLSSP)]
                code, typos, value, line_partner, *_ = ldata
                trx.add_line(code, int(typos), dec(value), line_partner)
                # print(f"   {code} {typos} {val:>12.2f} {line_partner}")
            book.save_transaction_to_book(trx)
    return book
