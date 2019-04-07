from unittest import TestCase
import os
from tedutil import files as fls
from tedutil.logger import logger


class TestDownload_file(TestCase):

    def test_zipfile_data(self):
        URLF = "http://www.ika.gr/gr/infopages/downloads/osyk.zip"
        dirc = os.path.dirname(__file__)
        fls.download_file(URLF, dirc)
        zfile = os.path.join(dirc, 'osyk.zip')
        fdata = fls.zipfile_data(zfile, 'dn_kad.txt')
        # print(fdata)
        os.remove(zfile)
        logger.info("File %s deleted" % zfile)
