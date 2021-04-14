from DuFuzzyLogic.src.Python.dufuzzylogic import *

# ========= FUZZY VALUES =============
from DuFuzzyLogic.src.Python.dufuzzylogic import FuzzyVeracity

"""
* Do not use the constructor of this class, use {@link FuzzyLogic.newSet} to create a new set.<br >
 * @class
 * @classdesc FuzzyValue is a value to be used with Fuzzy Logic. It's inclusion in a set can be tested with {@link FuzzyValue.IS} or {@link FuzzyValue.IS_NOT},<br />
 * Use {@link FuzzyValue.SET} or {@link FuzzyLogic.THEN} to change this value using a {@link FuzzySet}
 * @example
 * var logic = new FuzzyLogic();
 * var comfortable = logic.newSet("Warm", 17, 20);
 * var temperature = logic.newValue( 18 );
 * // Test if this temperature is comfortable
 * logic.IF(
 *    temperature.IS_NOT(comfortable);
 * )
 * // Set it very comfortable
 * logic.THEN ( temperature.SET(comfortable, "Very"); )
 * @property {string} unit The unit to display when returning this value as a string.
 * @property {bool} reportEnabled Enables or disable report generation when crispifying. Disabled by default to improve performance.
 * @property {string[][]} report The report (explanation) of the latest crispification {@link FuzzyValue.crispify}.<br />
 * It is an Array containing Arrays of strings. Each sub-array is the report of one rule, which you can print with <code>.join(newLine)</code> for example.
 */
"""


