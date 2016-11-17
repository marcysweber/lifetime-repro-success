import random

import aging
import lifetables
from agent import SavannahAgent, HamadryasAgent, FemaleState, MaleState, MakeAgents
from paternity import HamadryasPaternity, SavannahPaternity
from seedgroups import SavannahSeed


def main():
    hamadryas = HamadryasSim()
    # gelada = GeladaSim()
    savannah = SavannahSim()

    hamadryas.run_simulation()
    # gelada.run_simulation()
    savannah.run_simulation()


class Population:
    def __init__(self):
        self.all = []
        self.dict = {}
        #    females = dict.sex = 'f'
        #    males = dict.sex = 'm'
        self.groupsdict = {}
        self.topeverindex = 0


class Simulation:
    #  to hold generic functions pertaining to any/most sims.

    def mortality_check(self, population):
        ret = 0
        for agentindex in list(population.all):
            agent = population.dict[agentindex]
            getdeathchance = lifetables.getdeathchance(agent)
            dieroll = random.uniform(0, 1)
            if getdeathchance >= dieroll:
                ret += self.killagent(agent, population, population.groupsdict[agent.troopID])
        return ret

    def birth_check(self, population, halfyear):
        for agentindex in population.all:
            agent = population.dict[agentindex]
            if agent.sex == 'f':
                if agent.femaleState == FemaleState.cycling:
                    birthchance = lifetables.getbirthchance(agent)
                    dieroll = random.uniform(0, 1)
                    if birthchance >= dieroll:
                        self.birthagent(agent, population, halfyear)


    def promotions(self, population):
        for agent in population:
            aging.Promote.promote_agent(agent)

    def killagent(self, agent, population, group):
        del population.dict[agent.index]
        population.all.remove(agent.index)
        group.agents.remove(agent.index)
        assert agent.index not in population.all
        return 1

    def birthagent(self, mother, population, halfyear):
        sex = random.choice('m', 'f')

        if mother.taxon == "hamadryas":
            group = mother.bandID

            infant = MakeAgents.makenewhamadryas(group, sex, mother.index,
                                                 HamadryasPaternity.hamadryassire(mother, population, halfyear),
                                                 population)
            infant.OMU = mother.OMU
            infant.clanID = mother.clanID

        elif mother.taxon == "savannah":
            group = mother.troopID
            dom_hier = population.groupsdict[group].dominance_hierarchy

            infant = MakeAgents.makenewsavannah(group, sex, mother.index,
                                                SavannahPaternity.savannahsire(dom_hier, population, halfyear),
                                                population)

        population.all.append(infant.index)
        population.dict[infant.index] = infant
        population.groupsdict[group].agents.append(infant.index)

        #  also add here specialized lists!!!
"""
TAXA SPECIFIC CLASSES BELOW
are designed to hold schedules.
Schedules can vary between species to allow for
completely different functions e.g. takeovers
in hamadryas baboons and male dispersal in savannah.
"""


class HamadryasSim(Simulation):
    #  loop with unique functions when needed
    def run_simulation(self):
        population = Population()

        for halfyear in range(0, 400):
            self.mortality_check(population)

            self.birth_check(population, halfyear)

            self.promotions(population)


class GeladaSim(Simulation):
    #  loop with unique functions when needed
    def run_simulation(self):
        pass

class SavannahSim(Simulation):
    #  loop with unique functions when needed
    def run_simulation(self):
        population = Population()

        #  loop here for seed group/population
        for groupindex in range(0, 10):
            population = SavannahSeed.makeseed(groupindex, population)

        for halfyear in range(0, 400, 1):
            self.mortality_check(population)

            self.dispersal_check(population)

            for group in population.groupsdict.keys():
                group = population.groupsdict[group]
                self.dominance_calc(population, group)

            self.birth_check(population, halfyear)

            self.promotions(population)

    def dispersal_check(self, population):
        pass

    def dominance_calc(self, population, group):

        agents_in_group = [population.dict[idx] for idx in group.agents]
        adult_males = []

        for agent in agents_in_group:
            if agent.sex == "m":
                if agent.dispersed:
                    adult_males.append(agent)

        sorted_by_rhp = sorted(adult_males, key=lambda agent: agent.get_rhp(), reverse=True)
        dominance_hierarchy = [agent.index for agent in sorted_by_rhp]

        print sorted_by_rhp

        print sorted_by_rhp[0]

        alpha = sorted_by_rhp[0]
        tenure = alpha.alpha_tenure
        if tenure is not None:
            sorted_by_rhp[0].alpha_tenure += 0.5
        else:
            sorted_by_rhp[0].alpha_tenure = 0.5

        group.dominance_hierarchy = dominance_hierarchy
