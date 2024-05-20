QT = core \
     gui

CONFIG += c++17 cmdline

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

INCLUDEPATH += \
        dufuzzylogic/

SOURCES += \
        dufuzzylogic/fzengine.cpp \
        dufuzzylogic/fzmath.cpp \
        dufuzzylogic/fzset.cpp \
        dufuzzylogic/fzvalue.cpp \
        dufuzzylogic/fzveracity.cpp \
        main.cpp

HEADERS += \
    dufuzzylogic/fzengine.h \
    dufuzzylogic/fzmath.h \
    dufuzzylogic/fzset.h \
    dufuzzylogic/fzvalue.h \
    dufuzzylogic/fzveracity.h \
    dufuzzylogic/rxfuzzylogic.h \
    dufuzzylogic/shapes/fzabstractshape.h \
    dufuzzylogic/shapes/fzconstantshape.h \
    dufuzzylogic/shapes/fzgaussianshape.h \
    dufuzzylogic/shapes/fzlinearshape.h \
    dufuzzylogic/shapes/fzreversedgaussianshape.h \
    dufuzzylogic/shapes/fzsigmoidshape.h \
    dufuzzylogic/shapes/fzsquareshape.h


# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
