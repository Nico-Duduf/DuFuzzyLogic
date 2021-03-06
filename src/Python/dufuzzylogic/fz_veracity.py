from .fz_logicalgorithm import FuzzyLogicAlgorithm

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

    def __init__(self, veracity, algorithm=FuzzyLogicAlgorithm.LINEAR):
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
        The equivalent of the boolean operation <code>this and other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity
        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            veracity = min(x, y)
        else:
            veracity = x * y

        return FuzzyVeracity(veracity, self.algorithm)

    def OR(self, other):
        """
        The equivalent of the boolean operation <code>this or other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity
        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            veracity = max(x, y)
        else:
            veracity = x + y - x * y

        return FuzzyVeracity(veracity, self.algorithm)

    def XOR(self, other):
        """
        The equivalent of the boolean operation <code>this != other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity
        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            veracity = x + y - 2 * min(x, y)
        else:
            veracity = x + y - 2 * x * y

        return FuzzyVeracity(veracity, self.algorithm)

    def IS_NOT(self, other):
        """
        The equivalent of the boolean operation <code>this != other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        self.XOR(other)

    def DIFFERENT(self, other):
        """
        The equivalent of the boolean operation <code>this != other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        self.XOR(other)

    def NXR(self, other):
        """
        The equivalent of the boolean operation <code>this == other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity

        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            veracity = 1 - x - y + 2 * min(x, y)
        else:
            veracity = 1 - x - y + 2 * x * y

        return FuzzyVeracity(veracity, self.algorithm)

    def IS(self, other):
        """
        The equivalent of the boolean operation <code>this == other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        self.NXR(other)

    def EQUALS(self, other):
        """
        The equivalent of the boolean operation <code>this == other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        self.NXR(other)

    def IMPLIES(self, other):
        """
        The equivalent of the boolean operation <code>!(this and other)</code> or <code>!this or other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity

        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            veracity = 1 - min(x, 1 - y)
        else:
            veracity = 1 - x + x * y

        return FuzzyVeracity(veracity, self.algorithm)

    def WITH(self, other):
        """
        The equivalent of the boolean operation <code>!(this and other)</code> or <code>!this or other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        self.IMPLIES(other)

    def HAS(self, other):
        """
        The equivalent of the boolean operation <code>!(this and other)</code> or <code>!this or other</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        self.IMPLIES(other)

    def DOES_NOT_IMPLY(self, other):
        """
        The equivalent of the boolean operation <code>this and !other</code> or <code>!(this or other)</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity

        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            veracity = min(x, 1 - y)
        else:
            veracity = x * (1 - y)

        return FuzzyVeracity(veracity)

    def WITHOUT(self, other):
        """
        The equivalent of the boolean operation <code>this and !other</code> or <code>!(this or other)</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        self.DOES_NOT_IMPLY(other)

    def DOES_NOT_HAVE(self, other):
        """
        The equivalent of the boolean operation <code>this and !other</code> or <code>!(this or other)</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        self.DOES_NOT_IMPLY(other)

    def AND_NOT(self, other):
        """
        The equivalent of the boolean operation <code>this and !other</code> or <code>!(this or other)</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        self.DOES_NOT_IMPLY(other)

    def NAND(self, other):
        """
        The equivalent of the boolean operation <code>!(this and other)</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity

        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            veracity = 1 - min(x, y)
        else:
            veracity = 1 - x * y

        return FuzzyVeracity(veracity)

    def NOT_BOTH(self, other):
        """
        The equivalent of the boolean operation <code>!(this and other)</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        self.NAND(other)

    def NOR(self, other):
        """
        The equivalent of the boolean operation <code>!(this or other)</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        x = self.veracity
        y = other.veracity

        if self.algorithm == FuzzyLogicAlgorithm.LINEAR:
            veracity = 1 - max(x, y)
        else:
            veracity = 1 - x - y + x * y

        return FuzzyVeracity(veracity)

    def NONE(self, other):
        """
        The equivalent of the boolean operation <code>!(this or other)</code>
        :param other: {FuzzyVeracity} The other operand.
        :return: {FuzzyVeracity}
        """
        self.NOR(other)

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

        veracity = (1 - weight * x + weight * y)

        return FuzzyVeracity(veracity)
