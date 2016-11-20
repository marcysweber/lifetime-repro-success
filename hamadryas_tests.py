import unittest

from agent import *
from completesimulation import HamadryasSim, HamaPopulation
from dispersal import HamadryasDispersal
from group import HamadryasGroup
from seedgroups import HamadryasSeed


class ChallengeTests(unittest.TestCase):
    def setup_rhp(self):
        hama_rhp_pop = HamaPopulation()
        hama_rhp_group = HamadryasGroup(1)
        hama_rhp_pop.groupsdict[1] = hama_rhp_group

        HamadryasSeed.addagenttoseed(1, hama_rhp_group, hama_rhp_pop, 'm', None, None, 10)
        HamadryasSeed.addagenttoseed(1, hama_rhp_group, hama_rhp_pop, 'm', None, None, 10)
        HamadryasSeed.addagenttoseed(1, hama_rhp_group, hama_rhp_pop, 'm', None, None, 13.5)
        HamadryasSeed.addagenttoseed(1, hama_rhp_group, hama_rhp_pop, 'm', None, None, 13.5)

        hama_rhp_pop.dict[1].rhp = '1'
        hama_rhp_pop.dict[2].rhp = '2'
        hama_rhp_pop.dict[3].rhp = '3'
        hama_rhp_pop.dict[4].rhp = '4'

        return hama_rhp_pop

    def test_rhp(self):
        hama_rhp_pop = self.setup_rhp()

        self.assertTrue(hama_rhp_pop.dict[1].get_rhp() > hama_rhp_pop.dict[2].get_rhp())
        self.assertTrue(hama_rhp_pop.dict[3].get_rhp() > hama_rhp_pop.dict[1].get_rhp())
        self.assertTrue(hama_rhp_pop.dict[4].get_rhp() > hama_rhp_pop.dict[2].get_rhp())

    def test_challenge_outcome(self):
        dead2 = 0
        dead4 = 0

        for i in range(0, 1000):
            challenge_pop = self.setup_rhp()
            challenge_sim = HamadryasSim()

            challenge_pop.groupsdict[1].leadermales = [4]

            HamadryasSeed.addagenttoseed(1, challenge_pop.groupsdict[1], challenge_pop, 'f', None, None, 10)

            HamadryasDispersal.challenge(challenge_pop.dict[2], challenge_pop.dict[4], challenge_pop, challenge_sim)

            self.assertIn(5, challenge_pop.dict[4].females)

            HamadryasDispersal.challenge(challenge_pop.dict[1], challenge_pop.dict[4], challenge_pop, challenge_sim)

            if 2 not in challenge_pop.all:
                dead2 += 1
            if 4 not in challenge_pop.all:
                dead4 += 1

            self.assertIn(5, challenge_pop.dict[1].females)

        self.assertAlmostEqual(dead2, 500, delta=50)
        self.assertAlmostEqual(dead4, 500, delta=50)

    def test_rhp_assignment(self):

        agent = HamadryasAgent('m', None, None, None)
        self.assertEqual(agent.taxon, "hamadryas")

        score = MakeAgents.assignrhpcurve(HamadryasAgent('m', None, None, None))

        self.assertTrue(score)

    def test_sol_choices(self):
        sol_sim = HamadryasSim()

        became_leader = 0
        followed = 0
        died = 0

        for i in range(0, 1000):
            sol_pop = HamaPopulation()
            sol_pop = HamadryasSeed.makeseed(1, sol_pop)

            #  add a solitary
            HamadryasSeed.addagenttoseed(1, sol_pop.groupsdict[1], sol_pop, 'm', None, None, 20.5)
            our_guy = sol_pop.all[-1]
            our_guy = sol_pop.dict[our_guy]
            our_guy.maleState = MaleState.sol
            our_guy.clanID = 2

            sol_sim.get_young_natal_females(sol_pop)
            sol_sim.male_eligibility(sol_pop)

            self.assertTrue(sol_pop.groupsdict[1].leadermales)

            # give him choices
            sol_sim.male_choices(our_guy, sol_pop)

            if our_guy.index not in sol_pop.all:
                died += 1
            elif our_guy.maleState == MaleState.lea:
                became_leader += 1
            elif our_guy.maleState == MaleState.fol:
                followed += 1

        print became_leader, followed, died
        self.assertAlmostEqual(followed, 450, delta=45)
        self.assertAlmostEqual(became_leader, 250, delta=25)
        self.assertAlmostEqual(10, died, delta=5)

    def test_fol_choices(self):
        fol_sim = HamadryasSim()

        became_leader = 0
        followed = 0
        died = 0

        for i in range(0, 1000):
            fol_pop = HamaPopulation()
            fol_pop = HamadryasSeed.makeseed(1, fol_pop)
            fol_group = fol_pop.groupsdict[1]

            #  add a solitary
            HamadryasSeed.addagenttoseed(1, fol_group, fol_pop, 'm', None, None, 20.5)
            our_guy = fol_pop.all[-1]
            our_guy = fol_pop.dict[our_guy]
            our_guy.clanID = 2

            leader = random.choice([x for x in fol_group.leadermales if fol_pop.dict[x].clanID == 2])
            leader = fol_pop.dict[leader]
            HamadryasDispersal.follow(our_guy, leader, fol_pop)

            fol_sim.get_young_natal_females(fol_pop)
            fol_sim.male_eligibility(fol_pop)

            # give him choices
            fol_sim.male_choices(our_guy, fol_pop)

            if our_guy.index not in fol_pop.all:
                died += 1
            elif our_guy.maleState == MaleState.lea:
                self.assertTrue(our_guy.females)
                became_leader += 1
            elif our_guy.maleState == MaleState.fol:
                self.assertFalse(our_guy.females)
                followed += 1

        print became_leader, followed, died
        self.assertAlmostEqual(followed, 400, delta=100)
        self.assertAlmostEqual(became_leader, 600, delta=100)
        self.assertEqual(0, died)

    def test_disp_between_bands(self):
        pass

    def test_infanticide(self):
        pass

    def test_inherit_works(self):
        pass
