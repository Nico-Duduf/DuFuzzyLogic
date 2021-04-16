from .fz_value import FuzzyValue
from .fz_quantifier import quantify
from .fz_veracity import FuzzyVeracity
from .fz_math import logistic, inverseLogistic, gaussian, reversedGaussian, inverseGaussian, inverseReversedGaussian, mean
from .fz_shape import FuzzyShape
from .fz_logicalgorithm import FuzzyLogicAlgorithm
from .fz_quantifier import FuzzyQuantifier
import math


# =========== FUZZY SETS ============

class FuzzySet:
    def __init__(self, name, valueNot, valueIS, shapeIn=FuzzyShape.LINEAR, shapeOut=None, plateauMin=None,
                 plateauMax=None, algorithm=FuzzyLogicAlgorithm):  # Vérifier si algo est bien FuzzyLogicAlgo !?
        """"
        Do not use the constructor of this class, use {@link FuzzyLogic.newSet} to create a new set.
        Most of the time you won't need to access the properties nor use the methods of this class, but use the methods of {@link FuzzyLogic}, {@link FuzzyValue}, {@link FuzzyVeracity}
        @class
        @classdesc A Fuzzy set.
        :param name: {string} The name of this set
        :param valueNot: {Number} One of the closest value which is not in the set (either above or below).
        :param valueIS: {Number} The value which best fits in the set, the most extreme/maximum in the set.
        :param shapeIn: {FuzzyShape} The shape (i.e. interpolation or transition) when getting in (below) the set.
        :param shapeOut: {FuzzyShape} The shape (i.e. interpolation or transition) when getting out (above) of the set.
        :param plateauMin: {Number} The value above which a value is considered completely included.
        :param plateauMax: {Number} The value under which a value is considered completely included.
        :param algorithm:
        :return:
        """
        if valueNot > valueIS:
            maximum = valueNot
            minimum = valueNot - (valueNot - valueIS) * 2
        else:
            minimum = valueNot
            maximum = valueNot + (valueIS - valueNot) * 2

        if shapeOut is None:
            self.shapeOut = shapeIn
        if plateauMin is None:
            plateauMin = mean([minimum, maximum])
        if plateauMax is None:
            plateauMax = mean([minimum, maximum])

        self.name = name
        self.minimum = minimum
        self.maximum = maximum
        self.shapeIn = shapeIn
        self.shapeOut = shapeOut
        self.plateauMin = plateauMin
        self.plateauMax = plateauMax
        self.algorithm = algorithm

    def FSet_contains(self, value, quantifier=FuzzyQuantifier.NONE):
        """
        Checks if a value is contained in the set.
        :param value: {Number|FuzzyValue} The value to test.
        :param quantifier: {FuzzyQuantifier|Number} [quantifier=FuzzyQuantifier.NONE] Checks in which part of the set the value is in.
        :return: {FuzzyVeracity} The veracity.
        """
        if isinstance(value, FuzzyValue):
            value = value.FValue_crispify(False)

        if value >= self.plateauMin and value <= self.plateauMax:
            return quantify(quantifier, 1, self.algorithm)

        elif value < self.plateauMin:
            if self.shapeIn == FuzzyShape.CONSTANT:
                return quantify(quantifier, 1, self.algorithm)

            elif self.shapeIn == FuzzyShape.SQUARE:
                minimum = mean((self.plateauMin, self.minimum))  # 2 arguments au lieu d'un seul => créé une liste
                if value >= minimum:
                    return quantify(quantifier, 1, self.algorithm)
                else:
                    return quantify(quantifier, 0, self.algorithm)

            elif self.shapeIn == FuzzyShape.LINEAR:
                if value < self.minimum:
                    return quantify(quantifier, 0, self.algorithm)
                else:
                    return quantify(quantifier, (value - self.minimum) / (self.plateauMin - self.minimum),
                                    self.algorithm)

            elif self.shapeIn == FuzzyShape.SIGMOID:
                mid = (self.plateauMin + self.minimum) / 2
                rate = 6 / (self.plateauMin - self.minimum)
                return quantify(quantifier, logistic(value, mid, 0, 1, rate), self.algorithm)

            elif self.shapeIn == FuzzyShape.GAUSSIAN:
                width = self.plateauMin - self.minimum
                return quantify(quantifier, gaussian(value, 0, 1, self.plateauMin, width), self.algorithm)

            elif self.shapeIn == FuzzyShape.REVERSED_GAUSSIAN:
                width = self.plateauMin - self.minimum
                return quantify(quantifier, reversedGaussian(value, 0, 1, self.plateauMin, width), self.algorithm)

            else:
                return quantify(quantifier, 0, self.algorithm)

        else:
            if self.shapeOut == FuzzyShape.CONSTANT:
                return quantify(quantifier, 1, self.algorithm)

            elif self.shapeOut == FuzzyShape.SQUARE:
                maximum = mean((self.plateauMax, self.maximum))  # 2 arguments au lieu d'un seul => créé une liste
                if value <= maximum:
                    return quantify(quantifier, 1, self.algorithm)
                else:
                    return quantify(quantifier, 0, self.algorithm)

            elif self.shapeOut == FuzzyShape.LINEAR:
                if value > self.maximum:
                    return quantify(quantifier, 0, self.algorithm)
                else:
                    return quantify(quantifier, 1 - ((value - self.plateauMax) / (self.maximum - self.plateauMax)),
                                    self.algorithm)

            elif self.shapeOut == FuzzyShape.SIGMOID:
                mid = (self.plateauMax + self.maximum) / 2
                rate = 6 / (self.maximum - self.plateauMax)
                return quantify(quantifier, 1 - logistic(value, mid, 0, 1, rate), self.algorithm)

            elif self.shapeOut == FuzzyShape.GAUSSIAN:
                width = self.maximum - self.plateauMax
                return quantify(quantifier, gaussian(value, 0, 1, self.plateauMax, width), self.algorithm)

            elif self.shapeOut == FuzzyShape.REVERSED_GAUSSIAN:
                width = self.maximum - self.plateauMax
                return quantify(quantifier, reversedGaussian(value, 0, 1, self.plateauMax, width), self.algorithm)

            else:
                return quantify(quantifier, 0, self.algorithm)

    def FSet_getValues(self, veracity):
        """
        Gets a list of precise values from the set corresponding to the given veracity.
        :param veracity: {FuzzyVeracity|Number} [veracity=0.5] The veracity
        :return: {Number[]} The list of possible crisp values, ordered from minimum to maximum.
        """
        veracity = veracity or 0.5
        if isinstance(veracity, FuzzyVeracity):
            veracity = veracity.veracity

        defaultValue = mean([self.plateauMin, self.plateauMax])

        if self.shapeIn == FuzzyShape.CONSTANT and self.shapeOut == FuzzyShape.CONSTANT:
            return [self.minimum, self.plateauMin, defaultValue, self.plateauMax, self.maximum]

        crisp = []

        if veracity >= 1:
            crisp = [self.plateauMin, defaultValue, self.plateauMax]

        # below

        if self.shapeIn == FuzzyShape.CONSTANT and veracity == 1:
            crisp.append(self.minimum)
        elif self.shapeIn == FuzzyShape.SQUARE:
            if veracity >= 0.5:
                crisp.append(self.plateauMin)
            else:
                crisp.append(self.minimum)
        elif self.shapeIn == FuzzyShape.LINEAR:
            Rang = self.plateauMin - self.minimum
            crisp.append(self.minimum + Rang * veracity)
        elif self.shapeIn == FuzzyShape.SIGMOID:
            mid = (self.plateauMin + self.minimum) / 2
            crisp.append(inverseLogistic(veracity, mid))  # seulement 2 arguments pour inverseLogistic !?
        elif self.shapeIn == FuzzyShape.GAUSSIAN:
            width = self.plateauMin - self.minimum
            g = inverseGaussian(veracity, 0, 1, self.plateauMin, width)
            crisp.append(g[0])
        elif self.shapeIn == FuzzyShape.REVERSED_GAUSSIAN:
            width = self.plateauMin - self.minimum
            g = inverseReversedGaussian(veracity, 0, 1, self.plateauMin, width)
            crisp.append(g[0])

        # above
        if self.shapeOut == FuzzyShape.CONSTANT and veracity == 1:
            crisp.append(self.maximum)
        elif self.shapeOut == FuzzyShape.SQUARE:
            if veracity >= 0.5:
                crisp.append(self.plateauMax)
            else:
                crisp.append(self.maximum)
        elif self.shapeOut == FuzzyShape.LINEAR:
            Rang = self.maximum - self.plateauMax
            crisp.append(self.maximum + 1 - (Rang * veracity))
        elif self.shapeOut == FuzzyShape.SIGMOID:
            mid = (self.plateauMax + self.maximum) / 2
            crisp.append(inverseLogistic(1 - veracity, mid, 0, 1))  # seulement 4 arguments pour inverseLogistic !?
        elif self.shapeOut == FuzzyShape.GAUSSIAN:
            width = self.maximum - self.plateauMax
            g = inverseGaussian(1 - veracity, 0, 1, self.plateauMax, width)
            crisp.append(g[1])
        elif self.shapeOut == FuzzyShape.REVERSED_GAUSSIAN:
            width = self.maximum - self.plateauMax
            g = inverseReversedGaussian(1 - veracity, 0, 1, self.plateauMax, width)
            crisp.append(g(1))

        # clamp
        for i in range(0, len(crisp)):
            if crisp[i] > self.maximum:
                crisp[i] = self.maximum
            if crisp[i] < self.minimum:
                crisp[i] = self.minimum

        return sorted(crisp)

    def FSet_crispify(self, quantifier=FuzzyQuantifier.AVERAGE, veracity=0.5):
        """
        Gets a list of precise values from the set corresponding to the quantifier
        :param quantifier: {FuzzyModifier} [quantifier=FuzzyModifier.AVERAGE] The quantifier
        :param veracity: {FuzzyVeracity|Number} [veracity=0.5] The veracity
        :return: {Number[]} The list of possible crisp values, ordered from minimum to maximum.
        """
        v = None
        if veracity is None:
            v = quantify(quantifier)
        elif isinstance(veracity, FuzzyVeracity):
            v = veracity.veracity
        else:
            v = veracity

        v = quantify(quantifier, v, self.algorithm, True).veracity
        return self.FSet_getValues(v)

    def FSet_quantify(self, value):
        """
        Gets the closest quantifier to this value
        :param value: {Number|FuzzyValue} The value to quantify
        :return: {FuzzyQuantifier} The quantifier
        """
        if not isinstance(value, FuzzyValue):
            value = FuzzyValue(value, "", self.algorithm)
        val = value.FValue_crispify(False)

        if self.shapeIn == FuzzyShape.CONSTANT and self.shapeOut == FuzzyShape.CONSTANT:
            return FuzzyQuantifier.IS
        if val < self.minimum and self.shapeIn == FuzzyShape.CONSTANT:
            return FuzzyQuantifier.IS
        if val < self.minimum:
            return FuzzyQuantifier.IS_NOT
        if val > self.maximum and self.shapeOut == FuzzyShape.CONSTANT:
            return FuzzyQuantifier.IS
        if val > self.maximum:
            return FuzzyQuantifier.IS_NOT
        if self.plateauMin <= val <= self.plateauMax:
            return FuzzyQuantifier.IS

        quantifier = FuzzyQuantifier.IS_NOT        # Attention, c'était FuzzyQuantifier.NOT en js !?
        veracity = self.FSet_contains(val).veracity

        distance = 1
        for i in FuzzyQuantifier.FuzzyQuantifierList:
            q = FuzzyQuantifier.FuzzyQuantifierList[i]
            test = math.fabs(quantify(q) - veracity)

            if test < distance:
                distance = test
                quantifier = q

        return quantifier

    def FSet_toString(self):
        """
        Gets the name of this set.
        :return: {string} The name of the set.
        """
        return self.name
