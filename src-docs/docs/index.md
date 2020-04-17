# DuFuzzyLogic

A Fuzzy Logic Implementation

[TOC]

## What is Fuzzy Logic?

Fuzzy Logic is a way to replace Boolean logic when values may not be *completely* true or false, e.g. a temperature can be hot, but more precisely it can be *just a bit* hot or *very* hot.

Using Fuzzy Logic is a way to test the veracity of a statement, and get a nuanced result, which can then be used to set nuanced values according to the truthness, the veracity, obtained from the statement.

For example, if one wants to adjust the power of a fan, he needs to check the temperature and adjust the fan accordingly.

With boolean logic, the statement `IF the temperature IS hot THEN SET the fan on` will either turn the fan on at full power or completely off, according to a predefined limit value.

With Fuzzy Logic, both the veracity and the result being fuzzy and more nuanced, the same statement will adjust precisely the power of the fan according to the hotness. With a single simple rule like this, it is like a conversion (interpolation) of the temperature value into a power value.

> -> [**Read more about Fuzzy Logic**](Home.md)

## JavaScript Implementation

For now, this is an implementation of Fuzzy Logic for JavaScript, but I plan to implement it the same way in Qt/C++, Python, and probably C# for Unity.

The source is available in [this repo](https://github.com/Nico-Duduf/DuFuzzyLogic/tree/master/src/JS). Everything is fully [documented](https://dufuzzylogic-docs.rainboxlab.org/js).

The code is fully compatible with *Adobe ExtendScript* too.

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

In this example, isRed is an instance of `FuzzyVeracity`;  
`redChannel`, `greenChannel`, `blueChannel` are `FuzzyValues` and intense is a `FuzzySet`

> -> [**Read the reference**](https://dufuzzylogic-docs.rainboxlab.org/js) for all the details.

## After Effects Expressions Implementation

The implementation of the same library but adapted for expressions in After Effects (some changes have been made for better compatibility with both the extendscript and the javascript engine) is available as part of the [DuAEF Expression Library](https://github.com/Rainbox-dev/DuAEF_ExpressionLib).
