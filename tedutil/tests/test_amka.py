from unittest import TestCase
from tedutil import validators as amka


class TestAmka(TestCase):
    def test_amka_true_2(self):
        self.assertEqual(True, amka.is_amka('13080002382'))

    def test_amka_false_0(self):
        self.assertEqual(False, amka.is_amka('13080002380'))

    def test_amka_false_1(self):
        self.assertEqual(False, amka.is_amka('13080002381'))

    def test_amka_false_3(self):
        self.assertEqual(False, amka.is_amka('13080002383'))

    def test_amka_false_4(self):
        self.assertEqual(False, amka.is_amka('13080002384'))

    def test_amka_false_5(self):
        self.assertEqual(False, amka.is_amka('13080002385'))

    def test_amka_false_6(self):
        self.assertEqual(False, amka.is_amka('13080002386'))

    def test_amka_false_7(self):
        self.assertEqual(False, amka.is_amka('13080002387'))

    def test_amka_false_8(self):
        self.assertEqual(False, amka.is_amka('13080002388'))

    def test_amka_false_9(self):
        self.assertEqual(False, amka.is_amka('13080002389'))

    def test_amka_false_digits_less_than_11(self):
        self.assertEqual(False, amka.is_amka('1308000238'))
