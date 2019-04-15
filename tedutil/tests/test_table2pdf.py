

if __name__ == "__main__":
    from tedutil.table2pdf import render2pdf
    from tedutil.files import read_csv_file
    import os
    from os.path import expanduser

    home = expanduser('~')
    pdff = os.path.join(expanduser('~'), 'tst.pdf')
    data = read_csv_file("mis.csv")
    dvl = dict()
    dvl['head'] = data[0]
    dvl['lns'] = data[1:]
    dvl['sum'] = ['', '', '', '', '123', '5.340,34', '856,98', '1.120,44',
                  '2.222,64', '', '', '270,00', '3.456,78']
    dvl['szs'] = [35, 200, 110, 80, 50, 90, 70, 80, 90, 70, 50, 80, 90]
    dvl['aln'] = [1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    dvl['footer'] = 'Μαλακόπουλος ΕΠΕ, Αγίου Βερνάρδου 35, Αθήνα TK:11234, ' \
                    'ΑΦΜ:123123123, Τηλέφωνο:210 88 23 456'
    render2pdf(pdff, 'ΜΙΣΘΟΔΟΣΙΑ ΜΑΡΤΙΟΥ 2019', dvl, is_portrait=False)
