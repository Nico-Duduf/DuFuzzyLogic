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

- [Read the JavaScript starting guide here](https://github.com/Nico-Duduf/DuFuzzyLogic/blob/master/EXAMPLE-js.md)

- [Read the Python starting guide here](https://github.com/Nico-Duduf/DuFuzzyLogic/blob/master/EXAMPLE-py.md)
