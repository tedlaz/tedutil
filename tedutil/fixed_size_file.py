"""Library to read and write fixed size text data files
"""
from decimal import Decimal as dec
import os
from tedutil.grtext import grup


class FixedSizeField:
    """""Abstract class""" ""

    def __init__(self, siz) -> None:
        self.length = siz

    def text(self, val):
        raise NotImplementedError

    def revert(self, textVal):
        raise NotImplementedError


class StaticField(FixedSizeField):
    """Just a fixed value ABCD -> ABCD"""

    def __init__(self, val) -> None:
        self.val = grup(val)
        super().__init__(len(self.val))

    def text(self, _) -> str:
        return self.val

    def revert(self, txtval) -> str:
        assert txtval == self.val
        return txtval


class Filler(FixedSizeField):
    """Fill with a specific char"""

    def __init__(self, siz, val) -> None:
        super().__init__(siz)
        self.val = str(val)

    def text(self, _) -> str:
        return self.val * self.length

    def revert(self, txtval: str) -> str:
        return txtval[0]


class ZeroesTextField(FixedSizeField):
    """123 -> '0000123'"""

    def text(self, val) -> str:
        txt = str(val)
        txt_len = len(txt)
        if txt_len > self.length:
            raise ValueError("text length is bigger than allowed")
        zeroes = "0" * (self.length - txt_len)
        return zeroes + txt

    def revert(self, txtval: str) -> str:
        return txtval.strip().lstrip("0")


class Decimal2Field(FixedSizeField):
    """Decimal with 2 decimal digits 123.45 -> '0000012345'"""

    def text(self, val) -> str:
        txt = str(round(dec(val), 2)).replace(".", "")
        txt_len = len(txt)
        if txt_len > self.length:
            raise ValueError("text length is bigger than allowed")
        zeroes = "0" * (self.length - txt_len)
        return zeroes + txt

    def revert(self, txtval) -> dec:
        return round(dec(txtval.strip().lstrip("0")) / dec(100), 2)


class TextSpacesField(FixedSizeField):
    """'abc' -> 'abc    '"""

    def text(self, val) -> str:
        txt = grup(val)
        txt_len = len(txt)
        if txt_len > self.length:
            raise ValueError("text length is bigger than allowed")
        spaces = " " * (self.length - txt_len)
        return txt + spaces

    def revert(self, txtval: str) -> str:
        return txtval.strip()


class SpacesTextField(FixedSizeField):
    """'abc' -> '    abc'"""

    def text(self, val) -> str:
        txt = grup(val)
        txt_len = len(txt)
        if txt_len > self.length:
            raise ValueError("text length is bigger than allowed")
        spaces = " " * (self.length - txt_len)
        return spaces + txt

    def revert(self, txtval: str) -> str:
        return txtval.strip()


class Date2dmyField(FixedSizeField):
    """Iso date to text YYYY-MM-DD -> DDMMYYYY"""

    def __init__(self):
        super().__init__(8)

    def text(self, isodate: str) -> str:
        assert len(isodate) == 10
        year, month, day = isodate.split("-")
        return f"{day}{month}{year}"

    def revert(self, txtval: str) -> str:
        day = txtval[:2]
        month = txtval[2:4]
        year = txtval[4:]
        return f"{year}-{month}-{day}"


class Date2ymdField(FixedSizeField):
    """Iso date to text YYYY-MM-DD -> YYYYMMDD"""

    def __init__(self):
        super().__init__(8)

    def text(self, isodate: str) -> str:
        assert len(isodate) == 10
        year, month, date = isodate.split("-")
        return f"{year}{month}{date}"

    def revert(self, txtval: str) -> str:
        year = txtval[:4]
        month = txtval[4:6]
        day = txtval[6:]
        return f"{year}-{month}-{day}"


