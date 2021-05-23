import pickle


class Erg:
    def __init__(self, epo, ono):
        self.epo = epo
        self.ono = ono

    @property
    def onomatep(self):
        return f"{self.ono} {self.epo}"

    def __repr__(self):
        return f"Erg(eponymo='{self.epo}', onoma='{self.ono}')"


class Names:
    def __init__(self, filename="names.pickle"):
        self.filename = filename
        self.ergs = []

    def add_erg(self, erg_epo, erg_ono):
        self.ergs.append(Erg(erg_epo, erg_ono))
        # this is a test

    def __repr__(self):
        return f"Names(file: '{self.filename}', ergs: {self.ergs})"

    def save(self):
        with open(self.filename, "bw") as fil:
            pickle.dump(self, fil)


# def test_01():
#     names = Names()
#     names.add_erg("Lazaros", "Ted")
#     names.add_erg("Dazea", "Popi")
#     print(names)
#     names.save()

#     with open("names.pickle", "br") as fil:
#         nnames = pickle.load(fil)

#     print(nnames)
