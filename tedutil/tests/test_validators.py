from unittest import TestCase
from tedutil import validators as val


class TestAfm(TestCase):
    def test_afm_invalid1(self):
        self.assertEqual(False, val.is_afm(1))

    def test_afm_invalid2(self):
        self.assertEqual(False, val.is_afm(int('012312312')))

    def test_afm_invalid_0(self):
        self.assertEqual(False, val.is_afm('012312310'))

    def test_afm_invalid_1(self):
        self.assertEqual(False, val.is_afm('012312311'))

    def test_afm_invalid_3(self):
        self.assertEqual(False, val.is_afm('012312313'))

    def test_afm_invalid_4(self):
        self.assertEqual(False, val.is_afm('012312314'))

    def test_afm_invalid_5(self):
        self.assertEqual(False, val.is_afm('0123123145'))

    def test_afm_invalid_6(self):
        self.assertEqual(False, val.is_afm('012312316'))

    def test_afm_invalid_7(self):
        self.assertEqual(False, val.is_afm('012312317'))

    def test_afm_invalid_8(self):
        self.assertEqual(False, val.is_afm('012312318'))

    def test_afm_invalid_9(self):
        self.assertEqual(False, val.is_afm('012312319'))

    def test_afm_valid1(self):
        self.assertEqual(True, val.is_afm('012312312'))


class TestAmka(TestCase):
    def test_amka_true_2(self):
        self.assertEqual(True, val.is_amka('13080002382'))

    def test_amka_false_0(self):
        self.assertEqual(False, val.is_amka('13080002380'))

    def test_amka_false_1(self):
        self.assertEqual(False, val.is_amka('13080002381'))

    def test_amka_false_3(self):
        self.assertEqual(False, val.is_amka('13080002383'))

    def test_amka_false_4(self):
        self.assertEqual(False, val.is_amka('13080002384'))

    def test_amka_false_5(self):
        self.assertEqual(False, val.is_amka('13080002385'))

    def test_amka_false_6(self):
        self.assertEqual(False, val.is_amka('13080002386'))

    def test_amka_false_7(self):
        self.assertEqual(False, val.is_amka('13080002387'))

    def test_amka_false_8(self):
        self.assertEqual(False, val.is_amka('13080002388'))

    def test_amka_false_9(self):
        self.assertEqual(False, val.is_amka('13080002389'))

    def test_amka_false_digits_less_than_11(self):
        self.assertEqual(False, val.is_amka('1308000238'))
