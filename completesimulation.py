import random

import aging
import lifetables
from agent import FemaleState, MakeAgents
from dispersal import SavannahDispersal
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

    def __init__(self):
        self.siring_success = []

    def mortality_check(self, population, halfyear):
        ret = 0
        for agentindex in list(population.all):
            agent = population.dict[agentindex]
            getdeathchance = lifetables.getdeathchance(agent)
            dieroll = random.uniform(0, 1)
            if getdeathchance >= dieroll:
                ret += self.killagent(agent, population, population.groupsdict[agent.troopID], halfyear)
        return ret

    def birth_check(self, population, halfyear):
        for agentindex in population.all:
            agent = population.dict[agentindex]
            if agent.sex == 'f':
                if agent.femaleState == FemaleState.cycling:
                    birthchance = lifetables.getbirthchance(agent)
                    dieroll = random.uniform(0, 1)
                    if birthchance >= dieroll:
                        agent.femaleState = FemaleState.pregnant
                elif agent.femaleState == FemaleState.pregnant:
                    self.birthagent(agent, population, halfyear)
                    agent.femaleState = FemaleState.nursing0


    def promotions(self, population):
        for agent in population.dict.keys():
            agent = population.dict[agent]
            aging.promote_agent(agent)

    def killagent(self, agent, population, group, halfyear):
        del population.dict[agent.index]
        population.all.remove(agent.index)
        group.agents.remove(agent.index)
        assert agent.index not in population.all

        if agent.offspring:
            if population.dict[agent.offspring[-1]].age < 2:
                self.killagent(population.dict[agent.offspring[-1]], population, group, halfyear)

        if halfyear > 40:
            self.siring_success.append(len(agent.offspring))

        return 1

    def birthagent(self, mother, population, halfyear):
        sex = random.choice(['m', 'f'])

        if mother.taxon == "hamadryas":
            group = mother.bandID
            sire = HamadryasPaternity.hamadryassire(mother, population, halfyear)

            infant = MakeAgents.makenewhamadryas(group, sex, mother.index,
                                                 sire,
                                                 population)
            infant.OMU = mother.OMU
            infant.clanID = mother.clanID

        elif mother.taxon == "savannah":
            group = mother.troopID
            dom_hier = population.groupsdict[group].dominance_hierarchy
            sire = SavannahPaternity.savannahsire(dom_hier, population, halfyear)

            infant = MakeAgents.makenewsavannah(group, sex, mother.index,
                                                sire,
                                                population)

        mother.offspring.append(infant.index)
        mother.last_birth = halfyear
        population.dict[sire].offspring.append(infant.index)
        population.dict[sire].last_birth = halfyear


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
            self.mortality_check(population, halfyear)

            self.dispersal_check(population, halfyear)

            for group in population.groupsdict.keys():
                group = population.groupsdict[group]
                self.dominance_calc(population, group)

            self.birth_check(population, halfyear)

            self.promotions(population)

    def dispersal_check(self, population, halfyear):
        random.shuffle(population.all)
        for agent in population.all:
            agent = population.dict[agent]
            if agent.sex == 'm' and agent.age > 7:
                if agent.last_birth > halfyear - 2:
                    if population.groupsdict[agent.troopID].get_excess_females(population) < 1:
                        if random.uniform(0, 1) <= 0.5:
                            SavannahDispersal.disperse(agent, population)

    def dominance_calc(self, population, group):

        agents_in_group = [population.dict[idx] for idx in group.agents]
        adult_males = [x for x in agents_in_group if x.sex == "m" and x.dispersed]
        group.sorted_by_rhp = sorted(adult_males, key=lambda agent: agent.get_rhp(), reverse=True)
        dominance_hierarchy = [agent.index for agent in group.sorted_by_rhp]

        group.dominance_hierarchy = dominance_hierarchy

        alpha = population.dict[group.dominance_hierarchy[0]]
        tenure = alpha.alpha_tenure
        if tenure is not None:
            alpha.alpha_tenure += 0.5
        else:
            alpha.alpha_tenure = 0.5
