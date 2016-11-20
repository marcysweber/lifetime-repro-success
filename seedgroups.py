import random

from agent import MaleState, MakeAgents
from group import SavannahGroup, HamadryasGroup


class SavannahSeed:
    @staticmethod
    def makeseed(groupindex, population):
        group = SavannahGroup(groupindex)

        #  make the seed agents here
        for i in range(0, 16):
            #  make 16 adult females of any age
            SavannahSeed.addagenttoseed(groupindex, group, population, 'f', None, None,
                                        (float(random.randrange(10, 50)) / 2.0))

        for j in range(0, 15):
            #  make 15 non-adult females of any age
            SavannahSeed.addagenttoseed(groupindex, group, population, 'f', None, None,
                                        (float(random.randrange(0, 9)) / 2.0))

        for k in range(0, 8):
            #  make 8 adult males of any age
            SavannahSeed.addagenttoseed(groupindex, group, population, 'm', None, None,
                                        (float(random.randrange(15, 40)) / 2.0))

        for l in range(0, 15):
            #  make 15 non-adult males of any age
            SavannahSeed.addagenttoseed(groupindex, group, population, 'm', None, None,
                                        (float(random.randrange(0, 14)) / 2.0))

        population.groupsdict[groupindex] = group

        return population

    @staticmethod
    def addagenttoseed(groupindex, group, population, sex, mother, sire, age):
        newagent = MakeAgents.makenewsavannah(groupindex, sex, mother, sire, population, age)
        population.all.append(newagent.index)
        population.dict[newagent.index] = newagent
        group.agents.append(newagent.index)


class HamadryasSeed:
    @staticmethod
    def makeseed(groupindex, population):
        group = HamadryasGroup(groupindex)

        #  make adult males
        for i in range(0, 13):
            HamadryasSeed.addagenttoseed(groupindex,
                                         group, population, 'm', None, None,
                                         (float(random.randrange(12.0, 40.0)) / 2.0))

        # make some leaders, fols, and sols, and give clans and OMUs
        for j in range(0, len(group.agents)):
            male = population.dict[group.agents[j]]
            if j < 3:
                male.clanID = 1
                if j == 0 or j == 2:
                    male.maleState = MaleState.lea
                    male.OMU = male.index
                    group.leadermales.append(male.index)
                else:
                    male.maleState = MaleState.fol
                    male.OMU = group.agents[j - 1]
                    population.dict[group.agents[j - 1]].malefols.append(male.index)

            elif j < 8:
                male.clanID = 2

                if j == 3 or j == 5 or j == 6:
                    male.maleState = MaleState.lea
                    male.OMU = male.index
                    group.leadermales.append(male.index)

                elif j == 4:
                    male.maleState = MaleState.fol
                    male.OMU = group.agents[j - 1]
                    population.dict[group.agents[j - 1]].malefols.append(male.index)

                else:
                    male.maleState = MaleState.sol
                    male.OMU = None
            else:
                male.clanID = 3
                if j < 11:
                    male.maleState = MaleState.lea
                    male.OMU = male.index
                    group.leadermales.append(male.index)

                elif j == 11:
                    male.maleState = MaleState.fol
                    male.OMU = group.agents[j - 1]
                    population.dict[group.agents[j - 1]].malefols.append(male.index)

                else:
                    male.maleState = MaleState.sol
                    male.OMU = None

        for k in range(0, 23):
            HamadryasSeed.addagenttoseed(groupindex, group, population, 'f', None, None,
                                         (float(random.randrange(10.0, 40.0)) / 2.0))

        for l in range(0, 15):
            HamadryasSeed.addagenttoseed(groupindex, group, population, 'f', None, None,
                                         (float(random.randrange(0.0, 10.0)) / 2.0))

        for m in range(0, 14):
            HamadryasSeed.addagenttoseed(groupindex, group, population, 'm', None, None,
                                         (float(random.randrange(0.0, 11.0)) / 2.0))

        assert len(group.leadermales) == 8

        population.groupsdict[groupindex] = group

        return population

    @staticmethod
    def addagenttoseed(groupindex, group, population, sex, mother, sire, age):
        newagent = MakeAgents.makenewhamadryas(groupindex, sex, mother, sire, population, age)

        # assign adult females and all non-adults randomly to OMUs
        if newagent.sex == 'f' or newagent.age < 5.0:
            leaderindex = random.choice(group.leadermales)
            newagent.OMUID = leaderindex
            leader = population.dict[leaderindex]
            newagent.clanID = leader.clanID
            if newagent.sex == 'f' and newagent.age >= 5.0:
                leader.females.append(newagent.index)

        population.all.append(newagent.index)
        population.dict[newagent.index] = newagent
        group.agents.append(newagent.index)
