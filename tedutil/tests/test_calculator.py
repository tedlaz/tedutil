from unittest import TestCase
from decimal import Decimal
from tedutil import calculator as clc


mis = '''
?  imeromisthio meres pikat pikae
=0 BARPERIODOY  14
%4 PIKAT        pikat
%4 PIKAE        pikae
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
*2 FOROLETOYS   FOROLOGITEO BARPERIODOY
/2 EEAPERIODOY  EEAETOYS BARPERIODOY
+2 TOTALFOROS   FOROSPERIODO EEAPERIODOY
-2 PLIROTEO     FOROLOGITEO TOTALFOROS
+2 TOTALKOSTOS  TAPODOXES IKAERDOTIS
+2 TOTAL2       PLIROTEO TOTALFOROS IKATOTAL
d2 imeromisthio
d0 meres
d0 oresnyxta
d0 meresargia
'''


class TestCalculator(TestCase):
    def test_calculator(self):
        self.assertEqual(clc.calculator(
            mis, {'imeromisthio': 40, 'meres': 10,
                  'pikat': 44.15, 'pikae': 14.98}),
            {'imeromisthio': Decimal('40.00'), 'meres': Decimal('10'),
             'pikat': Decimal('44.150000'), 'pikae': Decimal('14.980000'),
             'BARPERIODOY': Decimal('14'), 'PIKAT': Decimal('0.4415'),
             'PIKAE': Decimal('0.1498'), 'PNYXTA': Decimal('0.2500'),
             'PARGIA': Decimal('0.7500'), 'SYNTFOROY': Decimal('0.22'),
             'POROM': Decimal('0.150000'), 'ORESANAMERA': Decimal('6.6667'),
             'OROMISTHIO': Decimal('6.00'), 'oresnyxta': Decimal('0'),
             'NYXTPROS': Decimal('0.00'), 'meresargia': Decimal('0'),
             'ARGIAPROS': Decimal('0.00'), 'NAPOD': Decimal('400.00'),
             'TAPODOXES': Decimal('400.00'), 'IKATOTAL': Decimal('176.60'),
             'IKAERGNO': Decimal('59.92'), 'IKAERDOTIS': Decimal('116.68'),
             'FOROLOGITEO': Decimal('340.08'), 'FOROLETOYS': Decimal('4761.12'),
             'EEAETOYS': Decimal('0'), 'EEAPERIODOY': Decimal('0.00'),
             'FOROSPERIODO': Decimal('0'), 'TOTALFOROS': Decimal('0.00'),
             'PLIROTEO': Decimal('340.08'), 'TOTALKOSTOS': Decimal('516.68'),
             'TOTAL2': Decimal('516.68')}
        )
