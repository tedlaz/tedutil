

if __name__ == "__main__":
    from tedutil.calculator import load_algorithm
    from tedutil.calculator import calculate
    from tedutil.calculator import calc
    alg = load_algorithm('algorithm-payroll.txt')
    dat = {'IMEROMISTHIO': 60,
           'meres': 25,
           'POSOSTO-IKA': 44.15,
           'POSOSTO-IKA-ERGAZOMENOY': 14.98,
           'paidia': 3}
    # print('\n'.join([f'{i.operator} {i.result} {i.pars}' for i in alg]))
    print('\n'.join('%-30s: %9s' % (i, j)
                    for i, j in calculate(alg, dat).items()))
    print(calc.registered())
