from unittest import TestCase
from tedutil import validators as val


class TestVarius(TestCase):
    def test_afm_invalid1(self):
        self.assertFalse(val.is_afm(1))

    def test_afm_invalid2(self):
        self.assertFalse(val.is_afm(int('012312312')))

    def test_afm_invalid_0(self):
        self.assertFalse(val.is_afm('012312310'))

    def test_afm_invalid_1(self):
        self.assertFalse(val.is_afm('012312311'))

    def test_afm_invalid_3(self):
        self.assertFalse(val.is_afm('012312313'))

    def test_afm_invalid_4(self):
        self.assertFalse(val.is_afm('012312314'))

    def test_afm_invalid_5(self):
        self.assertFalse(val.is_afm('0123123145'))

    def test_afm_invalid_6(self):
        self.assertFalse(val.is_afm('012312316'))

    def test_afm_invalid_7(self):
        self.assertFalse(val.is_afm('012312317'))

    def test_afm_invalid_8(self):
        self.assertFalse(val.is_afm('012312318'))

    def test_afm_invalid_9(self):
        self.assertFalse(val.is_afm('012312319'))

    def test_afm_valid1(self):
        self.assertTrue(val.is_afm('012312312'))

    def test_amka_true_2(self):
        self.assertTrue(val.is_amka('13080002382'))

    def test_amka_false_0(self):
        self.assertFalse(val.is_amka('13080002380'))

    def test_amka_false_1(self):
        self.assertFalse(val.is_amka('13080002381'))

    def test_amka_false_3(self):
        self.assertFalse(val.is_amka('13080002383'))

    def test_amka_false_4(self):
        self.assertFalse(val.is_amka('13080002384'))

    def test_amka_false_5(self):
        self.assertFalse(val.is_amka('13080002385'))

    def test_amka_false_6(self):
        self.assertFalse(val.is_amka('13080002386'))

    def test_amka_false_7(self):
        self.assertFalse(val.is_amka('13080002387'))

    def test_amka_false_8(self):
        self.assertFalse(val.is_amka('13080002388'))

    def test_amka_false_9(self):
        self.assertFalse(val.is_amka('13080002389'))

    def test_amka_false_digits_less_than_11(self):
        self.assertFalse(val.is_amka('1308000238'))

    def test_is_greek_date(self):
        self.assertTrue(val.is_greek_date('15/2/1963'))
        self.assertFalse(val.is_greek_date('15.2.1963'))
        self.assertFalse(val.is_greek_date('15/2.1963'))
        self.assertFalse(val.is_greek_date('15/2a/1963'))
        self.assertFalse(val.is_greek_date('-15/2/1963'))
        self.assertFalse(val.is_greek_date('0/2/1963'))
        self.assertTrue(val.is_greek_date('31/3/1963'))
        self.assertFalse(val.is_greek_date('30/2/1963'))
        self.assertFalse(val.is_greek_date('01/13/1963'))
        self.assertFalse(val.is_greek_date(3))


    def test_is_iso_date(self):
        self.assertTrue(val.is_iso_date('2020-01-01'))
        self.assertTrue(val.is_iso_date('2020-02-28'))
        self.assertFalse(val.is_iso_date('2020-13-01'))
        self.assertFalse(val.is_iso_date('2021-02-29'))
        self.assertFalse(val.is_iso_date('202c-02-01'))
        self.assertFalse(val.is_iso_date('2020-02-1'))
        self.assertFalse(val.is_iso_date(14))

    def test_is_number(self):
        self.assertFalse(val.is_number('123f'))
        self.assertTrue(val.is_number('13.24'))
        self.assertFalse(val.is_number('13.243.2'))
