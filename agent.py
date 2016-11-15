"""
AGENT: individual attributes
"""
import random

class FemaleState:
    juvenile, cycling, pregnant, nursing0, nursing1 = range(5)


class MaleState:
    juvsol, sol, fol, lea = range(4)


class AgentClass:
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

class HamadryasAgent(AgentClass):
    #  defines the attributes that a hamadryas baboon must have
    def __init__(self, sex, mother, sire, clanID, bandID, OMU):
        self.taxon = "hamadryas"

        self.clanID = clanID
        self.bandID = bandID
        self.OMU = OMU
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
    def makenewsavannah(troopID, sex, mother, sire, age=0):

        newagent = SavannahAgent(sex, mother, sire, troopID)

        newagent.age = age

        if newagent.sex == 'm':
            newagent.rhp = random.randrange(0, 4)
        else:
            newagent.femaleState = FemaleState.juvenile

        return newagent


class GeladaAgent(AgentClass):
    #  defines the attributes that a gelada must have
    taxon = "gelada"

    OMU = ""
    maleState = None
    females = []
    malefols = []
