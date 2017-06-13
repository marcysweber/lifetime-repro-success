import unittest

from agent import *
from completesimulation import HamadryasSim, HamaPopulation, GeladaSim, GelPopulation
from dispersal import HamadryasDispersal, GeladaDispersal
from group import HamadryasGroup, GeladaGroup
from seedgroups import HamadryasSeed, GeladaSeed


class DispersalTests(unittest.TestCase):
    def setup_gelada(self):
        sim = GeladaSim()
        pop = GelPopulation()
        band1 = GeladaGroup(1)
        band2 = GeladaGroup(2)

        pop.groupsdict[1] = band1
        pop.groupsdict[2] = band2

        GeladaSeed.addagenttoseed(1, band1, pop, 'm', None, None, 10, sim)

        pass

    def test_attractiveness_ranking(self):
        pass

    def test_become_bachelor(self):
        pass

    def test_inherit(self):
        pass

    def test_challenge(self):
        pass

    def test_fol_switch_OMU(self):
        pass

    def test_disperse_bands(self):
        pass

    def test_follow(self):
        pass

    def test_solitary(self):
        pass

    def test_follower(self):
        pass
