from tedutil.accounting.book import Book
from tedutil.accounting.transaction import Transaction
from tedutil.fake_data_generator import generate_financial


def sale(date, poso, par, afm):
    tr1 = Transaction(date, par, 'Πωλήσεις εμπορευμάτων', afm)
    tr1.add_line('70.00.7024', 2, poso)
    tr1.add_line('54.00.7024', 2, poso * .24)
    tr1.add_final_line('30.00.0001')
    return tr1


def expense(date, poso, par, afm):
    tr1 = Transaction(date, par, 'Έξοδα χρήσης', afm)
    tr1.add_line('64.00.0024', 1, poso)
    tr1.add_line('54.00.2924', 1, poso * .24)
    tr1.add_final_line('50.00.0000')
    return tr1


def simulate_poliseis():
    vls = generate_financial('2018-01-01', '2018-12-31', 200, 20,
                             max_value=30)
    book = Book('111111111', 'Test Co', 'Poliseis')
    for val in vls:
        book.save_transaction_to_book(sale(val.date, val.val,
                                           "TIM%s" % val.par, val.afm))
    # book.isozygio_print()
    # book.isozygio_partner_print()
    book.to_lines()


if __name__ == "__main__":
    simulate_poliseis()
