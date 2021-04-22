# -*- coding: utf-8 -*-

from dufuzzylogic import *

def runTest():
    print("--- FuzzyLogic ---\n \n")

    logic = FuzzyLogic(FuzzyLogicAlgorithm.HYPERBOLIC, FuzzyCrispAlgorithm.CENTROID)
    print("Algo: " + str(logic.algorithm))
    print("CrispAlgo: " + str(logic.crispAlgorithm))

    print("\n \n--- Basic Logic Test ---\n \n")
    comfortable = logic.newSet("Warm", 15, 20, FuzzyShape.LINEAR, FuzzyShape.LINEAR, None, None)
    cold = logic.newSet("Cold", 17, 0, FuzzyShape.CONSTANT, FuzzyShape.GAUSSIAN, None, None)
    hot = logic.newSet("Hot", 23, 35, FuzzyShape.GAUSSIAN, FuzzyShape.CONSTANT, None, None)

    temperatures = [-3, 0, 5, 10, 15, 17, 19, 21, 25, 30, 40]

    for i in range(0, len(temperatures)):
        temperature = logic.newValue(temperatures[i], "°C")

        print("\nTesting " + FuzzyValue.toString(temperature, None, None))

        logic.IF(temperature.IS_NOT(comfortable, None))
        print("Uncomfortable: " + str(logic.veracity.veracity))

        logic.IF(temperature.IS(comfortable, None))
        print("Comfortable: " + str(logic.veracity.veracity))

        logic.IF(temperature.IS(hot, "hot"))
        print("Hot: " + str(logic.veracity.veracity))

        logic.IF(temperature.IS(cold, "cold"))
        print("Cold: " + str(logic.veracity.veracity))

        print("\n===========================")

    print("\n \n--- Quantifiers Test ---\n")

    temperatures = [0, 14, 16, 18, 19, 20, 21, 23, 24, 25, 30, 40]
    quantifiers = [FuzzyQuantifier.IS_NOT,
                   FuzzyQuantifier.DOUBLE_MINUS,
                   FuzzyQuantifier.MINUS,
                   FuzzyQuantifier.AVERAGE,
                   FuzzyQuantifier.NONE,
                   FuzzyQuantifier.PLUS,
                   FuzzyQuantifier.DOUBLE_PLUS,
                   FuzzyQuantifier.IS]

    for i in range(0, len(temperatures)):
        temperature = logic.newValue(temperatures[i], "°C")

        print("\n===========================")
        print("\nTesting " + FuzzyValue.toString(temperature, None, None))

        for j in range(0, len(quantifiers)):
            quantifier = quantifiers[j]

            logic.IF(temperature.IS(comfortable, quantifier))

            print( quantifier + " comfortable: " + str(logic.veracity.veracity))

    print("\n===========================")
    print("\n \n--- Color Example ---\n \n")

    # Setup
    logic = FuzzyLogic(FuzzyLogicAlgorithm.HYPERBOLIC, FuzzyCrispAlgorithm.CENTROID)  # là ici, j'ai modifié : Si on mets None, None >>> Not Red

    # We don't need to worry about values above 255
    intense = logic.newSet("Intense", 0, 255)

    # The color to test
    color = [128, 200, 10]
    # A value to store the result
    redness = logic.newValue(None, None)

    # Separate channels
    redChannel = logic.newValue(color[0], None)
    greenChannel = logic.newValue(color[1], None)
    blueChannel = logic.newValue(color[2], None)

    logic.IF(redChannel.IS(intense, None).AND(
        greenChannel.IS(intense, None).NOR(blueChannel.IS(intense, None))))
    logic.THEN(redness, intense, None)

    # print the result
    print(str(color) + " is " + str(redness.quantify(intense) + " Red"))

    print("\n===========================")
    print("\n \n--- HVAC Example ---\n \n")

    logic = FuzzyLogic(FuzzyLogicAlgorithm.HYPERBOLIC)

    # Too wet is more than 70%, completely wet is 100%. Constant shape above 100%: it's still too wet!
    wet = logic.newSet("Wet", 60, 100, FuzzyShape.GAUSSIAN, FuzzyShape.CONSTANT)
    # The comfort zone begins at 40%, and its most comfortable at 60%. We use the same shape above and below this
    # comfort zone.
    comfortable = logic.newSet("Comfortable", 40, 55, FuzzyShape.SIGMOID)
    # Too dry is less than 50%, completely dry is 0%. Constant shape under 0%: it's still too dry!
    dry = logic.newSet("Dry", 50, 0, FuzzyShape.CONSTANT, FuzzyShape.GAUSSIAN)

    # Temperature
    # The principle is the same than humidity.
    hot = logic.newSet("Hot", 21, 35, FuzzyShape.GAUSSIAN, FuzzyShape.CONSTANT)
    warm = logic.newSet("Comfortably warm", 17, 20, FuzzyShape.GAUSSIAN)
    cold = logic.newSet("Cold", 17, 10, FuzzyShape.CONSTANT, FuzzyShape.GAUSSIAN)

    # Let's say a positive power (from 0% to 100%) heats the room, a negative one cools it.
    heat = logic.newSet("Heat", 0, 100, FuzzyShape.LINEAR, FuzzyShape.CONSTANT)
    refresh = logic.newSet("Refresh", 0, -100, FuzzyShape.CONSTANT, FuzzyShape.LINEAR)

    # Change these values to test the engine
    temperature = logic.newValue(22, "°C")
    humidity = logic.newValue(10, "%")

    hvacPower = logic.newValue(0, "%")
    # Enable reports to be able to have a look at the result of the logic
    hvacPower.reportEnabled = True

    # If it's hot, let's cool down
    logic.IF(temperature.IS(hot))
    logic.THEN(hvacPower, refresh, None)  # Rule #1

    # If it's cold, let's heat up
    logic.IF(temperature.IS(cold))
    logic.THEN(hvacPower, heat, None)  # Rule #2

    # If it's hot and wet, we want to refresh more
    logic.IF(temperature.IS(hot).AND(humidity.IS(wet)))
    logic.THEN(hvacPower, refresh, "More")  # Rule #3

    # If it's cold and wet, we want to heat more
    logic.IF(temperature.IS(cold).AND(humidity.IS(wet)))
    logic.THEN(hvacPower, heat, "More")  # Rule #4

    # If it's dry, we lower the power (because we don't want the hvac to make the air even drier)

    # If it's cold but not too cold and it is dry, we want to heat less to save energy
    logic.IF(
        temperature.IS(cold)
        .AND(temperature.IS_NOT(cold, "Extremely"))
        .AND(humidity.IS(dry)))
    logic.THEN(hvacPower, heat, "Less")  # Rule #5

    # If it's hot but not too hot, and it is dry, we want to refresh less to save energy
    logic.IF(temperature.IS(hot)
             .AND(temperature.IS_NOT(hot, "Extremely"))
             .AND(humidity.IS(dry)))
    logic.THEN(hvacPower, refresh, "Less")  # Rule #6

    logic.IF(temperature.IS(warm, "very")
             .OR(temperature.IS(cold))
             .AND(humidity.IS(wet)))
    logic.THEN(hvacPower, heat, "Somewhat")  # Rule #7

    logic.IF(temperature.IS(warm))
    logic.THEN(hvacPower, refresh, "not")  # Rule #9
    logic.THEN(hvacPower, heat, "not")  # Rule #9

    # print the result

    print(str(temperature.toString(None, hot)) + " and " + str(temperature.toString(None, cold)))
    print(str(humidity.toString(None, wet)) + " and " + str(humidity.toString(None, dry)))
    print("")
    print(str(temperature.toString(None, warm)))
    print(str(humidity.toString(None, comfortable)))
    print("")
    print("RESULT : the power of the air conditionner is " + str(hvacPower.toString(None, None)))
    print("")
    print("This is how this result is obtained: \n")

    for i in range(0, len(hvacPower.report)):
        print("")
        print( "\n".join(hvacPower.report[i]) )
        print("")

    # The default is CENTROID
    print("\nRESULT CENTROID: the power of the air conditionner is " + str(hvacPower.toString(None, None)))

    print("\nRESULT CENTROID_LOWER: the power of the air conditionner is " + str(
        hvacPower.toString(FuzzyCrispAlgorithm.CENTROID_LOWER, None)))

    print("\nRESULT CENTROID_HIGHER: the power of the air conditionner is " + str(
        hvacPower.toString(FuzzyCrispAlgorithm.CENTROID_HIGHER, None)))

    print("\nRESULT MEAN: the power of the air conditionner is " + str(hvacPower.toString(FuzzyCrispAlgorithm.MEAN, None)))

    print("\nRESULT MEAN_HIGHER: the power of the air conditionner is " + str(
        hvacPower.toString(FuzzyCrispAlgorithm.MEAN_HIGHER, None)))

    print("\nRESULT MEAN_LOWER: the power of the air conditionner is " + str(
        hvacPower.toString(FuzzyCrispAlgorithm.MEAN_LOWER, None)))


runTest()
