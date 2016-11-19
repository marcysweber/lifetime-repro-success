import random

from agent import *
from completesimulation import *


class HamadryasDispersal:
    @staticmethod
    def sol_choices(male, population):
        #  either do nothing, initial unit, challenge, or follow
        pass

    @staticmethod
    def follow(follower, leader, population):
        pass

    @staticmethod
    def challenge(challenger, leader, population):
        pass

    @staticmethod
    def fol_choices(male, population):
        #  either do nothing, start initial unit
        pass

    @staticmethod
    def attempt_init_unit(male, population):
        lottery = []
        chance = 0.0

        for female in population.young_natal_females:
            female = population.dict[female]
            if female.OMUID == male.OMUID:
                assert male.maleState == MaleState.fol
                lottery += [female.index]

            else:
                if male.maleState == MaleState.sol:
                    if male.clanID == female.clanID:
                        for i in range(0, 20):
                            lottery += [female.index]
                    elif male.bandID == female.bandID:
                        for i in range(0, 10):
                            lottery += [female.index]
                    else:
                        lottery += [female.index]
                else:
                    pass

        if male.maleState == MaleState.fol:
            chance = 0.85
        elif male.maleState == MaleState.sol:
            chance = 0.5

        female = population.dict[random.choice(lottery)]
        if random.uniform(0, 1) < chance:
            HamadryasDispersal.add_female_to_omu(male, female, population)

    @staticmethod
    def inherit_females(dead_leader, population):
        females = dead_leader.females
        males = dead_leader.malefols

        for male in males:
            male = population.dict[male]
            female = random.choice(females)
            female = population.dict[female]
            if random.uniform(0, 1) < 0.9:  # 90% chance of inheriting
                HamadryasDispersal.add_female_to_omu(male, female, population)

    @staticmethod
    def opportun_takeover(female, population):

        lottery = []

        for male in population.eligible_males:
            male = population.dict[male]
            reps = 1
            if female.bandID != male.bandID:
                reps = 1
            else:  # in the same band
                reps = reps * 4
                if female.clanID == male.clanID:  # and also clan
                    reps = reps * 4
            if male.maleState == MaleState.lea and not male.malefols:
                reps = reps - int(reps * 0.33)

            for i in range(0, reps):
                lottery += [male.index]

        winner = population.dict[random.choice(lottery)]
        HamadryasDispersal.add_female_to_omu(winner, female, population)

    @staticmethod
    def add_female_to_omu(male, female, population):
        if female.offspring:
            if population.dict[female.offspring[-1]].age < 2:
                Simulation.killagent(simulation, female.offspring[-1], population, female.bandID, population.halfyear)
                female.femaleState = FemaleState.cycling

        if male.maleState == MaleState.fol:
            population.dict[male.OMUID].malefols.remove(male.index)

        if female.dispersed:
            population.dict[female.OMUID].females.remove(female.index)
        else:
            female.dispersed = True

        male.OMUID = male.index
        male.females.append(female.index)
        male.maleState = MaleState.lea

        population.dict[female.OMUID].females.remove(female.index)

        if female.bandID != male.bandID:
            female.bandID = male.bandID
            population.groupsdict[male.bandID].agents.append(female.index)
            population.groupsdict[female.bandID].agent.remove(female.index)

        female.clanID = male.clanID
        female.OMUID = male.index


class SavannahDispersal:
    @staticmethod
    def disperse(male, pop):
        cand_groups = []

        for group in pop.groupsdict:
            group = pop.groupsdict[group]
            if group.index is not male.troopID:
                group.excess_females = group.get_excess_females(pop)
                cand_groups.append(group)

        group_lots = []
        for group in cand_groups:
            this_group_lots = group.excess_females + 15
            for i in range(0, this_group_lots):
                group_lots.append(group.index)

        dest_group = random.choice(group_lots)
        dest_group = pop.groupsdict[dest_group]

        pop.groupsdict[male.troopID].agents.remove(male.index)
        male.troopID = dest_group.index
        dest_group.agents.append(male.index)
        if not male.dispersed:
            male.dispersed = True
