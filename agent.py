"""
AGENT: individual attributes
"""

class FemaleState:
    juvenile, cycling, pregnant, nursing0, nursing1 = range(5)

class MaleState:
    juvsol, sol, fol, lea = range(4)

class AgentClass:
    #  defines an agent.py of any species
    index = 0

    age = 0.0
    sex = ""

    femaleState = None
    last_birth = 0

    lottery = []
    compability = None

    parents = []
    offspring = []

    dispersed = False

    taxon = ""

    def make_new_agent(self, mother):

class HamadryasAgent(AgentClass):
    #  defines the attributes that a hamadryas baboon must have
    taxon = "hamadryas"

    clanID = ""
    bandID = ""
    OMU = ""
    maleState = None
    females = []
    malefols = []

class SavannahAgent(AgentClass):
    #  defines attributes that a generic (savannah) baboon must have
    taxon = "savannah"

    troopID = ""

class GeladaAgent(AgentClass):
    #  defines the attributes that a gelada must have
    taxon = "gelada"

    OMU = ""
    maleState = None
    females = []
    malefols = []

