from .dufuzzylogic import *



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

        print("\nTesting " + FuzzyValue.FValue_toString(temperature, None, None))

        logic.FLogic_IF(temperature.FValue_IS_NOT(comfortable, None))
        print("Uncomfortable: " + str(logic.veracity.veracity))

        logic.FLogic_IF(temperature.FValue_IS(comfortable, None))
        print("Comfortable: " + str(logic.veracity.veracity))

        logic.FLogic_IF(temperature.FValue_IS(hot, "hot"))
        print("Hot: " + str(logic.veracity.veracity))

        logic.FLogic_IF(temperature.FValue_IS(cold, "cold"))
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
        print("\nTesting " + FuzzyValue.FValue_toString(temperature, None, None))

        for j in range(0, len(quantifiers)):
            quantifier = quantifiers[j]

            logic.FLogic_IF(temperature.FValue_IS(comfortable, quantifier))

            print(str(quantifier) + " comfortable: " + str(logic.veracity.veracity))

    print("\n===========================")
    print("\n \n--- Color Example ---\n \n")

    # Setup
    logic = FuzzyLogic(FuzzyLogicAlgorithm.HYPERBOLIC, FuzzyCrispAlgorithm.CENTROID)  # là ici, j'ai modifié

    # We don't need to worry about values above 255
    intense = logic.newSet("Intense", 0, 255)

    # The color to test
    color = [128, 200, 10]
    # A value to store the result
    redness = logic.newValue(None, None)  # A verifier...

    # Separate channels
    redChannel = logic.newValue(color[0], None)
    greenChannel = logic.newValue(color[1], None)
    blueChannel = logic.newValue(color[2], None)

    # logic.FLogic_IF(redChannel.FValue_IS(intense, None).FValue_AND(
    #     greenChannel.FValue_IS(intense).FValue_NOR(blueChannel.FValue_IS(intense))))
    # logic.FLogic_THEN(redness, intense)

    logic.FLogic_IF(redChannel.FValue_IS(intense, None).FVeracity_AND(
        greenChannel.FValue_IS(intense, None).FVeracity_NOR(blueChannel.FValue_IS(intense, None))))
    logic.FLogic_THEN(redness, intense, None)

    # print the result
    print(str(color) + " is " + str(redness.FValue_quantify(intense) + " Red"))

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
    logic.FLogic_IF(temperature.FValue_IS(hot, None))
    logic.FLogic_THEN(hvacPower, refresh, None)  # Rule #1

    # If it's cold, let's heat up
    logic.FLogic_IF(temperature.FValue_IS(cold, None))
    logic.FLogic_THEN(hvacPower, heat, None)  # Rule #2

    # If it's hot and wet, we want to refresh more
    logic.FLogic_IF(temperature.FValue_IS(hot, None).FVeracity_AND(humidity.FValue_IS(wet, None)))
    logic.FLogic_THEN(hvacPower, refresh, "More")  # Rule #3

    # If it's cold and wet, we want to heat more
    logic.FLogic_IF(temperature.FValue_IS(cold, None).FVeracity_AND(humidity.FValue_IS(wet, None)))
    logic.FLogic_THEN(hvacPower, heat, "More")  # Rule #4

    # If it's dry, we lower the power (because we don't want the hvac to make the air even drier)

    # If it's cold but not too cold and it is dry, we want to heat less to save energy
    logic.FLogic_IF(temperature.FValue_IS(cold, None)
                    .FVeracity_AND(temperature.FValue_IS_NOT(cold, "Extremly"))
                    .FVeracity_AND(humidity.FValue_IS(dry, None)))
    logic.FLogic_THEN(hvacPower, heat, "Less")  # Rule #5

    # If it's hot but not too hot, and it is dry, we want to refresh less to save energy
    logic.FLogic_IF(temperature.FValue_IS(hot, None)
                    .FVeracity_AND(temperature.FValue_IS_NOT(hot, "Extremly"))
                    .FVeracity_AND(humidity.FValue_IS(dry, None)))
    logic.FLogic_THEN(hvacPower, refresh, "Less")  # Rule #6

    logic.FLogic_IF(temperature.FValue_IS(warm, "very")
                    .FVeracity_OR(temperature.FValue_IS(cold, None))
                    .FVeracity_AND(humidity.FValue_IS(wet, None)))
    logic.FLogic_THEN(hvacPower, heat, "Somewhat")  # Rule #7

    logic.FLogic_IF(temperature.FValue_IS(warm, None))
    logic.FLogic_THEN(hvacPower, heat, "not")  # Rule #8
    logic.FLogic_THEN(hvacPower, refresh, "not")  # Rule #9

    # print the result

    print(str(temperature.FValue_toString(None, hot)) + " and " + str(temperature.FValue_toString(None, cold)))
    print(str(humidity.FValue_toString(None, wet)) + " and " + str(humidity.FValue_toString(None, dry)))
    print("")
    print(str(temperature.FValue_toString(None, warm)))
    print(str(humidity.FValue_toString(None, comfortable)))
    print("")
    print("RESULT : the power of the air conditionner is " + str(hvacPower.FValue_toString(None, None)))
    print("")
    print("This is how this result is obtained: \n")

    for i in range(0, len(hvacPower.report)):
        print("")
        print(str("\n").join(hvacPower.report[i]))
        print("")

    # The default is CENTROID
    print("\nRESULT CENTROID: the power of the air conditionner is " + str(hvacPower.FValue_toString(None, None)))

    print("\nRESULT CENTROID_LOWER: the power of the air conditionner is " + str(
        hvacPower.FValue_toString(FuzzyCrispAlgorithm.CENTROID_LOWER, None)))

    print("\nRESULT CENTROID_HIGHER: the power of the air conditionner is " + str(
        hvacPower.FValue_toString(FuzzyCrispAlgorithm.CENTROID_HIGHER, None)))

    print("\nRESULT MEAN: the power of the air conditionner is " + str(hvacPower.FValue_toString(FuzzyCrispAlgorithm.MEAN, None)))

    print("\nRESULT MEAN_HIGHER: the power of the air conditionner is " + str(
        hvacPower.FValue_toString(FuzzyCrispAlgorithm.MEAN_HIGHER, None)))

    print("\nRESULT MEAN_LOWER: the power of the air conditionner is " + str(
        hvacPower.FValue_toString(FuzzyCrispAlgorithm.MEAN_LOWER, None)))


runTest()
