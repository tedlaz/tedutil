from unittest import TestCase
from decimal import Decimal
from tedutil import taxes as tx1


class TestTaxes(TestCase):
    def test_foros_etoys(self):
        self.assertEqual(tx1.foros_etoys(2012, 110000), Decimal('36920'))
        self.assertRaises(ValueError, tx1.foros_etoys, 1963, 12000)

    def test_meiosi_foroy(self):
        self.assertEqual(tx1.meiosi_foroy(2019, 200000, 0), Decimal('100'))
        self.assertEqual(tx1.meiosi_foroy(2019, 1000, 5), Decimal('2100'))
        self.assertEqual(tx1.meiosi_foroy(2019, 500000, 0), Decimal('0'))

    def test_foros_etoys_me_ekptosi(self):
        self.assertEqual(tx1.foros_etoys_me_ekptosi(2019, 14000),
                         Decimal('1180'))

    def test_eea_etoys(self):
        self.assertEqual(tx1.eea_etoys(1985, 1000), Decimal('0'))

    def test_eea_periodoy(self):
        self.assertEqual(tx1.eea_periodoy(2019, 1000, extra=100),
                         Decimal('5.34'))

    def test_foros_eea_periodoy(self):
        self.assertEqual(tx1.foros_eea_periodoy(2019, 1000, extra=100),
                         {'foros': Decimal('106.29'), 'eea': Decimal('5.34'),
                          'forolog': Decimal('1100.00'),
                          'pliroteo': Decimal('988.37')})

    def test_reverse_apodoxes(self):
        self.assertEqual(tx1.reverse_apodoxes(2019, 1250, 16, 3),
                         Decimal('1697.99'))

    def test_apodoxes(self):

        result = {
            'foros': Decimal('5.09'),
            'eea': Decimal('0.00'),
            'forolog': Decimal('640.00'),
            'pliroteo': Decimal('634.91'),
            'paidia': 0,
            'mikto': Decimal('800.00'),
            'pika': '20%',
            'ika': Decimal('160.00'),
            'krat': Decimal('165.09')
        }
        self.assertEqual(tx1.test_apodoxes(2019, 800, 20, paidia=0), result)

    def test_kostos_misthodosias(self):
        self.assertEqual(tx1.kostos_misthodosias(800, 20), 1201.8)

    def test_mikta_apo_kathara(self):
        kathara = tx1.mikta_apo_kathara(1000, 15, 0, '2019-01-01')
        self.assertEqual(kathara, Decimal('1312.16'))
        kathara = tx1.mikta_apo_kathara(1000, 15, 0)
        self.assertEqual(kathara, Decimal('1292.54'))

    def test_foros2020(self):
        pliroteo = tx1.foros(2021, 10159.66, 1)['pliroteo']
        self.assertEqual(pliroteo, Decimal('10034.53'))
        pliroteo = tx1.foros(2021, 13000, 3)['pliroteo']
        self.assertEqual(pliroteo, Decimal('12518'))
        pliroteo = tx1.foros(2021, 130000, 3)['pliroteo']
        self.assertEqual(pliroteo, Decimal('71849'))
        pliroteo = tx1.foros(2021, 3000, 0)['pliroteo']
        self.assertEqual(pliroteo, Decimal('3000'))
        self.assertRaises(ValueError, tx1.foros, 1980, 15000, 1)
