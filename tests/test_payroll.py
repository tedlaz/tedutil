from tedutil import payroll as pay


def test_misthotos():
    mis1 = pay.Misthotos(740)
    assert mis1.hmeromisthio == 29.6
    assert mis1.oromisthio == 4.44
    assert mis1.oromisthio_nyxta == 5.55
    assert mis1.oromisthio_nyxta_p == 1.11
    apod = mis1.apodoxes_periodoy(10, nyxta_ores=11)
    assert apod["total"] == 308.21
    assert mis1.apodoxes_dpasxa(100)["total"] == 385.42
    assert mis1.apodoxes_dpasxa(175)["total"] == 385.42
    assert mis1.apodoxes_dxrist(200)["total"] == 770.84
    assert mis1.apodoxes_dxrist(201)["total"] == 770.84
    assert mis1.apodoxes_dxrist(999)["total"] == 770.84
    assert mis1.apodoxes_astheneias(3)["total"] == 44.4


def test_hmeromisthios():
    mis2 = pay.Hmeromisthios(29.6)
    assert mis2.oromisthio == 4.44
    assert mis2.oromisthio_nyxta == 5.55
    assert mis2.oromisthio_nyxta_p == 1.11
    apod = mis2.apodoxes_periodoy(10, nyxta_ores=11)
    assert apod["total"] == 308.21
    assert mis2.apodoxes_dpasxa(100)["total"] == 462.5
    assert mis2.apodoxes_dpasxa(101)["total"] == 462.5
    assert mis2.apodoxes_dpasxa(300)["total"] == 462.5
    assert mis2.apodoxes_dxrist(200)["total"] == 770.84
    assert mis2.apodoxes_dxrist(201)["total"] == 770.84
    assert mis2.apodoxes_dxrist(300)["total"] == 770.84
    asth = mis2.apodoxes_astheneias(3)
    assert asth["total"] == 44.4


def test_oromisthios():
    mis3 = pay.Oromisthios(4.44)
    assert mis3.oromisthio == 4.44
    assert mis3.hmeromisthio == 29.6
    assert mis3.oromisthio_nyxta == 5.55
    assert mis3.oromisthio_nyxta_p == 1.11
