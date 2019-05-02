

if __name__ == "__main__":
    from tedutil.calculator import load_algorithm
    from tedutil.calculator import calculate
    from tedutil.dec import dic2gr
    from tedutil.dec import dic_print
    from tedutil.files import file2data
    from tedutil.files import write2file
    # from tedutil.calculator import calc
    # alg = load_algorithm('algorithm-payroll.txt')
    # dat = {'IMEROMISTHIO': 60,
    #        'meres': 25,
    #        'POSOSTO-IKA': 44.15,
    #        'POSOSTO-IKA-ERGAZOMENOY': 14.98,
    #        'paidia': 3}
    # # print('\n'.join([f'{i.operator} {i.result} {i.pars}' for i in alg]))
    # print('\n'.join('%-30s: %9s' % (i, j)
    #                 for i, j in calculate(alg, dat).items()))
    # print(calc.registered())
    alg = load_algorithm('algorithm-f2.txt')
    dat = {'24.01.00.024': 1000,
           '24.01.00.000': 100,
           '71.00.00.024': 2000,
           'fpa': 240, 'V483': 20}
    # print('\n'.join([f'{i.operator} {i.result} {i.pars}' for i in alg]))
    result = calculate(alg, dat)
    gres = dic2gr(result)
    com = {'epon': "Somebody OE", 'onom': '', 'patr': '', 'afm': '123123123',
           'apo': '1/1/2018', 'eos': '31/3/2018'}
    finaldic = {**com, **gres}
    template = file2data("f2-template.html")
    dic_print(finaldic)
    ftxt = template.format(**finaldic)
    write2file(ftxt, "out.html")
