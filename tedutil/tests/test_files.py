from unittest import TestCase
import os
from tedutil import files as fls


class TestDownload_file(TestCase):

    def test_zipfile_data(self):
        URLF = "http://www.ika.gr/gr/infopages/downloads/osyk.zip"
        dirc = os.path.dirname(__file__)
        fls.download_file(URLF, dirc)
        zfile = os.path.join(dirc, 'osyk.zip')
        fdata = fls.zipfile_data(zfile, 'dn_kad.txt')
        # print(fdata)
        os.remove(zfile)
