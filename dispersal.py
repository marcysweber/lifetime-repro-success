import random

class HamadryasDispersal:
    pass

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
