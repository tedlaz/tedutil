from unittest import TestCase
from tedutil import grdate


class TestIso2gr(TestCase):
    def test_iso2gr_good(self):
        self.assertEqual('01/03/2017', grdate.iso2gr('2017-03-01'))

    def test_iso2gr_bad(self):
        self.assertEqual('01/01/1000', grdate.iso2gr('2017-0301'))

    def test_gr2iso_good(self):
        self.assertEqual('2017-12-28', grdate.gr2iso('28/12/2017'))

    def test_gr2iso_bad(self):
        self.assertEqual('1000-01-01', grdate.gr2iso('28/022017'))

    def test_gr2iso_bad2(self):
        self.assertEqual('1000-01-01', grdate.gr2iso('28/02/12017'))
        self.assertEqual('1000-01-01', grdate.gr2iso('281/02/2017'))
        self.assertEqual('1000-01-01', grdate.gr2iso('28/021/2017'))

    def test_date2period_end1(self):
        self.assertEqual('2018-03-31', grdate.date2period_end('2018-01-01'))
        self.assertEqual('2018-06-30', grdate.date2period_end('2018-04-01'))
        self.assertEqual('2018-09-30', grdate.date2period_end('2018-07-01'))
        self.assertEqual('2018-12-31', grdate.date2period_end('2018-10-01'))

    def test_date2per1(self):
        self.assertEqual('201711', grdate.date2per('2017-01-15', 1))  # Μήνας
        self.assertEqual('201721', grdate.date2per('2017-01-15', 2))  # Δίμηνο
        self.assertEqual('201731', grdate.date2per('2017-01-15', 3))  # Τρίμηνο
        self.assertEqual('201741', grdate.date2per('2017-01-15', 4))  # Τετράμ
        self.assertEqual('201761', grdate.date2per('2017-01-15', 6))  # Εξάμηνο
        self.assertEqual('201711', grdate.date2per('2017-01-15', 8))  # Εκτός

    def test_season1(self):
        self.assertEqual('2017-2018', grdate.season('2017-10-01'))
        self.assertEqual('2016-2017', grdate.season('2017-09-30'))
        self.assertEqual('2016-2017', grdate.season('2017-10-01', 11))
        self.assertEqual('2017-2018', grdate.season('2017-02-01', 2))
        self.assertEqual('2016-2017', grdate.season('2017-01-30', 2))
