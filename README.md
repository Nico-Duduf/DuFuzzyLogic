# DuFuzzyLogic
Fuzzy Logic Implementation

## What is Fuzzy Logic

Fuzzy Logic is a way to replace Boolean logic when values may not be *completely* true or false, e.g. a temperature can be hot, but more precisely it can be *just a bit* hot or *very* hot.

Using Fuzzy Logic is a way to test the veracity of a statement, and get a nuanced result, which can then be used to set nuanced values according to the truthness, the veracity, obtained from the statement.

For example, if one wants to adjust the power of a fan, he needs to check the temperature and adjust the fan accordingly.

With boolean logic, the statement `IF the temperature IS hot THEN SET the fan on` will either turn the fan on at full power or completely off, according to a predefined limit value.

With Fuzzy Logic, both the veracity and the result being fuzzy and more nuanced, the same statement will adjust precisely the power of the fan according to the hotness. With a single simple rule like this, it is like a conversion (interpolation) of the temperature value into a power value.

[To read more details, a very comprehensive description is available on the wiki here.](https://github.com/Nico-Duduf/DuFuzzyLogic/wiki)

## Implementation

For now, this is an implementation of Fuzzy Logic for JavaScript, but I plan to implement it the same way in Qt/C++, Python, and probably C# for Unity.

### JavaScript

### Introduction

The source is available in [src/js](https://github.com/Nico-Duduf/DuFuzzyLogic/tree/master/src/JS). Everything is full [documented](https://github.com/Nico-Duduf/DuFuzzyLogic/tree/master/docs/js).

The code is fully compatible with *Adobe ExtendScript* and *Adobe After Effects Expressions*.

The implementation creates 4 new classes:

- `FuzzyLogic` is the main class, the logic engine.
- `FuzzySet` represents fuzzy sets.
- `FuzzyValue` represents fuzzy values.
- `FuzzyVeracity` represents the veracity used in the rules instead of booleans.

This implementation uses fluent syntax for the logic, thus operators are methods of the `FuzzyVeracity` class which return `FuzzyVeracity` instances.

Here is an example of a rule in this fluent syntax which result is stored in a variable:

```js
var isRed = redChannel.IS( intense )
     .AND(
        greenChannel.IS( intense ).
        NOR( blueChannel.IS( intense ))
     )
```

In this example, isRed is an instance of `FuzzyVeracity`, `redChannel`, `greenChannel`, `blueChannel` are `FuzzyValues` and intense is a `FuzzySet`

### Examples

#### Simple Color example


```JavaScript
// Setup
var logic = new FuzzyLogic();

// We don't need to worry about values above 255
var intense = logic.newSet("Intense", 0, 255);

// The color to test
var color = [255,200,10];
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

// Print the result
Print("[" + color.toString() + "] is " + redness.quantify( intense ).toString() + " Red");
```

This is what is printed:

> [255,200,10] is Somewhat Red

#### Air conditionning: a comprehensive example


This is a comprehensive example meant to show how to use multiple sets and rules to control a (fake) air conditionning system.

Here's how this system is supposed to work, based on measured temperature (in `°C`) and humidity in the air (in `%`).

- The system is controlled by a "power" parameter in the range [-100%, 100%]. When it is negative, it cools down the room, when it is positive, it heats it up.
- The system takes the humidity into account. Let's say when the air is humid, we feel colder or hotter, so we need the system to run at a higher  - or lower if it cooling - power.
- With the same reasoning, when the air is dry, we want to lower the power consumption (because it's better for the planet).

This system is designed to show how using Fuzzy Logic makes things simpler in the code, but it is unnecessarily complex. For example in real life, it would not be the same value which controls both heating and cooling, and the rules would be a bit simpler.

#### 1 - Setup

First things firts, let's create the engine.

```JavaScript
var logic = new FuzzyLogic( FuzzyLogicAlgorithm.HYPERBOLIC );
```

The parameter changes the algorithm used for logic rules. It is optionnal, and slightly changes the behaviour of the system.

Now we can create the sets. This is the most important part, the parameters used in the sets will have a big impact on the results. We can see these values as the settings of the air conditionning system.

Humidity:

```JavaScript
// Too wet is more than 70%, completely wet is 100%. Constant shape above 100%: it's still too wet!
var wet = logic.newSet("Wet", 60, 100, FuzzyShape.GAUSSIAN, FuzzyShape.CONSTANT);
// The comfort zone begins at 40%, and its most comfortable at 60%. We use the same shape above and below this comfort zone.
var comfortable = logic.newSet("Comfortable", 40, 55, FuzzyShape.SIGMOID);
// Too dry is less than 50%, completely dry is 0%. Constant shape under 0%: it's still too dry!
    var dry = logic.newSet("Dry", 50, 0, FuzzyShape.CONSTANT, FuzzyShape.GAUSSIAN);
```

Temperature:

```JavaScript
// Temperature
// The principle is the same than humidity.
var hot = logic.newSet("Hot", 21, 35, FuzzyShape.GAUSSIAN, FuzzyShape.CONSTANT);
var warm = logic.newSet("Comfortably warm", 17, 20, FuzzyShape.GAUSSIAN);
var cold = logic.newSet("Cold", 17, 10, FuzzyShape.CONSTANT, FuzzyShape.GAUSSIAN);
```

Heating, ventilation and air-conditioning power:

```JavaScript
// Let's say a positive power (from 0% to 100%) heats the room, a negative one cools it.
var heat = logic.newSet("Heat", 0, 100, FuzzyShape.LINEAR, FuzzyShape.CONSTANT);
var refresh = logic.newSet("Refresh", 0, -100, FuzzyShape.CONSTANT, FuzzyShape.LINEAR);
```

#### 2 - Values

Input Values: We have two input values. These are what is going to vary, the result of the sensors.

```JavaScript
// Change these values to test the engine
var temperature = logic.newValue( 20, "°C" );
var humidity = logic.newValue( 50 , "%" );
```

Output Value: There is one output value, which is the power of the air conditionning system.

```JavaScript
var hvacPower = logic.newValue( 0, "%" );
// Enable reports to be able to have a look at the result of the logic
hvacPower.reportEnabled = true;
```

#### 2 - Rules

This is the fun part, just write some rules!

The easy ones first.

```JavaScript
// If it's hot, let's cool down
logic.IF( temperature.IS( hot ) ); 
logic.THEN( hvacPower, refresh  ); // Rule #1

// If it's cold, let's heat up
logic.IF( temperature.IS( cold ) ); 
logic.THEN( hvacPower, heat ); // Rule #2
```

But we want to adjust depending on the humidity.  
The (fake) idea is that if it's too humid, we need more power (because we feel less comfortable?).  

```JavaScript
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

If it's dry, we lower the power (because we don't want the hvac to make the air even drier)

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
```

And if it's really comfortably warm or cold, but wet, let's raise the temperature a lil'bit more

```JavaScript
logic.IF(
    temperature.IS( warm, "very" )
    .OR ( temperature.IS(cold) )
    .AND ( humidity.IS( wet ) )
)
logic.THEN( hvacPower, heat, "Somewhat" ); // Rule #7
```

Of course, if it's just comfortable, we want to stop the hvac.

```JavaScript
logic.IF( temperature.IS( warm ) );
logic.THEN( hvacPower, heat, "not"); // Rule #8
logic.THEN( hvacPower, refresh, "not"); // Rule #9
```

#### 3 - Results

The Print() in this example can be replaced by any method which shows/prints a string.

```JavaScript
// Print the result
Print( temperature.toString( hot ) + " and " + temperature.toString( cold ) );
Print( humidity.toString(wet) + " and " + humidity.toString( dry )  );
Print( "" );
Print( temperature.toString( warm ) );
Print( humidity.toString( comfortable ) );
Print( "" );
Print( "RESULT: the power of the air conditionner is " + hvacPower.toString()  );
Print( "" );
Print( "This is how this result is obtained:")
for (var i = 0, num = hvacPower.report.length; i < num; i++)
{
    Print( "" );
    Print( hvacPower.report[i].join("<br />") );
}
```

This is what will be printed with 25°C and 75% humidity.

> 25°C is Somewhat Hot and 25°C is Not Cold  
75% is Somewhat Wet and 75% is Not Dry

> 25°C is Not Comfortably warm  
75% is Not Comfortable

> **RESULT: the power of the air conditionner is _-47.51%_**

> This is how this result is obtained:  

> Rule #1: Set Refresh (Moderately)  
Gives value: -23.303 from these values: [ -23.303 ]  
With a veracity of: 0.243

> Rule #2: Set Heat (Moderately)  
Gives value: 0 from these values: [ 0 ]  
With a veracity of: 0

> Rule #3: Set Refresh (More)  
Gives value: -119.8 from these values: [ -100, -100, -100, -200, -99 ]  
With a veracity of: 0.082

> Rule #4: Set Heat (More)  
Gives value: 120 from these values: [ 100, 100, 100, 100, 200 ]  
With a veracity of: 0

> Rule #5: Set Heat (Less)  
Gives value: 0 from these values: [ 0 ]  
With a veracity of: 0

> Rule #6: Set Refresh (Less)  
Gives value: 0 from these values: [ 0 ]  
With a veracity of: 0

> Rule #7: Set Heat (Somewhat)  
Gives value: 0 from these values: [ 0 ]  
With a veracity of: 0

> Rule #9: Set Refresh (Not)  
Gives value: 0 from these values: [ 0 ]  
With a veracity of: 0

> Rule #9: Set Heat (Not)  
Gives value: 0 from these values: [ 0 ]  
With a veracity of: 0

You can also compare different crispification algorithms quite easily:

```JavaScript
// The default is CENTROID
Print( "RESULT CENTROID: the power of the air conditionner is " + hvacPower.toString()  );

Print( "RESULT CENTROID_LOWER: the power of the air conditionner is " + hvacPower.toString(FuzzyCrispAlgorithm.CENTROID_LOWER)  );

Print( "RESULT CENTROID_HIGHER: the power of the air conditionner is " + hvacPower.toString(FuzzyCrispAlgorithm.CENTROID_HIGHER)  );

Print( "RESULT MEAN: the power of the air conditionner is " + hvacPower.toString(FuzzyCrispAlgorithm.MEAN)  );

Print( "RESULT MEAN_HIGHER: the power of the air conditionner is " + hvacPower.toString(FuzzyCrispAlgorithm.MEAN_HIGHER)  );

Print( "RESULT MEAN_LOWER: the power of the air conditionner is " + hvacPower.toString(FuzzyCrispAlgorithm.MEAN_LOWER)  );

// Note that you can also globally set the algorithm as a second argument when creating the engine:
var lowerLogic = new FuzzyLogic( FuzzyLogicAlgorithm.LINEAR, FuzzyCrispAlgorithm.CENTROID_LOWER);
// The default for crispification will be the one passed to this engine
```

Which will print:

> RESULT CENTROID: the power of the air conditionner is -47.51%  
> RESULT CENTROID_LOWER: the power of the air conditionner is -67.71%  
> RESULT CENTROID_HIGHER: the power of the air conditionner is -42.27%  
> RESULT MEAN: the power of the air conditionner is -2.57%  
> RESULT MEAN_HIGHER: the power of the air conditionner is 8.63%  
> RESULT MEAN_LOWER: the power of the air conditionner is -13.7%
