from DuFuzzyLogic.src.Python.dufuzzylogic import FuzzyLogic
from DuFuzzyLogic.src.Python.dufuzzylogic.FuzzyLogic import FuzzyLogic
from DuFuzzyLogic.src.Python.dufuzzylogic.FzQuantifier import quantify
from DuFuzzyLogic.src.Python.dufuzzylogic.Namespace import *

def runTest():
    print("--- FuzzyLogic ---\n \n")

    logic = FuzzyLogic(FuzzyLogicAlgorithm.HYPERBOLIC, FuzzyCrispAlgorithm.CENTROID)
    print("Algo: \n" + str(logic.algorithm))
    print("CrispAlgo: \n" + str(logic.crispAlgorithm))

    print("\n \n--- Basic Logic Test ---\n \n")
    comfortable = logic.newSet("Warm", 15, 20, None, None, None, None)
    cold = logic.newSet("Cold", 17, 0, FuzzyShape.CONSTANT, FuzzyShape.GAUSSIAN, None, None)
    hot = logic.newSet("Hot", 23, 35, FuzzyShape.GAUSSIAN, FuzzyShape.CONSTANT, None, None)

    temperatures = [-3, 0, 5, 10, 15, 17, 19, 21, 25, 30, 40]

    for i in temperatures:
        temperature = logic.newValue(temperatures[i], "°C")

        print("\nTesting " + str(temperature))

        logic.FLogic_IF(temperature.FValue_IS_NOT(comfortable, None))
        print("\n Uncomfortable: " + str(logic.veracity.veracity))

        logic.FLogic_IF(temperature.FValue_IS(comfortable))
        print("\ncomfortable: " + str(logic.veracity.veracity))

        logic.FLogic_IF(temperature.FValue_IS(hot))
        print("\nhot: " + str(logic.veracity.veracity))

        logic.FLogic_IF(temperature.FValue_IS(cold))
        print("\ncold: " + str(logic.veracity.veracity))

    print("\n \n--- Quantifiers Test ---\n \n")

    temperatures = [0, 14, 16, 18, 19, 20, 21, 23, 24, 25, 30, 40]
    quantifiers = [
        FuzzyQuantifier.IS_NOT,
        FuzzyQuantifier.DOUBLE_MINUS,
        FuzzyQuantifier.MINUS,
        FuzzyQuantifier.AVERAGE,
        FuzzyQuantifier.NONE,
        FuzzyQuantifier.PLUS,
        FuzzyQuantifier.DOUBLE_PLUS,
        FuzzyQuantifier.IS]

    for i in temperatures:
        temperature = logic.newValue(temperatures[i], "°C")

        print("\nTesting " + str(temperature))

        for j in quantifiers:
            quantifier = quantifiers[j]

            logic.FLogic_IF(temperature.FValue_IS(comfortable, quantifier))

            print("\n" + str(quantifier) + " comfortable: " + str(logic.veracity.veracity))

    print("\n \n--- Color Example ---\n \n")

    # Setup
    logic = FuzzyLogic

    # We don't need to worry about values above 255
    intense = logic.newSet("Intense", 0, 255)

    # The color to test
    color = [128, 200, 10]
    # A value to store the result
    redness = logic.newValue

    # Separate channels
    redChannel = logic.newValue(color[0])
    greenChannel = logic.newValue(color[1])
    blueChannel = logic.newValue(color[2])

    logic.FLogic_IF(redChannel.FValue_IS(intense).FValue_AND(greenChannel.FValue_IS(intense).FValue_NOR(blueChannel.FValue_IS(intense))))
    logic.FLogic_THEN(redness, intense)

    # print the result
    print("\n[" + str(color) + "] is " + str(quantify(redness, intense)) + " Red")

    print("\n \n--- HVAC Example ---\n \n")

runTest()