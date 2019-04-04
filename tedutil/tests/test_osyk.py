from unittest import TestCase
from tedutil import osyk as osk

class TestOsyk(TestCase):
    def test_kadeidkpk_find(self):
        PER = 201602
        # print(eid_kad_string(5540, PER))
        print(osk.eid_find(311400))
        print(osk.kadeidkpk_find(5540, 311400, PER))
        print(osk.eid_kad_list(5540, '201903'))
        # print(kad_list())
        # osyk = Osyk()
        # osyk.find_kad('Ξενοδοχεία') returns list of kads
        # osyk.find_eid('Μάγειρας') returns list of eids
