#ifndef FZVERACITY_H
#define FZVERACITY_H

#include "fzengine.h"
#include "qglobal.h"

#include <cmath>


/**
 * @brief The DuFuzzyVeracity class is the core of fuzzy logics,
 * it is the equivalent of the bool with boolean logic, except
 * it's basically represented by a float in the range [0.0 ... 1.0]_
 */
class FzVeracity
{
public:
    FzVeracity() {};
    FzVeracity(FzEngine::Algorithm algorithm):
        _a(algorithm) {};
    FzVeracity(bool isTrue, FzEngine::Algorithm algorithm = FzEngine::Hyperbolic):
        _a(algorithm) { if (isTrue) _v = 1.0; };
    FzVeracity(qreal veracity, FzEngine::Algorithm algorithm = FzEngine::Hyperbolic):
        _v(veracity), _a(algorithm) { };

    float value() const { return _v; };
    void setValue(float value) { _v = value; };

    FzEngine::Algorithm algorithm() const;;
    void setAlgorithm(FzEngine::Algorithm algorithm) { _a = algorithm; };

private:
    float _v = 0.0;
    FzEngine::Algorithm _a = FzEngine::Default;
};

// Logic operators

// ==== Between Veracities ====

/**
 * @brief operator == All comparisons are made using the algorithm defined by the first veracity (righthand side)
 * @param a
 * @param b
 * @return
 */
inline FzVeracity operator==(const FzVeracity &a, const FzVeracity &b) {
    float x = a.value();
    float y = b.value();

    float v = 0;
    switch(a.algorithm()) {
    case FzEngine::Linear:
        v = 1-x-y + 2*std::fmin(x,y);
        break;
    case FzEngine::Default:
    case FzEngine::Hyperbolic:
        v = 1-x-y + 2*x*y;
        break;
    }

    return new FzVeracity( v, a.algorithm() );
}

/**
 * @brief operator ! Negation for a veracity
 * @param v
 * @return
 */
inline FzVeracity operator!(const FzVeracity &v) {
    return FzVeracity(1 - v.value(), v.algorithm());
}

/**
 * @brief operator !=
 * @param a
 * @param b
 * @return
 */
inline FzVeracity operator!=(const FzVeracity &a, const FzVeracity &b) {
    return (!a) == b;
}

/**
 * @brief operator && AND
 * @param a
 * @param b
 * @return
 */
inline FzVeracity operator&&(const FzVeracity &a, const FzVeracity &b) {
    float x = a.value();
    float y = b.value();

    float v = 0;
    switch(a.algorithm()) {
    case FzEngine::Linear:
        v = std::fmin(x, y);
        break;
    case FzEngine::Default:
    case FzEngine::Hyperbolic:
        v = x*y;
        break;
    }

    return FzVeracity( v, a.algorithm() );
}

/**
 * @brief operator || OR
 * @param a
 * @param b
 * @return
 */
inline FzVeracity operator||(const FzVeracity &a, const FzVeracity &b) {
    float x = a.value();
    float y = b.value();

    float v = 0;
    switch(a.algorithm()) {
    case FzEngine::Linear:
        v = std::fmax(x, y);
        break;
    case FzEngine::Default:
    case FzEngine::Hyperbolic:
        v = x + y - x*y;
        break;
    }

    return FzVeracity( v, a.algorithm() );
}

/**
 * @brief operator >
 * @param a
 * @param b
 * @return
 */
inline FzVeracity operator>(const FzVeracity &a, const FzVeracity &b) {
    float x = a.value();
    float y = b.value();

    float v = 0;
    if (x > y)
        v = x - y;

    return FzVeracity( v, a.algorithm() );
}

/**
 * @brief operator >=
 * @param a
 * @param b
 * @return
 */
inline FzVeracity operator>=(const FzVeracity &a, const FzVeracity &b) {
    return (a > b) || (a == b);
}

/**
 * @brief operator <
 * @param a
 * @param b
 * @return
 */
inline FzVeracity operator<(const FzVeracity &a, const FzVeracity &b) {
    return !(a >= b);
}

/**
 * @brief operator <=
 * @param a
 * @param b
 * @return
 */
inline FzVeracity operator<=(const FzVeracity &a, const FzVeracity &b) {
    return (a < b) || (a == b);
}

#endif // FZVERACITY_H
