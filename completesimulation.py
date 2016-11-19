import random

import aging
import lifetables
from agent import MakeAgents, MaleState, FemaleState
from dispersal import SavannahDispersal, HamadryasDispersal
from paternity import HamadryasPaternity, SavannahPaternity
from seedgroups import SavannahSeed, HamadryasSeed


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
        self.groupsdict = {}
        self.topeverindex = 0
        self.halfyear = 0


class HamaPopulation(Population):
    def __init__(self):
        self.avail_females = []
        self.eligible_males = []
        self.young_natal_females = []
        super(HamaPopulation, self).__init__()


class SavPopulation(Population):
    def __init__(self):
        super(SavPopulation, self).__init__()

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
        if agent.sex == 'f':
            if agent.offspring:
                if population.dict[agent.offspring[-1]].age < 2:
                    self.killagent(population.dict[agent.offspring[-1]], population, group, halfyear)
        if agent.females:  # if he is a hamadryas leader male
            if agent.malefols:  # malefols inherit first
                HamadryasDispersal.inherit_females(agent, population)
            # after inheritance, females are "up for grabs"
            population.avail_females.append(agent.females)
        if agent.taxon == "hamadryas" and agent.sex == 'f':
            if agent.dispersed:
                population.dict[agent.OMUID].females.remove(agent.index)

            if agent.index in population.avail_females:
                population.avail_females.remove(agent.index)
        if agent.age <= 1:
            if agent.parents:
                population.dict[agent.parents[0]].femaleState = FemaleState.cycling
        if halfyear > 40:
            self.siring_success.append(len(agent.offspring))

        del population.dict[agent.index]
        population.all.remove(agent.index)
        group.agents.remove(agent.index)
        assert agent.index not in population.all

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
        population = HamaPopulation()

        for groupindex in range(0, 10):
            population = HamadryasSeed.makeseed(groupindex, population)

        for halfyear in range(0, 400):
            population.halfyear = halfyear

            self.mortality_check(population)
            self.male_eligibility(population)
            self.get_young_natal_females(population)

            if population.avail_females:
                for female in population.avail_females:
                    female = population.dict[female]
                    HamadryasDispersal.opportun_takeover(female, population)
                population.avail_females = []
            males = [male for male in population.dict.values() if male.sex == 'm']
            for male in males:
                self.male_choices(male, population)
            if population.avail_females:
                for female in population.avail_females:
                    female = population.dict[female]
                    HamadryasDispersal.opportun_takeover(female, population)
                population.avail_females = []

            self.birth_check(population, halfyear)
            self.promotions(population)

    def male_eligibility(self, population):
        population.eligible_males = []
        for agent in population.dict.values():
            if agent.sex == 'm':
                if agent.dispersed:
                    if agent.maleState is not MaleState.juvsol or MaleState.fol:
                        population.eligible_males.append(agent.index)
                        if agent.maleState == MaleState.lea:
                            population.groupsdict[agent.bandID].leadermales.append(agent.index)

    def get_young_natal_females(self, population):
        population.young_natal_females = []

        for agent in population.dict.values():
            if agent.sex == 'f':
                if 2 <= agent.age < 5:
                    population.young_natal_females.append(agent.index)
                elif agent.age == 5:
                    population.avail_females.append(agent.index)

    def male_choices(self, male, population):
        if male.maleState == MaleState.fol:
            HamadryasDispersal.fol_choices(male, population, self)
        elif male.maleState == MaleState.sol:
            HamadryasDispersal.sol_choices(male, population, self)
        elif male.maleState == MaleState.lea:
            if not male.females:
                male.maleState = MaleState.sol
                male.OMUID = None
                if male.malefols:
                    for malefol in male.malefols:
                        malefol = population.dict[malefol]
                        malefol.maleState = MaleState.sol
                        malefol.OMUID = None
            #  leaders have no choices
            pass


class GeladaSim(Simulation):
    #  loop with unique functions when needed
    def run_simulation(self):
        pass

class SavannahSim(Simulation):
    #  loop with unique functions when needed
    def run_simulation(self):
        population = SavPopulation()

        #  loop here for seed group/population
        for groupindex in range(0, 10):
            population = SavannahSeed.makeseed(groupindex, population)

        for halfyear in range(0, 400, 1):
            population.halfyear = halfyear

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
