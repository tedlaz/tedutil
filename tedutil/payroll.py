"""Greek Payroll classes"""


class Ergazomenos:
    WEEK_DAYS = 6
    WEEK_HOURS = 40
    NYXTA_PROS = 0.25
    ARGIA_PROS = 0.75
    DORO_PROS = 0.04167

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

    def apodoxes_dpasxa(self):
        raise NotImplementedError

    def apodoxes_dxrist(self, meres_ores):
        raise NotImplementedError

    def apodoxes_epadeias(self, meres_ores):
        raise NotImplementedError

    def apodoxes_astheneias(self, meres_l3=0, meres_m3=0, apozimiosi_efka=0):
        """Αποδοχές ασθενείας"""
        apl3 = round(self.hmeromisthio * meres_l3 / 2, 2)
        apm3 = round(self.hmeromisthio * meres_m3, 2)
        total = round(apl3 + apm3, 2)
        return {"total": total, "apozimiosi": apozimiosi_efka}

    def selector(self, sel, **args):
        if sel == "ap":
            return self.apodoxes_periodoy(**args)
        elif sel == "dp":
            return self.apodoxes_dpasxa(**args)
        elif sel == "dx":
            return self.apodoxes_dxrist(**args)
        elif sel == "ea":
            return self.apodoxes_epadeias(**args)
        elif sel == "aa":
            return self.apodoxes_astheneias(**args)
        elif sel == "apolysi":
            pass
        else:
            raise ValueError(f"value {sel} for parameter sel is invalid")


class Misthotos(Ergazomenos):
    MONTH_DAYS = 25
    TYPOS = "misthotos"

    def __init__(self, apodoxes):
        self._misthos = apodoxes

    @property
    def misthos(self):
        """Μισθωτοί: Μισθός"""
        return self._misthos

    @property
    def hmeromisthio(self):
        """Μισθωτοί: Ημερομίσθιο"""
        return self.misthos / self.MONTH_DAYS

    @property
    def oromisthio(self):
        """Μισθωτοί: Ωρομίσθιο"""
        return self.hmeromisthio * self.WEEK_DAYS / self.WEEK_HOURS

    def apodoxes_periodoy(
        self, meres, ores=0, argia_meres=0, argia_ores=0, nyxta_ores=0
    ):
        """Μισθωτοί: Αποδοχές Περιόδου"""
        a_meres = round(meres / self.MONTH_DAYS * self.misthos, 2)
        a_ores = round(self.oromisthio * ores, 2)
        a_argia_meres = round(argia_meres * self.hmeromisthio_argia_p, 2)
        a_argia_ores = round(argia_ores * self.oromisthio_argia_p, 2)
        a_nyxta_ores = round(nyxta_ores * self.oromisthio_nyxta_p, 2)
        apod = round(a_meres + a_ores + a_argia_meres + a_argia_ores + a_nyxta_ores, 2)
        return {
            "erg_type": self.TYPOS,
            "mis_type": "apodoxes_periodoy",
            "meres": meres,
            "extra_ores": ores,
            "argia_meres": argia_meres,
            "argia_ores": argia_ores,
            "nyxta_ores": nyxta_ores,
            "meres_ika": meres,
            "argies_ika": argia_meres,
            "apodoxes_meres": a_meres,
            "apodoxes_ores": a_ores,
            "apodoxes_argia_ores": a_argia_ores,
            "apodoxes_argia_meres": a_argia_meres,
            "apodoxes_nyxta": a_nyxta_ores,
            "total": apod,
        }

    def apodoxes_dpasxa(self, meres):
        """Μισθωτοί: Αποδοχές Δώρου Πάσχα"""
        fmeres = meres if meres < 100 else 100
        apod = round(self.misthos / 2 * fmeres / 100, 2)
        pros = round(apod * self.DORO_PROS, 2)
        tot = apod + pros
        return {
            "erg_type": self.TYPOS,
            "mis_type": "apodoxes_dpasxa",
            "meres_periodoy": fmeres,
            "meres_ika": 0,
            "argies_ika": 0,
            "apodoxes_doroy": apod,
            "prosafksisi": pros,
            "total": tot,
        }

    def apodoxes_dxrist(self, meres):
        """Μισθωτοί: Αποδοχές Δώρου Χριστουγέννων"""
        fmeres = meres if meres < 200 else 200
        apod = round(self.misthos * fmeres / 200, 2)
        pros = round(apod * self.DORO_PROS, 2)
        tot = apod + pros
        return {
            "erg_type": self.TYPOS,
            "mis_type": "apodoxes_dxrist",
            "meres_periodoy": fmeres,
            "meres_ika": 0,
            "argies_ika": 0,
            "apodoxes_doroy": apod,
            "prosafksisi": pros,
            "total": tot,
        }

    def apodoxes_epadeias(self, meres):
        """Μισθωτοί: Αποδοχές επιδόματος αδείας"""
        fmeres = meres if meres < 150 else 150
        apod = round(self.misthos / 2 * fmeres / 150, 2)
        return {
            "erg_type": self.TYPOS,
            "mis_type": "apodoxes_epadeias",
            "meres_ika": 0,
            "argies_ika": 0,
            "total": apod,
        }

    def apozimiosi_apolysis(self, proslipsi_date):
        """Μισθωτοί: Αποζημίωση απόλυσης"""
        return {
            "erg_type": self.TYPOS,
            "mis_type": "apozimiosi_apolysis",
        }


