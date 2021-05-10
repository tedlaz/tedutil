from collections import namedtuple

Tap = namedtuple("Tap", "normal argia_ores argia_meres nyxta total")


class Ergazomenos:
    WEEK_DAYS = 6
    WEEK_HOURS = 40
    NYXTA_PROS = 0.25
    ARGIA_PROS = 0.75

    @property
    def hmeromisthio(self):
        raise NotImplementedError

    @property
    def oromisthio(self):
        raise NotImplementedError

    @property
    def oromisthio_nyxta(self):
        """Ωρομίσθιο νύχτας συνολικό"""
        return round(self.oromisthio * (1 + self.NYXTA_PROS), 2)

    @property
    def oromisthio_nyxta_p(self):
        """Προσαύξηση ωρομισθίου νύχτας"""
        return round(self.oromisthio * self.NYXTA_PROS, 2)

    @property
    def oromisthio_argia(self):
        """Ωρομίσθιο αργίας συνολικό"""
        return round(self.oromisthio * (1 + self.ARGIA_PROS), 2)

    @property
    def oromisthio_argia_p(self):
        """Προσαύξηση ωρομισθίου αργίας"""
        return round(self.oromisthio * self.ARGIA_PROS, 2)

    @property
    def hmeromisthio_argia(self):
        """Ημερομίσθιο αργίας συνολικό"""
        return round(self.hmeromisthio * (1 + self.ARGIA_PROS), 2)

    @property
    def hmeromisthio_argia_p(self):
        """Προσαύξηση ημερομισθίου αργίας"""
        return round(self.hmeromisthio * self.ARGIA_PROS, 2)

    def apodoxes_periodoy(self, meres_ores):
        raise NotImplementedError


class Misthotos(Ergazomenos):
    MONTH_DAYS = 25

    def __init__(self, apodoxes):
        self._misthos = apodoxes

    @property
    def misthos(self):
        return self._misthos

    @property
    def hmeromisthio(self):
        return self.misthos / self.MONTH_DAYS

    @property
    def oromisthio(self):
        return self.hmeromisthio * self.WEEK_DAYS / self.WEEK_HOURS

    def apodoxes_periodoy(self, meres, argia_meres=0, argia_ores=0, nyxta_ores=0):
        a_normal = round(meres / self.MONTH_DAYS * self.misthos, 2)
        a_argia_meres = round(argia_meres * self.hmeromisthio_argia_p, 2)
        a_argia_ores = round(argia_ores * self.oromisthio_argia_p, 2)
        a_nyxta_ores = round(nyxta_ores * self.oromisthio_nyxta_p, 2)
        apod = round(a_normal + a_argia_meres + a_argia_ores + a_nyxta_ores, 2)
        return Tap(a_normal, a_argia_ores, a_argia_meres, a_nyxta_ores, apod)



class Hmeromisthios(Ergazomenos):
    MONTH_DAYS = 26

    def __init__(self, apodoxes):
        self._hmeromisthio = apodoxes

    @property
    def hmeromisthio(self):
        return self._hmeromisthio

    @property
    def misthos(self):
        self._hmeromisthio * self.MONTH_DAYS

    @property
    def oromisthio(self):
        return self.hmeromisthio * self.WEEK_DAYS / self.WEEK_HOURS

    def apodoxes_periodoy(self, meres, argia_meres=0, argia_ores=0, nyxta_ores=0):
        a_normal = round(meres * self.hmeromisthio, 2)
        a_argia_meres = round(argia_meres * self.hmeromisthio_argia_p, 2)
        a_argia_ores = round(argia_ores * self.oromisthio_argia_p, 2)
        a_nyxta_ores = round(nyxta_ores * self.oromisthio_nyxta_p, 2)
        apod = round(a_normal + a_argia_meres + a_argia_ores + a_nyxta_ores, 2)
        return {
            "apodoxes_meres": a_normal,
            "apodoxes_argia_ores": a_argia_ores,
            "apodoxes_argia_meres": a_argia_meres,
            "apodoxes_nyxta_ores": a_nyxta_ores,
            "apodoxes_periodoy": apod,
        }


class Oromisthios(Ergazomenos):
    def __init__(self, apodoxes):
        self._oromisthio = apodoxes

    @property
    def oromisthio(self):
        return self._oromisthio

    def apodoxes_periodoy(self, ores):
        return ores * self.oromisthio
