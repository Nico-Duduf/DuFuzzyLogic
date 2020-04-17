# Color: Evaluate Redness

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
