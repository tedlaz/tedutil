from unittest import TestCase
import os
from tedutil import acc_parse as acp


dir_path = os.path.dirname(os.path.realpath(__file__))

class TestAccountParse(TestCase):
    def test_parse(self):
        fil = os.path.join(dir_path, 'acc.txt')
        chart, chart0, ee_lines = acp.acc_parse(fil)
        print(acp.match_account('24.02.00.000', chart))
