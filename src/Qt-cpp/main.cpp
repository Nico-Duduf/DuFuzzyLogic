#include <QCoreApplication>

#include <QtDebug>

#include "duffuzylogic.h"

int main(int argc, char *argv[])
{
    //QCoreApplication a(argc, argv);

    // Create a set
    FzL::Set intense(
        "Intense",
        new FzL::LinearShape(0, 255),
        new FzL::ConstantShape(255)
        );

    // The color to test
    QColor color(255, 125, 0);

    // A value to store the result
    FzL::Value redness;

    // Separate channels
    FzL::Value red( color.red() );
    FzL::Value green( color.green() );
    FzL::Value blue( color.blue() );

    // The logic
    FzL::fif( red == intense && green != intense && blue != intense);
    FzL::then(&redness, intense);

    // Print the result
    qInfo().noquote() << color.name() << "is" << int(FzL::currentVeracity().value()*100) << "% red";

    // Create the equivalent pure red color
    QColor newRed( redness.crisp().toInt(), 0, 0);
    qInfo().noquote() << newRed.name() << "is the equivalent pure red color with the red channel at" << redness.crisp();

    // Quit
    return 0;

    //return a.exec();
}
