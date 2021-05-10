from tedutil import payroll as pay


def test_misthotos():
    mis1 = pay.Misthotos(740)
    assert mis1.hmeromisthio == 29.6
    assert mis1.oromisthio == 4.44
    assert mis1.oromisthio_nyxta == 5.55
    assert mis1.oromisthio_nyxta_p == 1.11
    apod = mis1.apodoxes_periodoy(10, nyxta_ores=11)
    print(apod.total)
