function print(text) { document.write(text + "<br />"); }
function startP() { document.write("<p>"); }
function endP() { document.write("</p>"); }

function runTests() {

    startP();
    print("--- FuzzyLogic ---")

    var logic = new FuzzyLogic( FuzzyLogicAlgorithm.HYPERBOLIC, FuzzyCrispAlgorithm.CENTROID )
    print('Algo: ' + logic.algorithm);
    print('crispAlgo: ' + logic.crispAlgorithm);

    endP();
    
    startP();
    print("--- Basic Logic Test ---")

    var comfortable = logic.newSet("Warm", 15, 20);
    var cold = logic.newSet("Cold", 17, 0, FuzzyShape.CONSTANT, FuzzyShape.GAUSSIAN);
    var hot = logic.newSet("Hot", 23, 35, FuzzyShape.GAUSSIAN, FuzzyShape.CONSTANT);

    var temperatures = [ -3, 0, 5, 10, 15, 17, 19, 21, 25, 30, 40];

    for (var i = 0, n = temperatures.length; i < n; i++)
    {
        var temperature = logic.newValue(temperatures[i], "°C");

        startP();
        print('Testing ' + temperature.toString() );

        logic.IF(
           temperature.IS_NOT(comfortable)
        )
        print('uncomfortable: ' + logic.veracity.veracity );
    
        logic.IF(
           temperature.IS(comfortable)
        )
        print('comfortable: ' + logic.veracity.veracity );
    
        logic.IF(
           temperature.IS(hot)
        )
        print('hot: ' + logic.veracity.veracity );
    
        logic.IF(
           temperature.IS(cold)
        )
        print('cold: ' + logic.veracity.veracity );

        endP();
    }

    print("--- Quantifiers Test ---")

    temperatures = [ 0, 14, 16, 18, 19, 20, 21, 23, 24, 25, 30, 40];
    quantifiers = [
        FuzzyQuantifier.IS_NOT,
        FuzzyQuantifier.DOUBLE_MINUS,
        FuzzyQuantifier.MINUS,
        FuzzyQuantifier.AVERAGE,
        FuzzyQuantifier.NONE,
        FuzzyQuantifier.PLUS,
        FuzzyQuantifier.DOUBLE_PLUS,
        FuzzyQuantifier.IS
    ]

    for (var i = 0, n = temperatures.length; i < n; i++)
    {
        var temperature = logic.newValue(temperatures[i], "°C");

        startP();
        print('Testing ' + temperature.toString() );
        
        for (var j = 0, nj = quantifiers.length; j < nj; j++)
        {
            var quantifier = quantifiers[j];
    
            logic.IF(
                temperature.IS(comfortable, quantifier)
            )
            print(quantifier + ' comfortable: ' + logic.veracity.veracity );

        }

        endP();
    }

    print("--- Color Example ---");
    startP();

    // Setup
    var logic = new FuzzyLogic();

    // We don't need to worry about values above 255
    var intense = logic.newSet("Intense", 0, 255);

    // The color to test
    var color = [128,200,10];
    // A value to store the result
    var redness = logic.newValue();

    // Separate channels
    var redChannel = logic.newValue( color[0] );
    var greenChannel = logic.newValue( color[1] );
    var blueChannel = logic.newValue( color[2] );

    logic.IF(
        redChannel.IS( intense )
        .AND(
            greenChannel.IS( intense ).
            NOR( blueChannel.IS( intense ))
        )
    )
    logic.THEN( redness, intense );

    // print the result
    print("[" + color.toString() + "] is " + redness.quantify( intense ).toString() + " Red");
    endP();

    print("--- HVAC Example ---");
    startP();

    var logic = new FuzzyLogic( FuzzyLogicAlgorithm.HYPERBOLIC );

    // Too wet is more than 70%, completely wet is 100%. Constant shape above 100%: it's still too wet!
    var wet = logic.newSet("Wet", 60, 100, FuzzyShape.GAUSSIAN, FuzzyShape.CONSTANT);
    // The comfort zone begins at 40%, and its most comfortable at 60%. We use the same shape above and below this comfort zone.
    var comfortable = logic.newSet("Comfortable", 40, 55, FuzzyShape.SIGMOID);
    // Too dry is less than 50%, completely dry is 0%. Constant shape under 0%: it's still too dry!
    var dry = logic.newSet("Dry", 50, 0, FuzzyShape.CONSTANT, FuzzyShape.GAUSSIAN);

    // Temperature
    // The principle is the same than humidity.
    var hot = logic.newSet("Hot", 21, 35, FuzzyShape.GAUSSIAN, FuzzyShape.CONSTANT);
    var warm = logic.newSet("Comfortably warm", 17, 20, FuzzyShape.GAUSSIAN);
    var cold = logic.newSet("Cold", 17, 10, FuzzyShape.CONSTANT, FuzzyShape.GAUSSIAN);

    // Let's say a positive power (from 0% to 100%) heats the room, a negative one cools it.
    var heat = logic.newSet("Heat", 0, 100, FuzzyShape.LINEAR, FuzzyShape.CONSTANT);
    var refresh = logic.newSet("Refresh", 0, -100, FuzzyShape.CONSTANT, FuzzyShape.LINEAR);

    // Change these values to test the engine
    var temperature = logic.newValue( 22, "°C" );
    var humidity = logic.newValue( 10 , "%" );

    var hvacPower = logic.newValue( 0, "%" );
    // Enable reports to be able to have a look at the result of the logic
    hvacPower.reportEnabled = true;

    // If it's hot, let's cool down
    logic.IF( temperature.IS( hot ) ); 
    logic.THEN( hvacPower, refresh  ); // Rule #1

    // If it's cold, let's heat up
    logic.IF( temperature.IS( cold ) ); 
    logic.THEN( hvacPower, heat ); // Rule #2

    // If it's hot and wet, we want to refresh more
    logic.IF(
        temperature.IS( hot)
        .AND ( humidity.IS( wet ) )
    );
    logic.THEN( hvacPower, refresh, "More" ); // Rule #3

    // If it's cold and wet, we want to heat more
    logic.IF( 
        temperature.IS(cold)
        .AND ( humidity.IS( wet ) )
    );
    logic.THEN( hvacPower, heat, "More" ); // Rule #4

    //If it's dry, we lower the power (because we don't want the hvac to make the air even drier)

    // If it's cold but not too cold and it is dry, we want to heat less to save energy
    logic.IF( 
        temperature.IS(cold)
        .AND ( temperature.IS_NOT( cold, "Extremely") )
        .AND ( humidity.IS( dry ) )
    );
    logic.THEN( hvacPower, heat, "Less" ); // Rule #5

    // If it's hot but not too hot, and it is dry, we want to refresh less to save energy
    logic.IF( 
        temperature.IS( hot )
        .AND ( temperature.IS_NOT( hot, "Extremely") )
        .AND ( humidity.IS( dry ) )
    );
    logic.THEN( hvacPower, refresh, "Less" ); // Rule #6

    logic.IF(
        temperature.IS( warm, "very" )
        .OR ( temperature.IS(cold) )
        .AND ( humidity.IS( wet ) )
    )
    logic.THEN( hvacPower, heat, "Somewhat" ); // Rule #7

    logic.IF( temperature.IS( warm ) );
    logic.THEN( hvacPower, heat, "not"); // Rule #9
    logic.THEN( hvacPower, refresh, "not"); // Rule #9

    // print the result
    print( temperature.toString( hot ) + " and " + temperature.toString( cold ) );
    print( humidity.toString(wet) + " and " + humidity.toString( dry )  );
    print( "" );
    print( temperature.toString( warm ) );
    print( humidity.toString( comfortable ) );
    print( "" );
    print( "RESULT: the power of the air conditionner is " + hvacPower.toString()  );
    print( "" );
    print( "This is how this result is obtained:")
    for (var i = 0, num = hvacPower.report.length; i < num; i++)
    {
        print( "" );
        print( hvacPower.report[i].join("<br />") );
    }

    // The default is CENTROID
    startP();
    print( "RESULT CENTROID: the power of the air conditionner is " + hvacPower.toString()  );

    print( "RESULT CENTROID_LOWER: the power of the air conditionner is " + hvacPower.toString(undefined, FuzzyCrispAlgorithm.CENTROID_LOWER)  );

    print( "RESULT CENTROID_HIGHER: the power of the air conditionner is " + hvacPower.toString(undefined, FuzzyCrispAlgorithm.CENTROID_HIGHER)  );

    print( "RESULT MEAN: the power of the air conditionner is " + hvacPower.toString(undefined, FuzzyCrispAlgorithm.MEAN)  );

    print( "RESULT MEAN_HIGHER: the power of the air conditionner is " + hvacPower.toString(undefined, FuzzyCrispAlgorithm.MEAN_HIGHER)  );

    print( "RESULT MEAN_LOWER: the power of the air conditionner is " + hvacPower.toString(undefined, FuzzyCrispAlgorithm.MEAN_LOWER)  );
    endP();

    endP();

    endP();
}