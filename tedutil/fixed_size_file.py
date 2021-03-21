from decimal import Decimal as dec
import os
from tedutil.grtext import grup


class FixedSizeField:
    """""Abstract class"""""

    def __init__(self, siz):
        self.length = siz

    def text(self, val):
        raise NotImplemented

    def revert(self, textVal):
        raise NotImplemented


class StaticField(FixedSizeField):
    """Just a fixed value ABCD -> ABCD """

    def __init__(self, val):
        self.val = grup(val)
        super().__init__(len(self.val))

    def text(self, _):
        return self.val

    def revert(self, txtval):
        assert txtval == self.val
        return txtval


class Filler(FixedSizeField):
    """Fill with a specific char"""

    def __init__(self, siz, val):
        super().__init__(siz)
        self.val = str(val)

    def text(self, _):
        return self.val * self.length

    def revert(self, txtval):
        return txtval[0]


class ZeroesTextField(FixedSizeField):
    """ 123 -> '0000123' """

    def text(self, val):
        txt = str(val)
        txt_len = len(txt)
        if txt_len > self.length:
            raise ValueError('text length is bigger than allowed')
        zeroes = '0' * (self.length - txt_len)
        return zeroes + txt

    def revert(self, txtval):
        return txtval.strip().lstrip('0')


class Decimal2Field(FixedSizeField):
    """Decimal with 2 decimal digits 123.45 -> '0000012345' """

    def text(self, val):
        txt = str(round(dec(val), 2)).replace('.', '')
        txt_len = len(txt)
        if txt_len > self.length:
            raise ValueError('text length is bigger than allowed')
        zeroes = '0' * (self.length - txt_len)
        return zeroes + txt

    def revert(self, txtval):
        return round(dec(txtval.strip().lstrip('0')) / dec(100), 2)


class TextSpacesField(FixedSizeField):
    """ 'abc' -> 'abc    ' """

    def text(self, val):
        txt = grup(val)
        txt_len = len(txt)
        if txt_len > self.length:
            raise ValueError('text length is bigger than allowed')
        spaces = ' ' * (self.length - txt_len)
        return txt + spaces

    def revert(self, txtval):
        return txtval.strip()


class SpacesTextField(FixedSizeField):
    """ 'abc' -> '    abc' """

    def text(self, val):
        txt = grup(val)
        txt_len = len(txt)
        if txt_len > self.length:
            raise ValueError('text length is bigger than allowed')
        spaces = ' ' * (self.length - txt_len)
        return spaces + txt

    def revert(self, txtval):
        return txtval.strip()


class Date2dmyField(FixedSizeField):
    """Iso date to text YYYY-MM-DD -> DDMMYYYY """

    def __init__(self):
        super().__init__(8)

    def text(self, isodate):
        assert len(isodate) == 10
        year, month, day = isodate.split('-')
        return f'{day}{month}{year}'

    def revert(self, txtval):
        day = txtval[:2]
        month = txtval[2:4]
        year = txtval[4:]
        return f'{year}-{month}-{day}'


class Date2ymdField(FixedSizeField):
    """Iso date to text YYYY-MM-DD -> YYYYMMDD """

    def __init__(self):
        super().__init__(8)

    def text(self, isodate):
        assert len(isodate) == 10
        year, month, date = isodate.split('-')
        return f'{year}{month}{date}'

    def revert(self, txtval):
        year = txtval[:4]
        month = txtval[4:6]
        day = txtval[6:]
        return f'{year}-{month}-{day}'


def fld(fname, **pars):
    """Factory to create fields

    Args:
        fname (str): static(val), fill(siz, val), dec2(siz), _txt(siz), txt_(siz), dmy(), ymd()
        **pars: possible values are len, val
    Returns:
        FixedSizeField:
    """
    flds = {
        'static': StaticField,
        'fill': Filler,
        '0txt': ZeroesTextField,
        'dec2': Decimal2Field,
        '_txt': SpacesTextField,
        'txt_': TextSpacesField,
        'dmy': Date2dmyField,
        'ymd': Date2ymdField
    }
    if fname in flds:
        return flds[fname](**pars)
    raise ValueError(f'name {fname} is not valid')


class LinePrototype:
    """This is how line is constructed"""

    def __init__(self, line_code, line_per):
        self.code = str(line_code)
        self.per = line_per
        self.fields = []
        self.names = []
        self.labels = []

    def add_field(self, name, field_object, label=None):
        if name in self.names:
            raise ValueError(f'name {name} already exists')
        self.names.append(name)
        self.fields.append(field_object)
        if label is None:
            self.labels.append(name)
        else:
            self.labels.append(label)

    def revert(self, textval):
        assert len(textval) == self.line_size
        fdi = {'lineid': self.code}
        clean_val = textval[len(self.code):]
        step = 0
        for i, name in enumerate(self.names):
            txval = clean_val[step:step+self.fields[i].length]
            fdi[name] = self.fields[i].revert(txval)
            step += self.fields[i].length
        return fdi

    @property
    def number_of_fields(self):
        return len(self.fields)

    @property
    def line_size(self):
        tot = len(self.code)
        for field in self.fields:
            tot += field.length
        return tot

    def __str__(self):
        return (
            f'{self.per} με κωδικό {self.code} και πεδία {self.names} '
            f'συνολικού μεγέθους {self.line_size} χαρακτήρων'
        )


class DataLine:
    def __init__(self, line_prototype, valdic=None):
        self.prototype = line_prototype
        self.values = {}
        if valdic:
            self.add_vals(valdic)

    def add_val(self, name, value):
        if name not in self.prototype.names:
            raise ValueError(f'Invalid name {name}')
        self.values[name] = value

    def add_vals(self, nvdic):
        for name, value in nvdic.items():
            self.add_val(name, value)

    def text(self):
        txt = self.prototype.code
        for i, name in enumerate(self.prototype.names):
            txt += self.prototype.fields[i].text(self.values.get(name, ''))
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
    def __init__(self, protolinesdic):
        """first protoline is header, last is footer"""
        self.protolines = protolinesdic
        self.lines = []

    @property
    def line_signs(self):
        sig = {}
        for proto in self.protolines.values():
            sig[proto.code] = proto
        return sig

    def add_line(self, protoline_key, linedic=None):
        self.lines.append(DataLine(self.protolines[protoline_key], linedic))

    def text(self):
        return '\n'.join([l.text() for l in self.lines])

    def text2file(self, filename, encoding='WINDOWS-1253'):
        if os.path.exists(filename):
            raise FileExistsError(f'file {filename} already exists.')
        with open(filename, 'w', encoding=encoding) as fil:
            fil.write(self.text())
        return True

    def revert(self, txt_lines):
        lines = txt_lines.split('\n')
        result = []
        for line in lines:
            for sign, protoline in self.line_signs.items():
                if line.startswith(sign):
                    adi = protoline.revert(line)
                    if adi:
                        result.append(adi)
        return result
