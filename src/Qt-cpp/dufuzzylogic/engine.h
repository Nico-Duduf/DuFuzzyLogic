#ifndef ENGINE_H
#define ENGINE_H

#include <QPointer>

namespace FzL
{

class Value;
class Set;
class Veracity;

// Quick access to the default engine

/**
 * @brief fif Shortcut for DuFFuzzyLogic::globalEngine()->fif()
 * @param v
 * @return
 */
Veracity fif(const Veracity &v);
/**
 * @brief fif Shortcut for FzL::Engine::globalEngine()->fif()
 * @param v
 * @param then is a lambda function to run which takes the veracity as argument
 * @return
 */
template<typename Then>
Veracity fif(const Veracity &v, Then&& then);
/**
 * @brief fif Shortcut for FzL::Engine::globalEngine()->then()
 * @param v
 * @return
 */
void then(Value *v, const Set &s);

/**
 * @brief veracity shortcut for FzL::Engine::globalEngine()->veracity
 * @return
 */
Veracity currentVeracity();


/**
 * @brief The DuFuzzyEngine class configures the engine
 * static methods provide quick access to an instance to be used globally,
 * but the class can also be instanciated to use a custom local engine.
 */
class Engine
{
public:
    /**
     * @brief The Algorithm enum of the algorithms to use for resolving veracities
     */
    enum Algorithm {
    /**
     * Default (i.e. Hyperbolic)
     */
        Default = 0,
    /**
     * Uses Zadeh's method, resulting in a linear logic.
     */
        Linear = 1,
    /**
     * Uses Hyperbolic Parabloid logic, which is a bit heavier than linear, but may have more intuitive results.
     */
        Hyperbolic = 2
    };

    static Engine *globalEngine();

    Engine();
    Engine(Algorithm algorithm);
    ~Engine();

    Algorithm algorithm() { return _a; };
    void setAlgorithm(Algorithm algorithm) { _a = algorithm; };

    void setVeracity(const Veracity &v);
    Veracity veracity();

    Veracity fif(const Veracity &v);
    template<typename Then>
    Veracity fif(const Veracity &v, Then &&then);
    void then(Value *v, const Set &s);

private:
    static Engine *_globalEngine;
    Algorithm _a = Default;
    Veracity *_v;
};

}

#endif // ENGINE_H
