"""
AGENT: individual attributes
"""


class FemaleState:
    juvenile, cycling, pregnant, nursing0, nursing1 = range(5)


class MaleState:
    juvsol, sol, fol, lea = range(4)


class AgentClass:
    def __init__(self, sex, mother):
        #  defines an agent.py of any species
        self.index = 0

        self.age = 0.0
        self.sex = ""

        self.femaleState = None
        self.last_birth = 0

        self.lottery = []
        self.compability = None

        self.parents = []
        self.offspring = []

        self.dispersed = False

        self.taxon = ""

class HamadryasAgent(AgentClass):
    #  defines the attributes that a hamadryas baboon must have
    def __init__(self, taxon, clanID, bandID, OMU, maleState, females, malefols, femaleState):
        self.taxon = "hamadryas"

        self.clanID = ""
        self.bandID = ""
        self.OMU = ""
        self.maleState = None
        self.females = []
        self.malefols = []
        self.femaleState = None

class SavannahAgent(AgentClass):
    #  defines attributes that a generic (savannah) baboon must have
    def __init__(self, troopID, rhp, alphatenure=None):
        self.taxon = "savannah"
        self.troopID = troopID
        self.rhp = rhp
        self.alphatenure = alphatenure


class GeladaAgent(AgentClass):
    #  defines the attributes that a gelada must have
    taxon = "gelada"

    OMU = ""
    maleState = None
    females = []
    malefols = []
