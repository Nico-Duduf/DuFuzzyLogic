QT = core \
     gui

CONFIG += c++17 cmdline

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

INCLUDEPATH += \
        dufuzzylogic/

SOURCES += \
        dufuzzylogic/engine.cpp \
        dufuzzylogic/math.cpp \
        dufuzzylogic/set.cpp \
        dufuzzylogic/value.cpp \
        dufuzzylogic/veracity.cpp \
        main.cpp

HEADERS += \
    dufuzzylogic/duffuzylogic.h \
    dufuzzylogic/math.h \
    dufuzzylogic/shapes/abstractshape.h \
    dufuzzylogic/engine.h \
    dufuzzylogic/set.h \
    dufuzzylogic/shapes/constantshape.h \
    dufuzzylogic/shapes/gaussianshape.h \
    dufuzzylogic/shapes/linearshape.h \
    dufuzzylogic/shapes/reversedgaussianshape.h \
    dufuzzylogic/shapes/sigmoidshape.h \
    dufuzzylogic/shapes/squareshape.h \
    dufuzzylogic/value.h \
    dufuzzylogic/veracity.h


# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
