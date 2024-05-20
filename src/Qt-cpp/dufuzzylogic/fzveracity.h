#ifndef VERACITY_H
#define VERACITY_H

#include "engine.h"
#include "qglobal.h"

#include <cmath>

namespace FzL
{

/**
 * @brief The DuFuzzyVeracity class is the core of fuzzy logics,
 * it is the equivalent of the bool with boolean logic, except
 * it's basically represented by a float in the range [0.0 ... 1.0]_
 */
class Veracity
{
public:
    Veracity() {};
    Veracity(Engine::Algorithm algorithm):
        _a(algorithm) {};
    Veracity(bool isTrue, Engine::Algorithm algorithm = Engine::Hyperbolic):
        _a(algorithm) { if (isTrue) _v = 1.0; };
    Veracity(qreal veracity, Engine::Algorithm algorithm = Engine::Hyperbolic):
        _v(veracity), _a(algorithm) { };

    float value() const { return _v; };
    void setValue(float value) { _v = value; };

    Engine::Algorithm algorithm() const;;
    void setAlgorithm(Engine::Algorithm algorithm) { _a = algorithm; };

private:
    float _v = 0.0;
    Engine::Algorithm _a = Engine::Default;
};

}

// Logic operators

// ==== Between Veracities ====

/**
 * @brief operator == All comparisons are made using the algorithm defined by the first veracity (righthand side)
 * @param a
 * @param b
 * @return
 */
inline FzL::Veracity operator==(const FzL::Veracity &a, const FzL::Veracity &b) {
    float x = a.value();
    float y = b.value();

    float v = 0;
    switch(a.algorithm()) {
    case FzL::Engine::Linear:
        v = 1-x-y + 2*std::fmin(x,y);
        break;
    case FzL::Engine::Default:
    case FzL::Engine::Hyperbolic:
        v = 1-x-y + 2*x*y;
        break;
    }

    return new FzL::Veracity( v, a.algorithm() );
}

/**
 * @brief operator ! Negation for a veracity
 * @param v
 * @return
 */
inline FzL::Veracity operator!(const FzL::Veracity &v) {
    return FzL::Veracity(1 - v.value(), v.algorithm());
}

/**
 * @brief operator !=
 * @param a
 * @param b
 * @return
 */
inline FzL::Veracity operator!=(const FzL::Veracity &a, const FzL::Veracity &b) {
    return (!a) == b;
}

/**
 * @brief operator && AND
 * @param a
 * @param b
 * @return
 */
inline FzL::Veracity operator&&(const FzL::Veracity &a, const FzL::Veracity &b) {
    float x = a.value();
    float y = b.value();

    float v = 0;
    switch(a.algorithm()) {
    case FzL::Engine::Linear:
        v = std::fmin(x, y);
        break;
    case FzL::Engine::Default:
    case FzL::Engine::Hyperbolic:
        v = x*y;
        break;
    }

    return FzL::Veracity( v, a.algorithm() );
}

/**
 * @brief operator || OR
 * @param a
 * @param b
 * @return
 */
inline FzL::Veracity operator||(const FzL::Veracity &a, const FzL::Veracity &b) {
    float x = a.value();
    float y = b.value();

    float v = 0;
    switch(a.algorithm()) {
    case FzL::Engine::Linear:
        v = std::fmax(x, y);
        break;
    case FzL::Engine::Default:
    case FzL::Engine::Hyperbolic:
        v = x + y - x*y;
        break;
    }

    return FzL::Veracity( v, a.algorithm() );
}

/**
 * @brief operator >
 * @param a
 * @param b
 * @return
 */
inline FzL::Veracity operator>(const FzL::Veracity &a, const FzL::Veracity &b) {
    float x = a.value();
    float y = b.value();

    float v = 0;
    if (x > y)
        v = x - y;

    return FzL::Veracity( v, a.algorithm() );
}

/**
 * @brief operator >=
 * @param a
 * @param b
 * @return
 */
inline FzL::Veracity operator>=(const FzL::Veracity &a, const FzL::Veracity &b) {
    return (a > b) || (a == b);
}

/**
 * @brief operator <
 * @param a
 * @param b
 * @return
 */
inline FzL::Veracity operator<(const FzL::Veracity &a, const FzL::Veracity &b) {
    return !(a >= b);
}

/**
 * @brief operator <=
 * @param a
 * @param b
 * @return
 */
inline FzL::Veracity operator<=(const FzL::Veracity &a, const FzL::Veracity &b) {
    return (a < b) || (a == b);
}

#endif // VERACITY_H
