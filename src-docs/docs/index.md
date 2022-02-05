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

For now, this is an implementation of Fuzzy Logic for JavaScript and Python, but I plan to implement it the same way in Qt/C++, and maybe C# for Unity.

The source is available in [this repo](https://github.com/Nico-Duduf/DuFuzzyLogic/tree/master/src/JavaScript). Everything is fully [documented](https://dufuzzylogic-docs.rainboxlab.org/js/index.html).

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

It is the equivalent of the boolean logi:

```js
var isRed = redChannel == intense && !( greenChannel == intense || blueChannel == intenst )
```

> -> [**Read the reference**](https://dufuzzylogic-docs.rainboxlab.org/js/index.html) for all the details.

## After Effects Expressions Implementation

The implementation of the same library but adapted for expressions in After Effects (some changes have been made for better compatibility with both the extendscript and the javascript engine) is available as part of the [DuAEF Expression Library](https://github.com/Rainbox-dev/DuAEF_ExpressionLib).

## License

![GNU](images/logos/gnu.png) 

### This documentation

**Copyright (C) 2020 Nicolas Dufresne and Contributors.**  
Permission is granted to copy, distribute and/or modify this document under the terms of the *GNU Free Documentation License*, Version 1.3 or any later version published by the Free Software Foundation;  
with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
A copy of the license is included in the section entitled "[Documentation License](doc-license.md)".

![GFDL](images/logos/gfdl-logo.png)

### This implementation of Fuzzy Logics

DuFuzzyLogic is free software released under the [GNU-General Public License v3](https://github.com/Rainbox-dev/DuAEF_Duik/blob/master/LICENSE). This license guarantees you four freedoms:

- The freedom to **run the program as you wish**, for any purpose,  
- The freedom to **study how the program works, and change it**, so it does your computing as you wish,  
- The freedom to **redistribute copies** so you can help your fellow animator  
- The freedom to distribute **copies of your modified versions** to others.

A copy of the license is included in the section entitled "[GNU-GPLv3](gnu-gpl.md)".

![GPL](images/logos/gplv3.png)