from FzMath import *
from Namespace import *
from FuzzyValue import *
from FuzzyLogic import *
from FuzzyVeracity import *
from FuzzyQuantifier import *

FuzzyQuantifier = {}

# =========== FUZZY SETS ============

class FuzzySet:
    def __init__(self, name, valueNot, valueIS, shape, shapeAbove, plateauMin, plateauMax, algorithm):
        """"
        Do not use the constructor of this class, use {@link FuzzyLogic.newSet} to create a new set.
        Most of the time you won't need to access the properties nor use the methods of this class, but use the methods of {@link FuzzyLogic}, {@link FuzzyValue}, {@link FuzzyVeracity}
        @class
        @classdesc A Fuzzy set.
        :param name: {string} The name of this set
        :param valueNot: {Number} One of the closest value which is not in the set (either above or below).
        :param valueIS: {Number} The value which best fits in the set, the most extreme/maximum in the set.
        :param shape: {FuzzyShape} The shape (i.e. interpolation or transition) when getting in (below) the set.
        :param shapeAbove: {FuzzyShape} The shape (i.e. interpolation or transition) when getting out (above) of the set.
        :param plateauMin: {Number} The value above which a value is considered completely included.
        :param plateauMax: {Number} The value under which a value is considered completely included.
        :param algorithm:
        :return:
        """
        if valueNot > valueIS:
            max = valueNot
            min = valueNot - (valueNot - valueIS) * 2
        else:
            min = valueNot
            max = valueNot + (valueIS - valueNot) * 2

        shape = shape or FuzzyShape.LINEAR
        shapeAbove = shapeAbove or shape
        plateauMin = plateauMin or mean([min, max])
        plateauMax = plateauMax or mean([min, max])

        self.name = name
        self.min = min
        self.max = max
        self.shapeIn = shape
        self.shapeOut = shapeAbove
        self.plateauMin = plateauMin
        self.plateauMax = plateauMax
        self.algorithm = algorithm

    def contains(self, v, quantifier):  # ligne 199
        """
        Checks if a value is contained in the set.
        :param v: {Number|FuzzyValue} The value to test.
        :param quantifier: {FuzzyQuantifier|Number} [quantifier=FuzzyQuantifier.NONE] Checks in which part of the set the value is in.
        :return: {FuzzyVeracity} The veracity.
        """
        if isinstance(v, FuzzyValue):
            value = v.crispify(False)
        else:
            value = v

        quantifier = getQuantifier(quantifier)

        if value >= self.plateauMin & value <= self.plateauMax:
            return quantifier.quantify(1, self.algorithm)
        elif value < self.plateauMin:
            if self.shapeIn == FuzzyShape.CONSTANT:
                return quantifier(1, self.algorithm)
            elif self.shapeIn == FuzzyShape.SQUARE:
                min = mean(self.plateauMin, self.min)       # 2 arguments au lieu d'un seul !?
                if value >= min:
                    return quantifier(1, self.algorithm)
                else:
                    return quantifier(0, self.algorithm)
            elif self.shapeIn == FuzzyShape.LINEAR:
                if value < self.min:
                    return quantifier(0, self.algorithm)
                else:
                    return quantifier((value-self.min)/(self.plateauMin-self.min), self.algorithm)
            elif self.shapeIn == FuzzyShape.SIGMOID:
                mid = (self.plateauMin + self.min) / 2
                rate = 6 / (self.plateauMin - self.min)
                return quantifier(logistic(value, mid, 0, 1, rate), self.algorithm)
            elif self.shapeIn == FuzzyShape.GAUSSIAN:
                width = self.plateauMin - self.min
                return quantifier(gaussian(value, 0, 1, self.plateauMin, width), self.algorithm)
            elif self.shapeIn == FuzzyShape.REVERSED_GAUSSIAN:
                width = self.plateauMin - self.min
                return quantifier(reversedGaussian(value, 0, 1, self.plateauMin, width), self.algorithm)
            else:
                return quantifier(0, self.algorithm)
        else:
            if self.shapeOut == FuzzyShape.CONSTANT:
                return quantifier(1, self.algorithm)
            elif self.shapeOut == FuzzyShape.SQUARE:
                max = mean(self.plateauMax, self.max)       # 2 arguments au lieu d'un seul !?
                if value <= max:
                    return quantifier(1, self.algorithm)
                else:
                    return quantifier(0, self.algorithm)
            elif self.shapeOut == FuzzyShape.LINEAR:
                if value > self.max:
                    return quantifier(0, self.algorithm)
                else:
                    return quantifier(1 - ((value-self.plateauMax)/(self.max-self.plateauMax)), self.algorithm)
            elif self.shapeOut == FuzzyShape.SIGMOID:
                mid = (self.plateauMax + self.max) / 2
                rate = 6 / (self.max - self.plateauMax)
                return quantifier(1 - logistic(value, mid, 0, 1, rate), self.algorithm)
            elif self.shapeOut == FuzzyShape.GAUSSIAN:
                width = self.max - self.plateauMax
                return quantifier(gaussian(value, 0, 1, self.plateauMax, width), self.algorithm)
            elif self.shapeOut == FuzzyShape.REVERSED_GAUSSIAN:     # sur le fichier js : FuzzyShape.GAUSSIAN
                width = self.max - self.plateauMax
                return quantifier(reversedGaussian(value, 0, 1, self.plateauMax, width), self.algorithm)
            else:
                return quantifier(0, self.algorithm)

    def getValues(self, veracity):
        """
        Gets a list of precise values from the set corresponding to the given veracity.
        :param veracity: {FuzzyVeracity|Number} [veracity=0.5] The veracity
        :return: {Number[]} The list of possible crisp values, ordered from min to max.
        """
        global range
        veracity = veracity or 0.5
        if isinstance(veracity, FuzzyVeracity):
            veracity = veracity.veracity

        defaultValue = mean([self.plateauMin, self.plateauMax])

        if self.shapeIn == FuzzyShape.CONSTANT & self.shapeOut == FuzzyShape.CONSTANT:
            return [self.min, self.plateauMin, defaultValue, self.plateauMax, self.max]

        crisp = []

        if veracity >= 1:
            crisp = [self.plateauMin, defaultValue, self.plateauMax]

        # below

        if self.shapeIn == FuzzyShape.CONSTANT & veracity == 1:
            crisp.append(self.min)
        elif self.shapeIn == FuzzyShape.SQUARE:
            if veracity >= 0.5:
                crisp.append(self.plateauMin)
            else:
                crisp.append(self.min)
        elif self.shapeIn == FuzzyShape.LINEAR:
            range = self.plateauMin - self.min
            crisp.append(self.min + range * veracity)
        elif self.shapeIn == FuzzyShape.SIGMOID:
            mid = (self.plateauMin + self.min) / 2
            crisp.append(inverseLogistic(veracity, mid))  # seulement 2 arguments pour inverseLogistic !?
        elif self.shapeIn == FuzzyShape.GAUSSIAN:
            width = self.plateauMin - self.min
            g = inverseGaussian(veracity, 0, 1, self.plateauMin, width)
            crisp.append(g[0])
        elif self.shapeIn == FuzzyShape.REVERSED_GAUSSIAN:
            width = self.plateauMin - self.min
            g = inverseReversedGaussian(veracity, 0, 1, self.plateauMin, width)
            crisp.append(g[0])

        # above
        if self.shapeOut == FuzzyShape.CONSTANT & veracity == 1:
            crisp.append(self.max)
        elif self.shapeOut == FuzzyShape.SQUARE:
            if veracity >= 0.5:
                crisp.append(self.plateauMax)
            else:
                crisp.append(self.max)
        elif self.shapeOut == FuzzyShape.LINEAR:
            range = self.max - self.plateauMax
            crisp.append(self.max + 1 - (range * veracity))
        elif self.shapeOut == FuzzyShape.SIGMOID:
            mid = (self.plateauMax + self.max) / 2
            crisp.append(inverseLogistic(1 - veracity, mid, 0, 1)) # seulement 4 arguments pour inverseLogistic !?
        elif self.shapeOut == FuzzyShape.GAUSSIAN:
            width = self.max - self.plateauMax
            g = inverseGaussian(1 - veracity, 0, 1, self.plateauMax, width)
            crisp.append(g[1])
        elif self.shapeOut == FuzzyShape.REVERSED_GAUSSIAN:
            width = self.max - self.plateauMax
            g = inverseReversedGaussian(1 - veracity, 0, 1, self.plateauMax, width)
            crisp.append(g(1))

        # clamp
        for i in range(0, len(crisp)):
            if crisp[i] > self.max:
                crisp[i] = self.max
            if crisp[i] < self.min:
                crisp[i] = self.min

        return crisp.sort()

    def crispify(self, quantifier, veracity):
        """
        Gets a list of precise values from the set corresponding to the quantifier
        :param quantifier: {FuzzyModifier} [quantifier=FuzzyModifier.AVERAGE] The quantifier
        :param veracity: {FuzzyVeracity|Number} [veracity=0.5] The veracity
        :return: {Number[]} The list of possible crisp values, ordered from min to max.
        """
        quantifier = getQuantifier(quantifier)
        v = None
        if not veracity:
            v = quantifier
        elif isinstance(veracity, FuzzyVeracity):
            v = veracity.veracity
        else:
            v = veracity

        v = quantifier(v, self.algorithm, True).veracity
        return self.getValues(v)

    def quantify(self, value):
        """
        Gets the closest quantifier to this value
        :param value: {Number|FuzzyValue} The value to quantify
        :return: {FuzzyQuantifier} The quantifier
        """
        if not isinstance(value, FuzzyValue):
            value = FuzzyValue(value, "", self.algorithm)  # 3 arguments au lieu de 4!?
        val = value.crispify(False)

        if self.shapeIn == FuzzyShape.CONSTANT & self.shapeOut == FuzzyShape.CONSTANT:
            return FuzzyQuantifiers.IS
        if val < self.min & self.shapeIn == FuzzyShape.CONSTANT:
            return FuzzyQuantifiers.IS
        if val < self.min:
            return FuzzyQuantifiers.IS_NOT
        if val > self.max & self.shapeOut == FuzzyShape.CONSTANT:
            return FuzzyQuantifiers.IS
        if val > self.max:
            return FuzzyQuantifiers.IS_NOT
        if val >= self.plateauMin & val <= self.plateauMax:
            return FuzzyQuantifiers.IS

        quantifier = FuzzyQuantifier.NOT
        veracity = self.contains(val).veracity

        distance = 1
        for q in FuzzyQuantifiers.quantifiersList:
            test = math.fabs( q.quantify() - veracity)

            if test < distance:
                distance = test
                quantifier = q

        return quantifier

    def toString(self):
        """
        Gets the name of this set.
        :return: {string} The name of the set.
        """
        return self.name








