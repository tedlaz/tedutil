from unittest import TestCase
from collections import namedtuple
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

    def test_read_named_csv_file(self):
        dirc = os.path.dirname(__file__)
        filename = os.path.join(dirc, 'named.csv')
        data = fls.read_named_csv_file(filename)
        Row = namedtuple('Row', "no date name sex age")
        vls = [Row('1', '2019-02-17', 'mark', 'male', '26'),
               Row('2', '2019-02-18', 'mary', 'female', '19'),
               Row('3', '2019-03-21', 'ted', 'male', '57')]
        self.assertEqual(data, vls)
