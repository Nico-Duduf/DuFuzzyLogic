from .fz_veracity import FuzzyVeracity
from .fz_logicalgorithm import FuzzyLogicAlgorithm

class FuzzyQuantifier():
    """! Enum of available quantifiers. """

    ## This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
    IS_NOT = "Not"
    ## This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
    LESS = "Less"
    ## Slightly
    DOUBLE_MINUS = "Slightly"
    ## Somewhat
    MINUS = "Somewhat"
    ## Moderately
    AVERAGE = "Moderately"
    ## None
    NONE = ""
    ## Very
    PLUS = "Very"
    ## Extremely
    DOUBLE_PLUS = "Extremely"
    ## This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
    IS = "Completely"
    ## This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
    MORE = "More"

    FuzzyQuantifierList = {
        IS_NOT: "Not", LESS: "Less", DOUBLE_MINUS: "Slightly", MINUS: "Somewhat", AVERAGE: "Moderately",
        NONE: "", PLUS: "Very", DOUBLE_PLUS: "Extremely", IS: "Completely", MORE: "More"
    }

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
            v = pow(veracity, 1 / 3)

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
            return pow(0.5, 1 / 3)
        if inverse:
            v = pow(veracity, 1 / 3)
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
