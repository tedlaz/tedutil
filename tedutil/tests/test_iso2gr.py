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