class Hmeromisthios(Ergazomenos):
    MONTH_DAYS = 26
    TYPOS = "hmeromisthios"

    def __init__(self, apodoxes):
        self._hmeromisthio = apodoxes

    @property
    def hmeromisthio(self):
        """Ημερομίσθιοι: Ημερομίσθιο"""
        return self._hmeromisthio

    @property
    def misthos(self):
        """Ημερομίσθιοι: Μισθός (Ημερομίσθιο Χ 26 ημέρες)"""
        self._hmeromisthio * self.MONTH_DAYS

    @property
    def oromisthio(self):
        """Ημερομίσθιοι: Ωρομίσθιο"""
        return self.hmeromisthio * self.WEEK_DAYS / self.WEEK_HOURS

    def apodoxes_periodoy(
        self, meres, ores=0, argia_meres=0, argia_ores=0, nyxta_ores=0
    ):
        """Ημερομίσθιοι: Αποδοχές περιόδου"""
        a_meres = round(meres * self.hmeromisthio, 2)
        a_ores = round(self.oromisthio * ores, 2)
        a_argia_meres = round(argia_meres * self.hmeromisthio_argia_p, 2)
        a_argia_ores = round(argia_ores * self.oromisthio_argia_p, 2)
        a_nyxta_ores = round(nyxta_ores * self.oromisthio_nyxta_p, 2)
        apod = round(a_meres + a_ores + a_argia_meres + a_argia_ores + a_nyxta_ores, 2)
        return {
            "erg_type": self.TYPOS,
            "mis_type": "apodoxes_periodoy",
            "meres": meres,
            "extra_ores": ores,
            "argia_meres": argia_meres,
            "argia_ores": argia_ores,
            "nyxta_ores": nyxta_ores,
            "meres_ika": meres,
            "argies_ika": argia_meres,
            "apodoxes_meres": a_meres,
            "apodoxes_ores": a_ores,
            "apodoxes_argia_ores": a_argia_ores,
            "apodoxes_argia_meres": a_argia_meres,
            "apodoxes_nyxta": a_nyxta_ores,
            "total": apod,
        }

    def apodoxes_dpasxa(self, meres):
        """Ημερομίσθιοι: Αποδοχές Δώρου Πάσχα"""
        fmeres = meres if meres < 100 else 100
        apod = round(self.hmeromisthio * 15 * fmeres / 100, 2)
        pros = round(apod * self.DORO_PROS, 2)
        tot = apod + pros
        return {
            "erg_type": self.TYPOS,
            "mis_type": "apodoxes_dpasxa",
            "meres_periodoy": fmeres,
            "meres_ika": 0,
            "argies_ika": 0,
            "apodoxes_doroy": apod,
            "prosafksisi": pros,
            "total": tot,
        }

    def apodoxes_dxrist(self, meres):
        """Ημερομίσθιοι: Αποδοχές Δώρου Χριστουγέννων"""
        fmeres = meres if meres < 200 else 200
        apod = round(self.hmeromisthio * 25 * fmeres / 200, 2)
        pros = round(apod * self.DORO_PROS, 2)
        tot = apod + pros
        return {
            "erg_type": self.TYPOS,
            "mis_type": "apodoxes_dxrist",
            "meres_periodoy": fmeres,
            "meres_ika": 0,
            "argies_ika": 0,
            "apodoxes_doroy": apod,
            "prosafksisi": pros,
            "total": tot,
        }

    def apodoxes_epadeias(self, meres):
        """Ημερομίσθιοι: Αποδοχές Επιδόματος Αδείας"""
        fmeres = meres if meres < 150 else 150
        apod = self.hmeromisthio * 13 * fmeres / 150
        return {
            "erg_type": self.TYPOS,
            "mis_type": "apodoxes_epadeias",
            "meres_ika": 0,
            "argies_ika": 0,
            "total": apod,
        }

    def apozimiosi_apolysis(self, proslipsi_date):
        """Ημερομίσθιοι: Αποζημίωση απόλυσης"""
        return {
            "erg_type": self.TYPOS,
            "mis_type": "apozimiosi_apolysis",
        }


