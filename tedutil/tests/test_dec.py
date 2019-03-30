from unittest import TestCase
from tedutil import dec


class TestDec(TestCase):

    def test_is_num_string(self):
        self.assertEqual(False, dec.is_number('123f'))

    def test_is_num_float(self):
        self.assertEqual(True, dec.is_number('13.24'))

    def test_is_num_float2(self):
        self.assertEqual(False, dec.is_number('13.243.2'))


    def test_zero_string_equals_zero(self):
        self.assertEqual(0, dec.dec(''))

    def test_None_equals_zero(self):
        self.assertEqual(0, dec.dec(None))

    def test_rounding(self):
        self.assertEqual(10.35, float(dec.dec(10.345)))

    def test_rounding2(self):
        self.assertEqual(10.35, float(dec.dec('10.345')))

    def test_dec2gr1(self):
        self.assertEqual('123.456,78', dec.dec2gr(123456.78))

    def test_dec2gr2(self):
        self.assertEqual('-123.456,78', dec.dec2gr(-123456.78))

    def test_dec2gr3(self):
        self.assertEqual('123.456,78', dec.dec2gr('123456.78'))

    def test_dec2gr_empty_string(self):
        self.assertEqual('', dec.dec2gr(0))

    def test_gr2dec(self):
        self.assertEqual(dec.dec('123456.78'), dec.gr2dec('123.456,78'))
