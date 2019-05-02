from tedutil.accounting.levels import levels


class Account:
    def __init__(self, code, name=None):
        self.code = code
        self.name = name or ""

    @property
    def levels(self):
        return levels(self.code)

    def __str__(self):
        return f"{self.code} {self.name}"

    def __repr__(self):
        return f"Account(code: {self.code}, name: {self.name})"
