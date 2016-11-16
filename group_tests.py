import unittest

from completesimulation import SavannahSim, Population, HamadryasSim
from seedgroups import SavannahSeed, HamadryasSeed


class SeedTests(unittest.TestCase):
    def test_that_seed_makes_pop(self):
        fakesim = SavannahSim()
        fakepopulation = Population()
        fakepopulation = SavannahSeed.makeseed(1, fakepopulation)
        self.assertEqual(len(fakepopulation.all), len(fakepopulation.groupsdict[1].agents))
        self.assertEqual(len(fakepopulation.groupsdict), 1)

        self.assertEquals(len(fakepopulation.all), 54)
        self.assertEqual(fakepopulation.dict[10].sex, 'f')
        self.assertEqual(fakepopulation.dict[54].sex, 'm')
        self.assertGreater(fakepopulation.dict[16].age, 5.0)
        self.assertGreater(5.0, fakepopulation.dict[17].age)

    def test_hama_seed(self):
        fakesim = HamadryasSim()
        fakepopulation2 = Population()
        fakepopulation2 = HamadryasSeed.makeseed(1, fakepopulation2)

        self.assertEqual(len(fakepopulation2.groupsdict[1].leadermales), 8)
        self.assertEqual(len(fakepopulation2.all), 65)
