"""
This file contains:
- reproductive functions
- promotion of agents (i.e. increases age per turn)
- death of agents
"""
from agent import FemaleState


def promote_agent(this_agent):
    this_agent.age += 0.5

    if this_agent.femaleState:
        if this_agent.femaleState == FemaleState.nursing0:
            this_agent.femaleState = FemaleState.nursing1
        elif this_agent.femaleState == FemaleState.nursing1:
            this_agent.femaleState = FemaleState.cycling