def fld(fname: str, **pars):
    """Factory to create fields

    Args:
        fname (str): static(val), fill(siz, val),
        dec2(siz), _txt(siz), txt_(siz), dmy(), ymd()
        **pars: possible values are len, val
    Returns:
        FixedSizeField:
    """
    flds = {
        "static": StaticField,
        "fill": Filler,
        "0txt": ZeroesTextField,
        "dec2": Decimal2Field,
        "_txt": SpacesTextField,
        "txt_": TextSpacesField,
        "dmy": Date2dmyField,
        "ymd": Date2ymdField,
    }
    if fname in flds:
        return flds[fname](**pars)
    raise ValueError(f"name {fname} is not valid")


class LinePrototype:
    """This is how line is constructed"""

    def __init__(self, line_code, line_per) -> None:
        self.code = str(line_code)
        self.per = line_per
        self.fields = []
        self.names = []
        self.labels = []

    def add_field(self, name: str, field_object, label=None) -> None:
        if name in self.names:
            raise ValueError(f"name {name} already exists")
        self.names.append(name)
        self.fields.append(field_object)
        if label is None:
            self.labels.append(name)
        else:
            self.labels.append(label)

    def revert(self, textval: str) -> dict:
        assert len(textval) == self.line_size
        fdi = {"lineid": self.code}
        clean_val = textval[len(self.code) :]
        step = 0
        for i, name in enumerate(self.names):
            txval = clean_val[step : step + self.fields[i].length]
            fdi[name] = self.fields[i].revert(txval)
            step += self.fields[i].length
        return fdi

    @property
    def number_of_fields(self) -> int:
        return len(self.fields)

    @property
    def line_size(self) -> int:
        tot = len(self.code)
        for field in self.fields:
            tot += field.length
        return tot

    def __str__(self) -> str:
        return (
            f"{self.per} με κωδικό {self.code} και πεδία {self.names} "
            f"συνολικού μεγέθους {self.line_size} χαρακτήρων"
        )


class DataLine:
    def __init__(self, line_prototype, valdic=None) -> None:
        self.prototype = line_prototype
        self.values = {}
        if valdic:
            self.add_vals(valdic)

    def add_val(self, name: str, value) -> None:
        if name not in self.prototype.names:
            raise ValueError(f"Invalid name {name}")
        self.values[name] = value

    def add_vals(self, nvdic) -> None:
        for name, value in nvdic.items():
            self.add_val(name, value)

    def text(self) -> str:
        txt = self.prototype.code
        for i, name in enumerate(self.prototype.names):
            txt += self.prototype.fields[i].text(self.values.get(name, ""))
        return txt


class TextFile:
    """[summary]
    1. Create prototype lines:
       li1 = LineProrotype('1', <Description1>)
       li1.add_field(<field name>, fld(<field type>, ...))
       li1.add_field...

       li2 = LineProrotype('2', <Description2>)
       li2.add_field(<field name>, fld(<field type>, ...))
       li2.add_field ...

    2. Create a TextFile object with prototype lines:
       tf1 = TextFile({'li1': li1, 'li2': li2, ...})

    3. Now you are ready to add actual lines like:
       tf1.add_line('li1', {<field name 1>: val1, ...})
    """

    def __init__(self, protolinesdic) -> None:
        """first protoline is header, last is footer"""
        self.protolines = protolinesdic
        self.lines = []

    @property
    def line_signs(self) -> dict:
        sig = {}
        for proto in self.protolines.values():
            sig[proto.code] = proto
        return sig

    def add_line(self, protoline_key, linedic=None) -> None:
        self.lines.append(DataLine(self.protolines[protoline_key], linedic))

    def text(self) -> str:
        return "\n".join([lin.text() for lin in self.lines])

    def text2file(self, filename, encoding="WINDOWS-1253"):
        if os.path.exists(filename):
            raise FileExistsError(f"file {filename} already exists.")
        with open(filename, "w", encoding=encoding) as fil:
            fil.write(self.text())
        return True

    def revert(self, txt_lines) -> list:
        lines = txt_lines.split("\n")
        result = []
        for line in lines:
            for sign, protoline in self.line_signs.items():
                if line.startswith(sign):
                    adi = protoline.revert(line)
                    if adi:
                        result.append(adi)
        return result