class FuzzyValue:
    def __init__(self, value, unit, algorithm, crispAlgorithm):
        if value is None:
            value = 0
        if unit is None:
            unit = ""
        self.value = value
        self.unit = unit
        self.sets = []
        self.algorithm = algorithm
        self.crispAlgorithm = crispAlgorithm

        self.report = []
        self.reportEnabled = False
        self.numRules = 0

    def FValue_IS(self, FuzzySet, quantifier):
        """
        Tests the inclusion of the value in the set
        :param FuzzySet: {FuzzySet} The set which may include the value.
        :param quantifier: {FuzzyQuantifier|string} A quantifier.
        :return: {FuzzyVeracity} The veracity of the inclusion of the value in the set.
        """
        veracity = FuzzySet.FSet_contains(self, quantifier)
        return veracity

    def FValue_IS_NOT(self, FuzzySet, quantifier):
        """
        Tests the exclusion of the value in the set
        :param FuzzySet: {FuzzySet} The set which may (not) include the value.
        :param quantifier: {FuzzyQuantifier|string} A quantifier.
        :return: {FuzzyVeracity} The veracity of the exclusion of the value in the set.
        """
        x = FuzzySet.FSet_contains(self.value, quantifier)
        return x.FVeracity_NEGATE()

    def FValue_SET(self, FuzzySet, quantifier=None, veracity=None):
        """
        Changes the value according to a new veracity.
        :param FuzzySet: The set.
        :param quantifier: [quantifier=FuzzyQuantifier.NONE] The quantifier
        :param veracity: [quantifier=FuzzyQuantifier.NONE] The quantifier
        :return:
        """
        if quantifier is None:
            quantifier = FuzzyQuantifier.NONE
        if veracity is None:
            veracity = FuzzyVeracity(1, self.algorithm)

        self.numRules = self.numRules + 1
        veracity.ruleNum = self.numRules

        # Check if this set is already here
        for i in range(0, len(self.sets), 1):
            if FuzzySet.name == self.sets[i].name:
                self.sets[i].quantifiers.append(quantifier)
                self.sets[i].veracities.appends(veracity)
                return

        # Otherwise, add it
        FuzzySet.quantifiers = [quantifier]
        FuzzySet.veracities = [veracity]
        self.sets.append(FuzzySet)

    def FValue_crispify(self, clearSets=True, algorithm=None):
        """
        Computes a crisp value depending on the inclusions which have been set before using {@link FuzzyValue.SET}.
        :param clearSets: {bool} [clearSets=true] When crispifying, the sets added with {@link FuzzyValue.SET} are cleared, this means changes made before the call to crispify() will be lost in subsequent calls. Set this parameter to false to keep these previous changes.
        :param algorithm: {FuzzyCrispAlgorithm} [algorithm] Change the algorithm to use for crispification.
        :return: {Number} The crisp (i.e. standard) value.
        """
        if algorithm is None:
            algorithm = self.crispAlgorithm

        if len(self.sets) == 0:
            return self.value

        crisp = 0
        self.report = []

        def ruleSorter(a, b):
            return a.number - b.number

        # get all average values and veracities from the sets
        sumWeights = 0
        for i in self.sets:  # for singleSet in self.sets: ???
            singleSet = self.sets[i]
            for j in range(0, len(singleSet.veracities), 1):
                #  the veracity
                v = singleSet.veracities[j]
                q = singleSet.quantifiers[j]
                # the corresponding values
                vals = singleSet.crispify(q, v)

                val = None
                ver = None

                if algorithm == FuzzyCrispAlgorithm.CENTROID or algorithm == FuzzyCrispAlgorithm.MEAN:
                    val = mean(vals)
                elif algorithm == FuzzyCrispAlgorithm.CENTROID_LOWER or algorithm == FuzzyCrispAlgorithm.MEAN_LOWER:
                    val = vals[0]
                elif algorithm == FuzzyCrispAlgorithm.CENTROID_HIGHER or algorithm == FuzzyCrispAlgorithm.MEAN_HIGHER:
                    val = vals[len(vals - 1)]

                if algorithm == FuzzyCrispAlgorithm.CENTROID or algorithm == FuzzyCrispAlgorithm.CENTROID_LOWER or algorithm == FuzzyCrispAlgorithm.CENTROID_HIGHER:
                    crisp += val * v.veracity
                    ver = v.veracity
                elif algorithm == FuzzyCrispAlgorithm.MEAN or algorithm == FuzzyCrispAlgorithm.MEAN_LOWER or algorithm == FuzzyCrispAlgorithm.MEAN_HIGHER:
                    crisp += val
                    ver = 1

                sumWeights += ver

                # generate report
                if self.reportEnabled:
                    for iVals in range(0, len(vals), 1):
                        vals[iVals] = round(vals[iVals] * 1000) / 1000

                    reportRule = []
                    reportRule.append("Rule #" + v.ruleNum + ": Set " + str(singleSet) + " (" + str(q) + ")")
                    reportRule.append(
                        "Gives value: " + str(round(val * 1000) / 1000) + " from these values: [" + ",".join(
                            vals) + "]")
                    reportRule.append("with a veracity of : " + str(round(ver * 1000) / 1000))
                    reportRule.number = v.ruleNum
                    self.report.append(reportRule)

        if sumWeights != 0:
            crisp = crisp / sumWeights

        # sort the report
        if self.reportEnabled:
            self.report.sort()

        if clearSets:
            # freeze all
            self.value = crisp
            # reset sets
            self.sets = []

        return crisp

    def FValue_toNumber(self, clearSets, algorithm):
        """
        This is an alias for {@link FuzzyValue.prototype.crispify};     
        """
        return self.FValue_crispify(clearSets, algorithm)

    def FValue_toFloat(self, clearSets, algorithm):
        """
        This is an alias for {@link FuzzyValue.prototype.crispify};     
        """
        return self.FValue_crispify(clearSets, algorithm)

    def FValue_defuzzify(self, clearSets, algorithm):
        """
        This is an alias for {@link FuzzyValue.prototype.crispify};     
        """
        return self.FValue_crispify(clearSets, algorithm)

    def FValue_quantify(self, fuzzySet):
        """
        Returns the closest quantifier for this value in this set
        :param fuzzySet: {FuzzySet} The set
        :return: {FuzzyQuantifier} The quantifier
        """
        return fuzzySet.FSet_quantify(self)

    def FValue_toString(self, crispAlgorithm, fuzzySet):
        """
        Returns a string representation of the value with its unit (if any)
        :param crispAlgorithm: {FuzzyCrispAlgorithm} [crispAlgorithm] The algorithm to use for crispification before returning the string. Uses the algorithm set when creating the {@link FuzzyLogic} instance by default.
        :param fuzzySet: {FuzzySet} [set] A set to quantify the value
        :return: {string} The description of the value
        """
        v = self.FValue_crispify(False, crispAlgorithm)
        v = round(v * 100) / 100
        string = v + self.unit
        if fuzzySet is not None:
            string = str(string) + " is " + str(fuzzySet.quanfity(self)) + " " + str(fuzzySet)
        return string
