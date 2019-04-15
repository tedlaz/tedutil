from unittest import TestCase
from decimal import Decimal
from tedutil import calculator as clc
from tedutil.taxes import foros_periodoy
from tedutil.taxes import eea_periodoy
fundic = {'CALC-FOROS': foros_periodoy, 'CALC-EEA': eea_periodoy}


mis = '''
#  This is a test
?  imeromisthio meres pikatotal pikaenos
=0 BARPERIODOY  14
%4 PIKAT       pikatotal
%4 PIKAE       pikaenos
%4 PNYXTA       25
%4 PARGIA       75
%2 SYNTFOROY    22
/6 POROM        6 40
/4 ORESANAMERA  40 6
*2 OROMISTHIO   imeromisthio POROM 
*2 NYXTPROS     oresnyxta OROMISTHIO PNYXTA
*2 ARGIAPROS    meresargia imeromisthio PARGIA 
*2 NAPOD        imeromisthio meres
+2 TAPODOXES    NAPOD NYXTPROS ARGIAPROS
*2 IKATOTAL     TAPODOXES PIKAT
*2 IKAERGNO     TAPODOXES PIKAE
-2 IKAERDOTIS   IKATOTAL IKAERGNO
-2 FOROLOGITEO  TAPODOXES IKAERGNO
f  FOROSPERIODO CALC-FOROS 2019 FOROLOGITEO PAIDIA BARPERIODOY
f  EEAPERIODOY  CALC-EEA 2019 FOROLOGITEO BARPERIODOY
+2 TOTALFOROS   FOROSPERIODO EEAPERIODOY
-2 PLIROTEO     FOROLOGITEO TOTALFOROS
+2 TOTALKOSTOS  TAPODOXES IKAERDOTIS
>2 TOTAL2       PLIROTEO TOTALKOSTOS
^2 TOTAL2       10 11 1
+2 TOTAL2       PLIROTEO TOTALFOROS IKATOTAL
d2 imeromisthio
d0 meres
d0 oresnyxta
d0 meresargia
'''

exep1 = """
# To test exception1
? val1 val2
"""

exep2 = """
# to test exception 2
} SOMETHING
"""

als = """
# Δοκιμαστικός αλγόριθμος
%4 pososto-ika             45
%4 pososto-ika-ergazomenoy 15
=2 apodoxes                350
*2 ika-ergazomenoy apodoxes pososto-ika-ergazomenoy 
"""


class TestCalculator(TestCase):
    def test_calculator_good(self):
        self.assertEqual(clc.calculator(
            mis, {'imeromisthio': 60, 'meres': 25,
                  'pikatotal': 44.15, 'pikaenos': 14.98}, fundic),
        {'imeromisthio': Decimal('60.00'), 'meres': Decimal('25'),
         'pikatotal': Decimal('44.150000'), 'pikaenos': Decimal('14.980000'),
         'BARPERIODOY': Decimal('14'), 'PIKAT': Decimal('0.4415'),
         'PIKAE': Decimal('0.1498'), 'PNYXTA': Decimal('0.2500'),
         'PARGIA': Decimal('0.7500'), 'SYNTFOROY': Decimal('0.22'),
         'POROM': Decimal('0.150000'), 'ORESANAMERA': Decimal('6.6667'),
         'OROMISTHIO': Decimal('9.00'), 'oresnyxta': Decimal('0'),
         'NYXTPROS': Decimal('0.00'), 'meresargia': Decimal('0'),
         'ARGIAPROS': Decimal('0.00'), 'NAPOD': Decimal('1500.00'),
         'TAPODOXES': Decimal('1500.00'), 'IKATOTAL': Decimal('662.25'),
         'IKAERGNO': Decimal('224.70'), 'IKAERDOTIS': Decimal('437.55'),
         'FOROLOGITEO': Decimal('1275.30'), 'PAIDIA': Decimal('0'),
         'FOROSPERIODO': Decimal('144.85'), 'EEAPERIODOY': Decimal('9.20'),
         'TOTALFOROS': Decimal('154.05'), 'PLIROTEO': Decimal('1121.25'),
         'TOTALKOSTOS': Decimal('1937.55'), 'TOTAL2': Decimal('1937.55')})

    def test_calculator_exception1(self):
        self.assertRaises(ValueError, clc.calculator, exep1, {'val1': 15})

    def test_calculator_exception2(self):
        self.assertRaises(ValueError, clc.calculator, exep2, {'val1': 15})

    def test_load_algorithm(self):
        dat = {'IMEROMISTHIO': 60,
               'meres': 25,
               'POSOSTO-IKA': 44.15,
               'POSOSTO-IKA-ERGAZOMENOY': 14.98,
               'paidia': 3}
        # alg = clc.load_algorithm()
        print(clc.calc2('/home/ted/alg1.txt', dat, fundic))
        # print(clc.calc2('/home/ted/alg1.txt', dat, fundic))
        # print(clc.calc2('/home/ted/alg1.txt', dat, fundic))
