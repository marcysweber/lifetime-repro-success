import aging


def main():
    hamadryas = HamadryasSim()
    # gelada = GeladaSim()
    savannah = SavannahSim()

    hamadryas.run_simulation()
    # gelada.run_simulation()
    savannah.run_simulation()


class Population:
    all = []
    dict = {}
    #    females = dict.sex = 'f'
    #    males = dict.sex = 'm'
    groupsdict = {}


class Simulation:
    #  to hold generic functions pertaining to any/most sims.

    def mortality_check(self, population):
        for agent in population:
            pass

    def birth_check(self, population):
        for agent in population:
            pass

    def promotions(self, population):
        for agent in population:
            aging.Promote.promote_agent(agent)


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

        self.mortality_check(population)

        self.birth_check(population)

        self.promotions(population)


class GeladaSim(Simulation):
    #  loop with unique functions when needed
    def run_simulation(self):
        pass

class SavannahSim(Simulation):
    #  loop with unique functions when needed
    def run_simulation(self):
        population = Population()

        for halfyear in range(0, 400, 1):
            self.mortality_check(population)

            self.dispersal_check(population)

            self.dominance_calc(population)

            self.birth_check(population)

            self.promotions(population)

    def dispersal_check(self, population):
        pass

    def dominance_calc(self, population):
        for group in population.groupsdict:
            agents_in_group = [population.dict[idx] for idx in population.groupsdict[group]]
            sorted_by_rhp = sorted(agents_in_group, key=lambda agent: agent.rhp, reverse=True)
            dominanace_hierarchy = [agent.index for agent in sorted_by_rhp]
            return dominanace_hierarchy
