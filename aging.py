"""
This file contains:
- reproductive functions
- promotion of agents (i.e. increases age per turn)
- death of agents
"""
from agent import AgentClass, FemaleState


class Reproduction:
    def chance_of_preg(self, age):
        pass

    # chance of preg is a function of age using lifetable


    def get_pregnant(self, this_agent, current_pop_dict):
        #  unborn agents need to have fathers. Savannah baboons could
        #  sire agents and then disperse "immediately".

        assert this_agent.sex == "f"
        assert this_agent.femaleState == FemaleState.cycling

        if self.chance_of_preg(this_agent.age):
            pass
    def give_birth(self, mother, current_pop_dict):
        assert mother.femaleState == FemaleState.pregnant
        #  AS OFFSPRING ARE BORN, MAKE SURE THEY ARE ADDED
        #  TO THE BEGINNING OF AGENT.OFFSPRING ARRAY

        newborn = AgentClass.make_new_agent(mother)

        mother.offspring = [newborn.index] + mother.offspring


class Promote:
    def promote_agent(self, this_agent):
        this_agent.age += 0.5


class Death:
    def check_depen_offspring(self, dead_agent, current_pop_dict):
        assert dead_agent.sex == "f"
        if dead_agent.offspring:
            offspring = current_pop_dict[dead_agent.offspring[0]]
            if offspring.age < 1.5:
                self.die(offspring, current_pop_dict)

    def die(self, this_agent, current_pop_dict):
        pass
