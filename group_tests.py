import unittest

from agent import FemaleState
from completesimulation import SavannahSim, Population, HamadryasSim
from dispersal import SavannahDispersal
from group import SavannahGroup
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


class DominanceTests(unittest.TestCase):
    def test_savannah_hier(self):
        fakesim = SavannahSim()
        dompop = Population()
        fakegroup = SavannahGroup(1)

        SavannahSeed.addagenttoseed(1, fakegroup, dompop, "m", None, None, 7)
        SavannahSeed.addagenttoseed(1, fakegroup, dompop, "m", None, None, 7)
        SavannahSeed.addagenttoseed(1, fakegroup, dompop, "m", None, None, 7)
        SavannahSeed.addagenttoseed(1, fakegroup, dompop, "m", None, None, 7)
        SavannahSeed.addagenttoseed(1, fakegroup, dompop, "m", None, None, 7)

        for male in [agent for agent in dompop.dict.values() if agent.sex == "m"]:
            male.dispersed = True

        dompop.dict[1].rhp = "5"
        dompop.dict[2].rhp = "1"
        dompop.dict[3].rhp = "2"
        dompop.dict[4].rhp = "4"
        dompop.dict[5].rhp = "3"

        fakesim.dominance_calc(dompop, fakegroup)

        self.assertEqual(fakegroup.dominance_hierarchy, [2, 3, 5, 4, 1])


class DispersalTests(unittest.TestCase):
    def test_move_one_agent(self):
        disp_sim = SavannahSim()
        disp_pop = Population()
        disp_group_1 = SavannahGroup(1)
        disp_group_2 = SavannahGroup(2)

        for i in range(0, 10):
            SavannahSeed.addagenttoseed(1, disp_group_1, disp_pop, 'f', None, None, 10)
        for fem in disp_group_1.agents:
            fem = disp_pop.dict[fem]
            fem.femaleState = FemaleState.cycling

        for i in range(0, 10):
            SavannahSeed.addagenttoseed(2, disp_group_2, disp_pop, 'f', None, None, 10)
        for fem in disp_group_2.agents:
            fem = disp_pop.dict[fem]
            fem.femaleState = FemaleState.cycling

        SavannahSeed.addagenttoseed(1, disp_group_1, disp_pop, 'm', None, None, 10)

        disp_pop.groupsdict = {1: disp_group_1, 2: disp_group_2}

        SavannahDispersal.disperse(disp_pop.dict[21], disp_pop)

        self.assertNotIn(21, disp_group_1.agents)

    def test_dispersal_dest_proportion(self):

        total_dispersals_to_1 = 0

        for i in range(0, 1000):
            disp_sim = SavannahSim()
            disp_pop = Population()
            disp_group_1 = SavannahGroup(1)
            disp_group_2 = SavannahGroup(2)
            disp_group_3 = SavannahGroup(3)

            disp_pop.groupsdict = {1: disp_group_1, 2: disp_group_2, 3: disp_group_3}

            for group in disp_pop.groupsdict.keys():
                for i in range(0, 10):
                    SavannahSeed.addagenttoseed(group,
                                                disp_pop.groupsdict[group],
                                                disp_pop, 'f', None, None, 10)
                for i in range(0, 5):
                    SavannahSeed.addagenttoseed(group,
                                                disp_pop.groupsdict[group],
                                                disp_pop, 'm', None, None, 10)
                if group == 1:
                    for i in range(0, 10):
                        agentindex = disp_pop.groupsdict[1].agents[i]
                        agent = disp_pop.dict[agentindex]
                        agent.femaleState = FemaleState.cycling
                if group == 2:
                    for i in range(0, 5):
                        agentindex = disp_pop.groupsdict[1].agents[i]
                        agent = disp_pop.dict[agentindex]
                        agent.femaleState = FemaleState.cycling

            SavannahDispersal.disperse(disp_pop.dict[27], disp_pop)

            total_dispersals_to_1 += len(disp_group_1.agents) - 15

        self.assertAlmostEqual(total_dispersals_to_1, 666, delta=60)
