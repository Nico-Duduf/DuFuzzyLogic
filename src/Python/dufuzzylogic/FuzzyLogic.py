from FuzzyVeracity import *
from FzMath import *
from Namespace import *
from FuzzyValue import *
from FuzzyQuantifier import *
from FuzzySets import *

class FuzzyLogic:

    def __init__(self, algorithm, crispAlgorithm):
        """
        Creates a new Fuzzy Logic Engine.
        @class
        @classdesc The Fuzzy Logic engine
        @author Nicolas Dufresne
        @copyright 2020 Nicolas Dufresne and contributors
        @version 1.0.0
        @license GPL-3.0
        :param algorithm: {FuzzyLogicAlgorithm} [algorithm=FuzzyLogicAlgorithm.LINEAR] The algorithm to use for logic operations
        :param crispAlgorithm: {FuzzyCrispAlgorithm} [crispAlgorithm=FuzzyCrispAlgorithm.CENTROID] The algorithm to use for crispification
        """
        algorithm = algorithm or FuzzyLogicAlgorithm.LINEAR
        crispAlgorithm = crispAlgorithm or FuzzyCrispAlgorithm.CENTROID

        self.algorithm = algorithm
        self.veracity = FuzzyVeracity(0)
        self.crispAlgorithm = crispAlgorithm

    def newValue(self, value, unit):
        """
        Creates a new {@link FuzzyValue}
        :param value: {Number} The initial crisp value.
        :param unit: {string} The unit to display when returning this value as a string.
        :return: {FuzzyValue} The value.
        """
        return FuzzyValue(value, unit, self.algorithm, self.crispAlgorithm)

    def newVeracity(self, veracity):
        """
        Creates a new {@link FuzzyVeracity}
        :param veracity: {Number} The initial veracity, in the range [0.0, 1.0].
        :return: {FuzzyVeracity} The veracity.
        """
        return FuzzyVeracity(veracity, self.algorithm)

    def newSet(self, name, extremeValue, referenceValue, shape, shapeAbove, plateauMin, plateauMax):
        """
        Creates a new {@link FuzzySet}.
        @example
        var logic = new FuzzyLogic();
        // Temperatures between 15 and 25 will be considered comfortable, 20 being the most comfortable
        var comfortabble = logic.newSet("Warm", 15, 20);
        // Temperatures under 17 are cold, and temperatures under 0 are the most cold (because of the constant shape below)
        var cold = logic.newSet("Cold", 17, 0, FuzzyShape.CONSTANT);
        // Temperatures above 23 are hot, and all temperatures above 35 are the most hot (because of the constant shape above)
        var hot = logic.newSet("Hot", 23, 35, FuzzyShape.GAUSSIAN, FuzzyShape.CONSTANT);
        :param name: {string} The unique name of this set (e.g. "hot", "fast", "red", "flower addict"...). <strong>It must be unique!</strong>
        :param extremeValue: property {Number} valueNOT One of the closest value which is not in the set (either above or below).
        :param referenceValue: {Number} valueIS The value which best fits in the set, the most extreme/maximum in the set.
        :param shape: {FuzzyShape} [shapeBelow=FuzzyShape.LINEAR] The shape (i.e. interpolation or transition) when getting in the set.
        :param shapeAbove: {FuzzyShape} [shapeAbove=shape] The shape (i.e. interpolation or transition) when getting out of the set. By default, same as shape.
        :param plateauMin: {Number} The value above which it is considered completely included. By default, it is at the middle between min and max.
        :param plateauMax: {Number} The value under which it is considered completely included. By default, it is at the middle between min and max.
        :return: {FuzzySet} The set.
        """
        return FuzzySet(name, extremeValue, referenceValue, shape, shapeAbove, plateauMin, plateauMax, self.algorithm)

    def IF(self, veracity):
        """
        This function internally stores the veracity to be used with {@link FuzzyLogic.THEN}.
         @example
         var logic = new FuzzyLogic();
         var comfortable = logic.newSet("Warm", 17, 20);
         var temperature = logic.newValue( 18 );
         // Test if this temperature is comfortable
         logic.IF(
            temperature.IS_NOT(comfortable);
         )
         // Set it very comfortable
         logic.THEN ( temperature.SET(comfortable, "Very"); )
        :param veracity: {FuzzyVeracity} The veracity of the statement.
        :return: {FuzzyVeracity} The value passed as argument.
        """
        self.veracity = veracity
        return veracity

    def THEN(self, value, fuzzySet, quantifier):
        """
        This function sets a value in a new set, using the veracity resulting from the previous call to {@link FuzzyLogic.IS}.<br /|
         It can be called several times after any call to IF.
         @example
         var logic = new FuzzyLogic();
         var comfortable = logic.newSet("Warm", 17, 20);
         var power = logic.newSet("Fan power", 0, 100);
         var temperature = logic.newValue( 18 );
         var fanPower = logic.newValue();
         // Test if this temperature is comfortable
         logic.IF(
            temperature.IS_NOT(comfortable);
         )
         // Set it very comfortable
         logic.THEN ( temperature.SET(comfortable, "Very"); )
         // and turn on the fan
         logic.THEN ( fanPower.SET( power ); )
        :param value: {FuzzyValue} The value to set.
        :param set: {FuzzySet} The set the value has to be included in.
        :param quantifier: {FuzzyQuantifier} A quantifier to apply for setting the value.
        :return:
        """
        value.SET(fuzzySet, quantifier, self.veracity)