class Oromisthios(Ergazomenos):
    max_month_ores = 167
    TYPOS = "oromisthios"

    def __init__(self, apodoxes):
        self._oromisthio = apodoxes

    @property
    def oromisthio(self):
        """Ωρομίσθιοι: Ωρομίσθιο"""
        return self._oromisthio

    @property
    def hmeromisthio(self):
        """Ωρομίσθιοι: Ημερομίσθιο (με αναγωγή στις 6,67 ώρες/μέρα)"""
        return round(self.oromisthio * self.WEEK_HOURS / self.WEEK_DAYS, 2)

    @property
    def misthos(self):
        raise NotImplementedError("Δεν έχουν μισθό οι ωρομίσθιοι")

    def apodoxes_periodoy(self, ores, argia_ores=0, nyxta_ores=0):
        """Ωρομίσθιοι: Αποδοχές περιόδου"""
        # assert meres == 0
        # assert argia_meres == 0
        a_ores = round(self.oromisthio * ores, 2)
        a_argia_ores = round(argia_ores * self.oromisthio_argia_p, 2)
        a_nyxta_ores = round(nyxta_ores * self.oromisthio_nyxta_p, 2)
        apod = round(a_ores + a_argia_ores + a_nyxta_ores, 2)
        return {
            "erg_type": self.TYPOS,
            "mis_type": "apodoxes_periodoy",
            "ores": ores,
            "argia_ores": argia_ores,
            "nyxta_ores": nyxta_ores,
            "meres_ika": 0,  # Εδώ να μπεί ο σωστός υπολογισμός ημερών
            "argies_ika": 0,  # και εδώ
            "apodoxes_ores": a_ores,
            "apodoxes_argia_ores": a_argia_ores,
            "apodoxes_nyxta": a_nyxta_ores,
            "total": apod,
        }

    def apodoxes_dpasxa(self, ores):
        """Ωρομίσθιοι: Αποδοχές Δώρου Πάσχα"""
        total_ores = 4 * self.max_month_ores
        ores = ores if ores <= total_ores else total_ores
        # Aποδοχές από 01-Ιανουαρίου έως 30-Απριλίου / 8 Χ 1,04166
        apod = round(ores * self.oromisthio / 8, 2)
        pros = round(apod * self.DORO_PROS, 2)
        tot = apod + pros
        return {
            "erg_type": self.TYPOS,
            "mis_type": "apodoxes_dpasxa",
            "ores_periodoy": total_ores,
            "meres_ika": 0,
            "argies_ika": 0,
            "apodoxes_doroy": apod,
            "prosafksisi": pros,
            "total": tot,
        }

    def apodoxes_dxrist(self, ores):
        """Ωρομίσθιοι: Αποδοχές Δώρου Χριστουγέννων"""
        total_ores = 8 * self.max_month_ores
        ores = ores if ores <= total_ores else total_ores
        # Αποδοχές από 01-Μαίου έως 31-Δεκεμβρίου / 8 Χ 1,04166
        apod = round(ores * self.oromisthio / 8, 2)
        pros = round(apod * self.DORO_PROS, 2)
        tot = apod + pros
        return {
            "erg_type": self.TYPOS,
            "mis_type": "apodoxes_dxrist",
            "ores_periodoy": ores,
            "meres_ika": 0,
            "argies_ika": 0,
            "apodoxes_doroy": apod,
            "prosafksisi": pros,
            "total": tot,
        }

    def apodoxes_epadeias(self, ores):
        """Ωρομίσθιοι: Αποδοχές Επιδόματος Αδείας"""
        total_ores = 6 * self.max_month_ores
        ores = ores if ores <= total_ores else total_ores
        apod = round(ores * self.oromisthio / 12, 2)
        return {
            "erg_type": self.TYPOS,
            "mis_type": "apodoxes_epadeias",
            "meres_ika": 0,
            "argies_ika": 0,
            "total": apod,
        }

    def apozimiosi_apolysis(self, proslipsi_date):
        """Ωρομίσθιοι: Αποζημίωση απόλυσης"""
        return {
            "erg_type": self.TYPOS,
            "mis_type": "apozimiosi_apolysis",
        }


# Factory methods here
ety = {"mi": Misthotos, "hm": Hmeromisthios, "or": Oromisthios}


def apod(erg_type, ap_type, apod, **arg):
    """
    ap_type: ap, dp, dx, ea, aa apolysi
    """
    erg = ety.get(erg_type, Misthotos)(apod)
    return erg.selector(ap_type, **arg)
