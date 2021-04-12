from FuzzyVeracity import *
from FuzzyVeracity import *
from FuzzyLogic import *
import math

class FuzzyQuantifier():
    def __init__(self, name, quantifyValue):
        self.name = name
        self._quantifyValue = quantifyValue

    def quantify(self, value, algorithm, inverse):
        if not value:
            math.pow( 0.5, 1/self._quantifyValue )
        if inverse:
            p = 1/self._quantifyValue
        else:
            p = self._quantifyValue
        return FuzzyVeracity( math.pow(value, p), algorithm)

class FuzzyQuantifierIS_NOT( FuzzyQuantifier ):
    def __init__(self):
        self.name = "Not"

    def quantify( self, value, algorithm, inverse):
        """
        This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
        @type {string}
        @default "Not"

        :param v:
        :param algorithm:
        :param inverse:
        :return:
        """
        if value is None:
            return 0
        if inverse:
            q = 0
        else:
            q = 1
        return FuzzyVeracity(q, algorithm)

FuzzyQuantifiers = {
    'DOUBLE_MINUS' = FuzzyQuantifier( 1 / 3, "Slightly" ),
    'IS_NOT' = FuzzyQuantifierIS_NOT()
}  

def getQuantifier(quantifier):
    """low-level undocumented function.
    gets a quantifier by its name"""
    if not quantifier:
        return FuzzyQuantifier['AVERAGE']

    try:
        n = quantifier.name
        return quantifier
    except:
        for q in FuzzyQuantifiers:
            if q.name == quantifier:
                return q

    raise Exception("Quantifier : " + str(quantifier) + " is unknown.")

# ========= ENUMS =============

# Quantifiers


def LESS(v, algorithm, inverse):
    """
    This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
    @type {string}
    @default "Less"
    :param v:
    :param algorithm:
    :param inverse:
    :return:
    """
    if v is None:
        return 0
    if inverse:
        q = 0
    else:
        q = 1


def LESS_ToString():
    return "Less"


FuzzyQuantifier.DOUBLE_MINUS = createQuantifier(1 / 3, "Slightly")
"""
@type {string}
@default "Slightly"
"""

FuzzyQuantifier.MINUS = createQuantifier(0.5, "Somewhat")
"""
@type {string}
@default "Somewhat"
"""


def AVERAGE(v, algorithm):
    """
    @type {string}
    @default "Moderately"
    :param v:
    :param algorithm:
    :return:
    """
    if v is None:
        return 0.5
    else:
        return FuzzyVeracity(v, algorithm)


def AVERAGE_ToString():
    return "Moderately"


FuzzyQuantifier.PLUS = createQuantifier(2, "Very")
"""
@type {string}
@default "Very"
"""

FuzzyQuantifier.DOUBLE_PLUS = createQuantifier(3, "Extremely")
"""
@type {string}
@default "Extremely"
"""


def IS(v, algorithm, inverse):
    """
    This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
    @type {string}
    @default "Completely"
    :param v:
    :param algorithm:
    :param inverse:
    :return:
    """
    if v is None:
        return 1
    q = 1 if inverse else 0
    return FuzzyVeracity(q, algorithm)


def IS_ToString():
    return "Completely"


def MORE(v, algorithm, inverse):
    """
    This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
    @type {string}
    @default "More"
    :param v:
    :param algorithm:
    :param inverse:
    :return:
    """
    if v is None:
        return 1
    q = 1 if inverse else 0
    return FuzzyVeracity(q, algorithm)


def MORE_ToString():
    return "More"
