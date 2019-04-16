from unittest import TestCase
from tedutil import osyk as osk
from tedutil.logger import logger
import os


class TestOsyk(TestCase):
    def test_kadeidkpk_find(self):
        per = 201602
        # print(eid_kad_string(5540, PER))
        dirc = os.path.dirname(__file__)
        osyk = os.path.join(dirc, 'osyk.zio')
        logger.info(osk.eid_find(311400, osyk=osyk))
        logger.info(osk.kadeidkpk_find(5540, 311400, per, osyk=osyk))
        logger.info(osk.kpk_find(101, 201901, osyk=osyk))
        vls = '\n'.join(['%s' % i for i in osk.eid_kad_list(5540,
                                                            '201903',
                                                            osyk=osyk)])
        logger.info('List:\n%s\n' % vls)
        # print(kad_list())
        # osyk = Osyk()
        # print(osk.find_kad('Ξενοδοχεία')) # returns list of kads
        # osyk.find_eid('Μάγειρας') returns list of eids
