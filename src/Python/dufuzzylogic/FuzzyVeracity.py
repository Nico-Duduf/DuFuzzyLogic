from FzMath import *
from Namespace import *
from FuzzyValue import *
from FuzzyLogic import *
from FuzzyVeracity import *
from FuzzyQuantifier import *

# ========== FUZZY VERACITY ==========


class FuzzyVeracity:
    """
    @class
    @classdesc FuzzyVeracity is the fuzzy equivalent of a crisp boolean in boolean logic. It represents the result of logical operations (IS, AND, OR...).<br />
    Its value can vary in the range [0.0, 1.0], 0.0 being the equivalent of "false" and 1.0 of "true".<br />
    You can acces logic operators through instances of this class, which enable fluent syntax for rules (Except IS and IS_NOT which are members of {@link FuzzyValue}).<br />
    Operators are methods in upper case.
    @example
    var logic = new FuzzyLogic();
    var intense = logic.newSet("Intense", 0, 255);
    // An RGB color to test
    var color = [255,200,10];
    // Separate channels
    var redChannel = logic.newValue( color[0] );
    var greenChannel = logic.newValue( color[1] );
    var blueChannel = logic.newValue( color[2] );
    // isRed will be a FuzzyVeracity, the result of the test.
    // Note that FuzzyValue.IS returns a FuzzyVeracity, on which the methods AND and NOR are called.
    // But this is all internal and you don't really need to know that to use this syntax.
    var isRed = redChannel.IS( intense )
        .AND(
            greenChannel.IS( intense ).
            NOR( blueChannel.IS( intense ))
        )
    @property {Number} veracity The veracity level in the range [0.0, 1.0]
    """
    def __init__(self, veracity, algorithm = FuzzyLogicAlgorithm.LINEAR):
        self.veracity = veracity
        self.algorithm = algorithm

    def NEGATE(self):
        """
        Negates the current veracity. A new veracity is returned, and the current veracity is not changed.
        :return: {FuzzyVeracity} The negation of this veracity.
        """
        return FuzzyVeracity(1 - self.veracity, self.algorithm)

    def AND(self, other):
        """
        The equivalent of the boolean operation <code>this && other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity
        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            v = min(x, y)
        else:
            v = x * y

        return FuzzyVeracity(v, self.algorithm)

    def OR(self, other):
        """
        The equivalent of the boolean operation <code>this || other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity
        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            v = max(x, y)
        else:
            v = x + y - x*y

        return FuzzyVeracity(v, self.algorithm)

    def XOR(self, other):
        """
        The equivalent of the boolean operation <code>this != other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity
        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            v = x + y - 2 * min(x, y)
        else:
            v = x + y - 2 * x * y

        return FuzzyVeracity(v, self.algorithm)

    """The equivalent of the boolean operation <code>this != other</code>"""
    self.IS_NOT = self.XOR

    """The equivalent of the boolean operation <code>this != other</code>"""
    self.DIFFERENT = self.XOR

    def NXR(self, other):
        """
        The equivalent of the boolean operation <code>this == other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity

        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            v = 1 - x - y + 2 * min(x, y)
        else:
            v = 1 - x - y + 2 * x *y

        return FuzzyVeracity(v, self.algorithm)

    """The equivalent of the boolean operation <code>this == other</code>"""
    self.IS = self.NXR

    """The equivalent of the boolean operation <code>this == other</code>"""
    self.EQUALS = self.NXR

    def IMPLIES(self, other):
        """
        The equivalent of the boolean operation <code>!(this && other)</code> or <code>!this || other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity

        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            v = 1 - min(x, 1-y)
        else:
            v = 1-x + x * y

        return FuzzyVeracity(v, self.algorithm)

    """The equivalent of the boolean operation <code>!(this && other)</code> or <code>!this || other</code>"""
    FuzzyVeracity.WITH = self.IMPLIES

    """The equivalent of the boolean operation <code>!(this && other)</code> or <code>!this || other</code>"""
    FuzzyVeracity.HAS = self.IMPLIES

    def DOES_NOT_IMPLY(self, other):
        """
        The equivalent of the boolean operation <code>this && !other</code> or <code>!(this || other)</code>
        :param other: {FuzzyVeracity}  The other operand.
        :return:
        """
        x = self.veracity
        y = other.veracity

        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            v = min(x, 1-y)
        else:
            v = x * (1-y)

        return FuzzyVeracity(v)     # 1 seul argument

    """The equivalent of the boolean operation <code>this && !other</code> or <code>!(this || other)</code>"""
    FuzzyVeracity.WITHOUT = DOES_NOT_IMPLY()

    """The equivalent of the boolean operation <code>this && !other</code> or <code>!(this || other)</code>"""
    FuzzyVeracity.DOES_NOT_HAVE = DOES_NOT_IMPLY()

    """The equivalent of the boolean operation <code>this && !other</code> or <code>!(this || other)</code>"""
    FuzzyVeracity.AND_NOT = DOES_NOT_IMPLY()

    def NAND(self, other):
        """
        The equivalent of the boolean operation <code>!(this && other)</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity

        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            v = 1 - min(x, y)
        else:
            v = 1 - x * y

        return FuzzyVeracity(v)     # 1 seul argument

    """The equivalent of the boolean operation <code>!(this && other)</code>"""
    FuzzyVeracity.NOT_BOTH = NAND()

    def NOR(self, other):
        """
        The equivalent of the boolean operation <code>!(this || other)</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity

        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            v = 1 - max(x, y)
        else:
            v = 1 - x - y + x * y

        return FuzzyVeracity(v)     # 1 seul argument

    """The equivalent of the boolean operation <code>!(this || other)</code>"""
    FuzzyVeracity.NONE = NOR()

    def WEIGHTED(self, other, weight):
        """
        Weights this and other according to a given factor.
        The weight factor is applied to the other operand, and the <code>1 - weight</code> factor is applied to this.
        :param other: {FuzzyVeracity} The other operand.
        :param weight: {Number} The weight.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity

        v = (1 - weight * x + weight * y)       # ATTENTION, sur le fichier.js c'est w au lieu de weight !?

        return FuzzyVeracity(v)     # 1 seul argument
