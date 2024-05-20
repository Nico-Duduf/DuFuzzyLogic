# Qt / C++

## Introduction

## Examples

### Simple Color example

```c++
#include <QtDebug>
#include "duffuzylogic.h"

int main(int argc, char *argv[])
{
    // Get the default engine
    auto fz = FzEngine::globalEngine();

    // Create a set
    FzSet intense(
        "Intense",
        new FzLinearShape(0, 255),
        new FzConstantShape(255)
        );

    // The color to test
    QColor color(255, 125, 0);

    // A value to store the result
    FzValue redness;

    // Separate channels
    FzValue red( color.red() );
    FzValue green( color.green() );
    FzValue blue( color.blue() );

    // The logic
    fz->fif( red == intense &&
             green != intense &&
             blue != intense );
    fz->then(&redness, intense);

    // Print the result
    qInfo().noquote() << color.name() << "is" << int(fz->veracity().value()*100) << "% red";

    // Create the equivalent pure red color
    QColor newRed( redness.crisp().toInt(), 0, 0);
    qInfo().noquote() << newRed.name() << "is the equivalent pure red color with the red channel at" << redness.crisp();

    // Quit
    return 0;
}
```

Program output:

```
#ff7d00 is 50 % red
#820000 is the equivalent pure red color with the red channel at QVariant(double, 130)
```
