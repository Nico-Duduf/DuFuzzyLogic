# Rules

Rules are defined by operators, like `AND`, `OR`, `EQUALS`, etc. While it is easy to understand what these operators do in Boolean Logic, with Fuzzy Logic there are several ways of defining and implementing them, as the result of `IF the temperature IS hot AND the temperature IS comfortable` is neither *true* or *false*, but a veracity in the range [0, 1].

Wikipedia has a nice [List of operators](https://commons.wikimedia.org/wiki/Fuzzy_operator) with representations of them to easily compare the algorithms.

## Implementation

With the veracity `x`, `y` and the weight `w` in the range `[0,1]` for fuzzy logic, and `x,y,w = 0` or `1` for boolean logic.

| Name | JavaScript, C... Boolean | Python Boolean | Fuzzy: Zadeh (linear) | Fuzzy: Hyperbolic Parabloid | Fuzzy: Yager-2 |
|------ |---|----|---| ------ | ----- |
|NOT(x)| `!x`| `not x` | `1-x`|`1-x`|`1-x`|
|AND(x,y)| `x && y` | `x and y` | `min(x,y)`| `xy` | `1- min( 1, sqrt( (1-x)² + (1-y)² ) )` |
|OR(x,y)| `x || y`| `x or y` |  `max(x,y)` | `x+y - xy` | `min( 1, (x² + y²)² )` |
|XOR(x,y)| `x != y` | `x is not y` | `x + y - 2min(x,y)` | `x+y - 2xy` | |
|NXR(x,y)| `x == y` | `x is y` | `1-x-y + 2*min(x,y)` | `1-x-y + (2xy)` | |
|IMPLIES(x,y)| `!(x && !y)` | `not (x and not y)`| `1 - min(x, 1-y)` | `1 - x + xy` ||
|DOES_NOT_IMPLY(x,y)| `x && !y`| `x and not y`| `min(x,1-y)`| `x*(1-y)`||
|NAND(x,y)|`!(x && y)`| `not (x and y)` | `1-min(x,y)` | `1 - xy` | |
|NOR(x,y)| `!(x || y)`|`not (x or y)` | `1 - max(x,y)` | `1-x-y + xy`| |
|WEIGHTED(x,y,w| | | `wx + (1-w)y` | `wx + (1-w)y` | `wx + (1-w)y` |
