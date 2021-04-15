from DuFuzzyLogic.src.Python.dufuzzylogic.FuzzyQuantifier import FuzzyQuantifier
from DuFuzzyLogic.src.Python.dufuzzylogic.FuzzyVeracity import *

"""
    low-level undocumented method
    adjusts an existing veracity according to the quantifier
    returns a new adjusted veracity
    or returns a factor if veracity is undefined
"""

def quantify(quantifier, veracity=None, algorithm=FuzzyLogicAlgorithm, inverse=True):  # Vérifier les valeurs par défaut... :-/
    v = veracity

    if quantifier == FuzzyQuantifier.IS_NOT or quantifier == FuzzyQuantifier.LESS:
        if veracity is None:
            return 0
        if inverse:
            v = 0
        else:
            v = 1

    elif quantifier == FuzzyQuantifier.DOUBLE_MINUS:
        if veracity is None:
            return pow(0.5, 3)
        if inverse:
            v = pow(veracity, 3)
        else:
            v = pow(veracity, 1/3)

    elif quantifier == FuzzyQuantifier.MINUS:
        if veracity is None:
            return pow(0.5, 2)
        if inverse:
            v = pow(veracity, 2)
        else:
            v = pow(veracity, 0.5)

    elif quantifier == FuzzyQuantifier.AVERAGE or quantifier == FuzzyQuantifier.NONE:
        if veracity is None:
            return 0.5

    elif quantifier == FuzzyQuantifier.PLUS:
        if veracity is None:
            return pow(0.5, 0.5)
        if inverse:
            v = pow(veracity, 0.5)
        else:
            v = pow(veracity, 2)

    elif quantifier == FuzzyQuantifier.DOUBLE_PLUS:
        if veracity is None:
            return pow(0.5, 1/3)
        if inverse:
            v = pow(veracity, 1/3)
        else:
            v = pow(veracity, 3)

    elif quantifier == FuzzyQuantifier.IS or quantifier == FuzzyQuantifier.MORE:
        if veracity is None:
            return 1
        if inverse:
            v = 1
        else:
            v = 0

    return FuzzyVeracity(v, algorithm)
