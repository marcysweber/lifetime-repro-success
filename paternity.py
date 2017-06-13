import random


class HamadryasPaternity:
    @staticmethod
    def hamadryassire(mother, population, halfyear):
        sire = None
        if halfyear >= 40:
            sire = population.dict[mother.OMUID].index
        return sire


class SavannahPaternity:
    @staticmethod
    def savannahsire(dominance_hierarchy, population, halfyear):
        sire = None

        n = float(len(dominance_hierarchy))
        at = population.dict[dominance_hierarchy[0]].alpha_tenure
        m = (n - at) / (n + at)
        if m < 0.1:
            m = 0.1

        ticketbreaks = [1000]
        #  start with 0-1000 for alpha

        for male in dominance_hierarchy[1:]:
            ticketbreaks.append(int((m * (ticketbreaks[-1]))))

        for i in range(1, len(ticketbreaks)):
            ticketbreaks[i] += ticketbreaks[i - 1]

        draw = random.randrange(0, ticketbreaks[-1])

        for j in range(len(ticketbreaks)):
            if draw < ticketbreaks[j]:
                sire = dominance_hierarchy[j]
                break

        return sire


class GeladaPaternity:
    @staticmethod
    def geladasire(mother, population, halfyear):
        sire = None
        if halfyear >= 40:
            leader = population.dict[mother.OMUID]

            p = random.uniform(0, 1)

            if p >= 0.17 or not leader.malefols:
                sire = leader.index
            else:
                sire = random.choice(leader.malefols)

        return sire
