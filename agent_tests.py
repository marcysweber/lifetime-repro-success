import unittest

import agent
import lifetables
from completesimulation import SavannahSim, Population
from group import SavannahGroup
from paternity import SavannahPaternity
from seedgroups import SavannahSeed


class AgentTests(unittest.TestCase):
    def test_defaults_are_correct(self):
        generic_agent = agent.AgentClass("m", 0, None)
        self.assertEqual(generic_agent.index, 0, "index is zero")
        self.assertEqual(generic_agent.age, 0.0, "age is zero")
        self.assertEqual(generic_agent.sex, "", "sex is undefined")

    def test_rhp_dom_calc(self):
        agentone = agent.SavannahAgent('m', None, None, troopID=0)
        agentone.rhp = 10
        agenttwo = agent.SavannahAgent('m', None, None, troopID=0)
        agenttwo.rhp = 30
        agenttwo.alpha_tenure = 0.5
        agentthree = agent.SavannahAgent('m', None, None, troopID=0)
        agentthree.rhp = 20

        agentone.index = 1
        agenttwo.index = 2
        agentthree.index = 3

        agentone.sex = "m"
        agenttwo.sex = "m"
        agentthree.sex = "m"

        agentone.dispersed = True
        agenttwo.dispersed = True
        agentthree.dispersed = True

        fakesim = SavannahSim()
        fakepopulation = Population()
        fakepopulation.dict = {new_agent.index: new_agent for new_agent in [agentone,
                                                                            agenttwo,
                                                                            agentthree]}

        fakepopulation.groupsdict = {1: [1, 2, 3]}

        self.assertEquals(fakesim.dominance_calc(fakepopulation),
                          [2, 3, 1])


class PaternityTests(unittest.TestCase):
    def test_sav_paternity(self):
        agentone = agent.SavannahAgent('m', None, None, troopID=0)
        agentone.rhp = 10
        agenttwo = agent.SavannahAgent('m', None, None, troopID=0)
        agenttwo.rhp = 30
        agenttwo.alpha_tenure = 0.5
        agentthree = agent.SavannahAgent('m', None, None, troopID=0)
        agentthree.rhp = 20

        agentone.index = 1
        agenttwo.index = 2
        agentthree.index = 3

        agentone.sex = "m"
        agenttwo.sex = "m"
        agentthree.sex = "m"

        agentone.dispersed = True
        agenttwo.dispersed = True
        agentthree.dispersed = True

        fakesim = SavannahSim()
        fakepopulation = Population()
        fakepopulation.dict = {new_agent.index: new_agent for new_agent in [agentone,
                                                                            agenttwo,
                                                                            agentthree]}

        fakepopulation.groupsdict = {1: [1, 2, 3]}

        whosthedaddy = []
        for i in range(1000):
            whosthedaddy.append(SavannahPaternity.savannahsire(None,
                                                               fakesim.dominance_calc(fakepopulation),
                                                               fakepopulation))

            #  self.assertIs(Counter(whosthedaddy), 0)


class LifeTableTests(unittest.TestCase):
    def test_getting_deathchance(self):
        agentbone = agent.SavannahAgent('f', None, None, troopID=0)
        agentbone.age = 22.0
        agentbone.taxon = "savannah"

        self.assertEqual(0.2552875, lifetables.getdeathchance(agentbone))

    def test_death_proportion(self):
        fakesim = SavannahSim()
        fakepop = Population()
        group = SavannahGroup(0)

        for i in range(0, 1000):
            SavannahSeed.addagenttoseed(0, group, fakepop, 'f', None, None, 22.0)
        fakepop.groupsdict[0] = group

        for agent in fakepop.all:
            fakepop.dict[agent].taxon = "savannah"

        deathcounter = fakesim.mortality_check(fakepop)

        print "death count: " + str(deathcounter)

        #  self.assertAlmostEqual(deathcounter, 250)
        self.assertAlmostEqual(len(fakepop.all), 750, delta=75)
