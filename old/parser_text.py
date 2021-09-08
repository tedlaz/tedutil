from decimal import Decimal as Dec
from collections import defaultdict


def gr2strdec(greek_number: str) -> str:
    """
    Greek number to text decimal
    '1.234,56' -> 1234.56
    """
    return greek_number.replace('.', '').replace(',', '.')


def gr2dec(greek_number: str) -> Dec:
    """
    Greek number to text decimal
    '1.234,56 ->' Decimal(1234.56)
    """
    return round(Dec(gr2strdec(greek_number)), 2)


def parse(file_name):
    """
    Parser for accounting text files
    """
    trn = None
    company_afm = ''
    company_name = ''
    transactions = []
    transaction_number = 0
    validations = []
    anoigma = []
    accounts_totals = defaultdict(Dec)
    accounts_ids = {}
    acc_id = 0
    trand_id = 0
    tran_total = 0

    with open(file_name) as fil:
        lines = fil.read().split('\n')

    for line in lines:
        rline = line.rstrip()

        # Αγνόησε τις κενές γραμμές
        if len(rline) == 0:
            continue

        # Αγνόησε τις γραμμές σχολίων
        elif rline.startswith('#'):
            continue

        # Στοιχεία εταιρείας (ΑΦΜ, Επωνυμία)
        elif rline.startswith('$'):
            _, co_afm, *co_name = rline.split()
            company_afm = co_afm
            company_name = ' '.join(co_name)

        # Εγγραφές ανοίγματος
        elif rline.startswith('<'):
            _, adate, accounta, value = rline.split()
            anoigma.append({'date': adate, 'account': accounta,
                            'ypoloipo': gr2dec(value)})

        # Γραμμή επιβεβαίωσης υπολοίπου
        elif rline.startswith(('@')):
            # @ 2020-05-10 Αγορές.Εμπορευμάτων.εσωτερικού -120,32
            _, cdat, cacc, cval = rline.split()
            validations.append(
                {'date': cdat, 'account': cacc, 'ypoloipo': gr2dec(cval)})

        # Γραμμή Head (Ημερομηνία EEEE-MM-DD γίνεται EEEEMMDD αριθμητικό)
        elif rline[:10].replace('-', '').isnumeric():
            # if status == LINE:
            #     self.add_transaction(trn)
            dat, par, _, per, *afma = rline.split('"')
            dat = dat.strip()
            par = par.strip()
            per = per.strip()
            afm = afma[0].strip() if afma else ''
            transaction_number += 1
            trn = {
                'id': transaction_number,
                'date': dat,
                'par': par,
                'per': per,
                'afm': afm,
                'lines': []
            }
            transactions.append(trn)
            tran_total = 0

        # Γραμμή λεπτομέρειας
        elif rline[:2] == '  ':  # Line detail
            account, *txtval = rline.split()
            if account not in accounts_ids:
                acc_id += 1
                accounts_ids[account] = acc_id
            val = gr2dec(txtval[0]) if txtval else 0
            if val:
                tran_total += val
            else:
                val = -tran_total
            trand_id += 1
            trn['lines'].append(
                {
                    'id': trand_id,
                    'account': account,
                    'acc_id': accounts_ids[account],
                    'value': val
                }
            )
            accounts_totals[account] += val
        else:  # Υπάρχουν γραμμές που ξεκινούν με μη αποδεκτό χαρακτήρα
            raise ValueError('Γραμμή που ξεκινάει από μη απόδεκτό χαρακτήρα')
    return {
        'afm': company_afm,
        'name': company_name,
        'transactions': transactions,
        'validations': validations,
        'accounts_totals': accounts_totals,
        'accounts_ids': accounts_ids,
        'anoigma': anoigma
    }


def isozygio_print(filename):
    res = parse(filename)
    tameio = 0
    acct = res['accounts_totals']
    for acc in sorted(acct):
        if acct[acc] != 0:
            print(f"{acc:50}{acct[acc]:>12,.2f}")
            if acc.startswith('Ταμείο'):
                tameio += acct[acc]
    print(f'Ταμείο: {tameio:,.2f}')


if __name__ == '__main__':
    isozygio_print('tedata')
