import random


class HamadryasPaternity:
    def hamadryassire(self, mother):
        sire = population.dict[mother.OMU].index
        return sire


class SavannahPaternity:
    @staticmethod
    def savannahsire(mother, dominance_hierarchy, population):
        sire = None

        n = float(len(dominance_hierarchy))
        at = population.dict[dominance_hierarchy[0]].alphatenure
        m = (n - at) / (n + at)
        if m < 0.1:
            m = 0.1

        ticketbreaks = [1000]
        #  start with 0-1000 for alpha

        for male in dominance_hierarchy[1:]:
            ticketbreaks.append(int((m * (ticketbreaks[-1]))))

        for i in range(1, len(ticketbreaks)):
            ticketbreaks[i] = ticketbreaks[i] + ticketbreaks[i - 1]

        draw = random.randrange(0, ticketbreaks[-1])

        for j in range(len(ticketbreaks)):
            if draw < ticketbreaks[j]:
                sire = dominance_hierarchy[j]
                break

        return sire
