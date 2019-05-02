class Company:
    def __init__(self, afm, name):
        self.afm = afm
        self.name = name
        self.type = None
        self.city = ''

    def __repr__(self):
        return f"Company(afm: {self.afm}, name: {self.name})"
