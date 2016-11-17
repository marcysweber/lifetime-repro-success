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
        agentone.rhp = "5"
        agenttwo = agent.SavannahAgent('m', None, None, troopID=0)
        agenttwo.rhp = "1"
        agenttwo.alpha_tenure = 0.5
        agentthree = agent.SavannahAgent('m', None, None, troopID=0)
        agentthree.rhp = "3"

        agentone.index = 1
        agenttwo.index = 2
        agentthree.index = 3

        agentone.sex = "m"
        agenttwo.sex = "m"
        agentthree.sex = "m"

        agentone.dispersed = True
        agenttwo.dispersed = True
        agentthree.dispersed = True

        agentone.age = 8
        agenttwo.age = 8
        agentthree.age = 8

        fakesim = SavannahSim()
        fakepopulation = Population()
        fakepopulation.dict = {new_agent.index: new_agent for new_agent in [agentone,
                                                                            agenttwo,
                                                                            agentthree]}

        group = SavannahGroup(1)
        group.agents = [1, 2, 3]
        fakepopulation.groupsdict[1] = group
        fakesim.dominance_calc(fakepopulation, group)

        self.assertEquals(group.dominance_hierarchy,
                          [2, 3, 1])


class PaternityTests(unittest.TestCase):
    def test_sav_paternity(self):
        agentone = agent.SavannahAgent('m', None, None, troopID=0)
        agentone.rhp = "5"
        agenttwo = agent.SavannahAgent('m', None, None, troopID=0)
        agenttwo.rhp = "1"
        agenttwo.alpha_tenure = 0.5
        agentthree = agent.SavannahAgent('m', None, None, troopID=0)
        agentthree.rhp = "3"

        agentone.index = 1
        agenttwo.index = 2
        agentthree.index = 3

        agentone.sex = "m"
        agenttwo.sex = "m"
        agentthree.sex = "m"

        agentone.dispersed = True
        agenttwo.dispersed = True
        agentthree.dispersed = True

        agentone.age = 8
        agenttwo.age = 8
        agentthree.age = 8

        fakesim = SavannahSim()
        fakepopulation = Population()
        fakepopulation.dict = {new_agent.index: new_agent for new_agent in [agentone,
                                                                            agenttwo,
                                                                            agentthree]}
        group = SavannahGroup(1)
        group.agents = [1, 2, 3]
        fakepopulation.groupsdict[1] = group

        whosthedaddy = []
        # for i in range(1000):
        #     whosthedaddy.append(SavannahPaternity.savannahsire(None,
        #                                                        fakesim.dominance_calc(fakepopulation, group),
        #                                                        fakepopulation))

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

    def test_birth_stuff(self):
        fakesim = SavannahSim()
        fakepop = Population()
        group = SavannahGroup(0)

        for i in range(0, 1200):
            SavannahSeed.addagenttoseed(0, group, fakepop, 'f', None, None, 5.0)

        SavannahSeed.addagenttoseed(0, group, fakepop, 'm', None, None, 9)
        SavannahSeed.addagenttoseed(0, group, fakepop, 'm', None, None, 18)
        fakepop.groupsdict[0] = group

        fakepop.dict[1201].rhp = "1"
        fakepop.dict[1202].rhp = "5"

        fakesim.dominance_calc(fakepop, group)

        fakesim.birth_check(fakepop, 50)

        self.assertAlmostEqual(fakepop.all, 2200, delta=100)

        sired1201 = 0
        females = 0

        for agentindex in fakepop.all:
            agent = fakepop.dict[agentindex]

            if agent.parents:
                if agent.parents[1] == 1201:
                    sired1201 += 1
            if agent.sex == 'f':
                females += 1

        self.assertAlmostEqual(sired1201, 625, delta=50)
        self.assertAlmostEqual(females, 1700, delta=100)


class RhpTests(unittest.TestCase):
    def checkrhpvalues(self):
        tagent1 = agent.SavannahAgent('m', None, None, None)
        tagent1.age = 20
        tagent1.rhp = "1"
        self.assertEqual(16, tagent1.get_rhp())

        tagent2 = agent.SavannahAgent('m', None, None, None)
        tagent2.age = 11.5
        tagent2.rhp = "5"
        self.assertEqual(23.9, tagent2.get_rhp())

        tagent3 = agent.HamadryasAgent('m', None, None, None)
        tagent3.age = 13
        tagent3.rhp = "2"
        self.assertEqual(40, tagent3.get_rhp())
