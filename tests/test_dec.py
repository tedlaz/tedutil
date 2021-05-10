from unittest import TestCase
from tedutil import dec


class TestDec(TestCase):
    def test_zero_string_equals_zero(self):
        self.assertEqual(0, dec.dec(""))

    def test_None_equals_zero(self):
        self.assertEqual(0, dec.dec(None))

    def test_rounding(self):
        self.assertEqual(10.35, float(dec.dec(10.345)))

    def test_rounding2(self):
        self.assertEqual(10.35, float(dec.dec("10.345")))

    def test_dec2gr1(self):
        self.assertEqual("123.456,78", dec.dec2gr(123456.78))

    def test_dec2gr2(self):
        self.assertEqual("-123.456,78", dec.dec2gr(-123456.78))

    def test_dec2gr3(self):
        self.assertEqual("123.456,78", dec.dec2gr("123456.78"))

    def test_dec2gr_empty_string(self):
        self.assertEqual("", dec.dec2gr(0))

    def test_gr2dec(self):
        self.assertEqual(dec.dec("123456.78"), dec.gr2dec("123.456,78"))

    def test_klimaka_normal(self):
        self.assertEqual(dec.klimaka(900, [50, 50], [0, 10, 20]), dec.dec(165))
        self.assertEqual(dec.klimaka(10, [50, 50], [0, 10, 20]), dec.dec(0))

    def test_klimaka_exception(self):
        self.assertRaises(ValueError, dec.klimaka, 10, [10, 20], [10, 20])

    def test_split_val_to_list1(self):
        self.assertEqual(
            dec.split_val_to_list(100, [10, 20]),
            [dec.dec(10), dec.dec(20), dec.dec(70)],
        )

    def test_distribute1(self):
        self.assertEqual(
            dec.distribute(100.37, [10.22, 20.31, 30.44, 41, 28]),
            [
                dec.dec("7.89"),
                dec.dec("15.68"),
                dec.dec("23.51"),
                dec.dec("31.67"),
                dec.dec("21.62"),
            ],
        )

    def test_int_always(self):
        self.assertEqual(dec.int_always(100.3), 100)
        self.assertEqual(dec.int_always("35a"), 0)
        self.assertEqual(dec.int_always(None), 0)

    def test_dec_with_given_digits(self):
        self.assertEqual(dec.dec_with_given_digits("100.236"), dec.dec(100.236, 3))
        self.assertEqual(dec.dec_with_given_digits("100"), dec.dec(100, 0))

    def test_dic2gr(self):
        self.assertEqual(
            dec.dic2gr({"a": 100.23, "b": "100.23"}), {"a": "100,23", "b": "100,23"}
        )

    def test_dic_print(self):
        va1 = "αγορές                        :        10.25"
        self.assertEqual(dec.dic_print({"αγορές": 10.25}), va1)

    def test_eisfores(self):
        cost = dec.eisfores(845, 14.12, 36.66)["cost"]
        self.assertEqual(cost, dec.dec(1035.47))
        cost = dec.eisfores(845, 0.1412, 0.3666)["cost"]
        self.assertEqual(cost, dec.dec(1035.47))
        total = dec.eisfores(845, 14.12, 40, 500)["total"]
        self.assertEqual(total, dec.dec(200))
