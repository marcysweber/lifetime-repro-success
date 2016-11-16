import unittest

import agent
from completesimulation import SavannahSim, Population
from paternity import SavannahPaternity


class AgentTests(unittest.TestCase):
    def test_defaults_are_correct(self):
        generic_agent = agent.AgentClass("m", 0)
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
