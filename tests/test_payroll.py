from tedutil import payroll as pay


def test_misthotos():
    mis = pay.Misthotos(740)
    assert mis.hmeromisthio == 29.6
    assert mis.oromisthio == 4.44
    assert mis.oromisthio_nyxta == 5.55
    assert mis.oromisthio_nyxta_p == 1.11
    apod = mis.apodoxes_periodoy(10, nyxta_ores=11)
    assert apod["total"] == 308.21
    assert mis.apodoxes_dpasxa(100)["total"] == 385.42
    assert mis.apodoxes_dpasxa(175)["total"] == 385.42
    assert mis.apodoxes_dxrist(200)["total"] == 770.84
    assert mis.apodoxes_dxrist(201)["total"] == 770.84
    assert mis.apodoxes_dxrist(999)["total"] == 770.84
    assert mis.apodoxes_astheneias(3)["total"] == 44.4
    assert mis.apodoxes_epadeias(150)["total"] == 370
    assert mis.apodoxes_epadeias(151)["total"] == 370
    assert mis.apodoxes_epadeias(300)["total"] == 370


def test_hmeromisthios():
    ime = pay.Hmeromisthios(29.6)
    assert ime.oromisthio == 4.44
    assert ime.oromisthio_nyxta == 5.55
    assert ime.oromisthio_nyxta_p == 1.11
    assert ime.apodoxes_periodoy(10, nyxta_ores=11)["total"] == 308.21
    assert ime.apodoxes_dpasxa(100)["total"] == 462.5
    assert ime.apodoxes_dpasxa(101)["total"] == 462.5
    assert ime.apodoxes_dpasxa(300)["total"] == 462.5
    assert ime.apodoxes_dxrist(200)["total"] == 770.84
    assert ime.apodoxes_dxrist(201)["total"] == 770.84
    assert ime.apodoxes_dxrist(300)["total"] == 770.84
    assert ime.apodoxes_astheneias(3)["total"] == 44.4
    assert ime.apodoxes_epadeias(150)["total"] == 384.8
    assert ime.apodoxes_epadeias(151)["total"] == 384.8
    assert ime.apodoxes_epadeias(300)["total"] == 384.8


def test_oromisthios():
    oro = pay.Oromisthios(4.44)
    assert oro.oromisthio == 4.44
    assert oro.hmeromisthio == 29.6
    assert oro.oromisthio_nyxta == 5.55
    assert oro.oromisthio_nyxta_p == 1.11
    assert oro.apodoxes_periodoy(167)["total"] == 741.48
    assert oro.apodoxes_dpasxa(4 * 167)["total"] == 386.19
    assert oro.apodoxes_dpasxa(4 * 167 + 1)["total"] == 386.19
    assert oro.apodoxes_dpasxa(4 * 167 + 999)["total"] == 386.19
    assert oro.apodoxes_dxrist(8 * 167)["total"] == 772.38
    assert oro.apodoxes_dxrist(8 * 167 + 1)["total"] == 772.38
    assert oro.apodoxes_dxrist(8 * 167 + 999)["total"] == 772.38
    assert oro.apodoxes_epadeias(12 * 167)["total"] == 370.74


def test_factories():
    assert pay.apod("mi", "ap", 750, meres=25)["total"] == 750
    assert pay.apod("mi", "dp", 750, meres=101)["total"] == 390.63
    # print(pay.apod("hm", "ap", 30, meres=10))
    # print(pay.apod("or", "ap", 7.5, ores=10))
