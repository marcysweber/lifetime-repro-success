"""
AGENT: individual attributes
"""


class FemaleState:
    juvenile, cycling, pregnant, nursing0, nursing1 = range(5)


class MaleState:
    juvsol, sol, fol, lea = range(4)


class SavannahRhp:
    type1 = []
    type2 = []
    type3 = []
    type4 = []
    type5 = []


class HamadryasRhp:
    type1 = []
    type2 = []
    type3 = []
    type4 = []


class AgentClass(object):
    def __init__(self, sex, mother, sire):
        #  defines an agent.py of any species
        self.index = 0

        self.age = 0.0
        self.sex = sex

        self.femaleState = None
        self.last_birth = 0

        self.lottery = []
        self.compability = None

        self.parents = [mother, sire]
        self.offspring = []

        self.dispersed = False

        self.taxon = ""

        #  set to True if born during sim
        self.born = False

class HamadryasAgent(AgentClass):
    #  defines the attributes that a hamadryas baboon must have
    def __init__(self, sex, mother, sire, bandID):
        self.taxon = "hamadryas"

        self.clanID = None
        self.bandID = bandID
        self.OMU = None
        self.maleState = None
        self.females = []
        self.malefols = []
        self.femaleState = None
        self.maleState = None

        super(HamadryasAgent, self).__init__(sex, mother, sire)

class SavannahAgent(AgentClass):
    #  defines attributes that a generic (savannah) baboon must have
    def __init__(self, sex, mother, sire, troopID):
        self.taxon = "savannah"
        self.troopID = troopID
        self.rhp = None
        self.alpha_tenure = None

        super(SavannahAgent, self).__init__(sex, mother, sire)


class MakeAgents:
    @staticmethod
    def makenewsavannah(troopID, sex, mother, sire, population, age=0.0):

        newagent = SavannahAgent(sex, mother, sire, troopID)

        newagent.age = age

        if newagent.sex == 'm':
            newagent.rhp = MakeAgents.assignrhpcurve(newagent)
        else:
            newagent.femaleState = FemaleState.juvenile

        newagent.index = MakeAgents.get_unique_index(population)

        #  parents get credit
        if sire and mother:
            population.dict[sire].offspring.append(newagent.index)
            population.dict[mother].offspring.append(newagent.index)

        return newagent

    @staticmethod
    def makenewhamadryas(bandID, sex, mother, sire, population, age=0.0):
        newagent = HamadryasAgent(sex, mother, sire, bandID)
        newagent.age = age

        if newagent.sex == 'm':
            newagent.rhp = MakeAgents.assignrhpcurve(newagent)
        else:
            newagent.femaleState = FemaleState.juvenile

        newagent.index = MakeAgents.get_unique_index(population)

        #  parents get credit
        if sire and mother:
            population.dict[sire].offspring.append(newagent.index)
            population.dict[mother].offspring.append(newagent.index)

        return newagent

    @staticmethod
    def assignrhpcurve(agent):
        if agent.taxon == "hamadryas":
            return 0
        elif agent.taxon == "savannah":
            return 0

    @staticmethod
    def get_unique_index(population):
        newindex = population.topeverindex + 1
        population.topeverindex = newindex
        return newindex


class GeladaAgent(AgentClass):
    #  defines the attributes that a gelada must have
    taxon = "gelada"

    OMU = ""
    maleState = None
    females = []
    malefols = []
