#ifndef FZENGINE_H
#define FZENGINE_H

#include <QPointer>

class FzValue;
class FzSet;
class FzVeracity;

/**
 * @brief The DuFuzzyEngine class configures the engine
 * static methods provide quick access to an instance to be used globally,
 * but the class can also be instanciated to use a custom local engine.
 */
class FzEngine
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

    static FzEngine *globalEngine();

    FzEngine();
    FzEngine(Algorithm algorithm);
    ~FzEngine();

    Algorithm algorithm() { return _a; };
    void setAlgorithm(Algorithm algorithm) { _a = algorithm; };

    void setVeracity(const FzVeracity &v);
    FzVeracity veracity();

    FzVeracity fif(const FzVeracity &v);
    FzVeracity fif(const FzVeracity &v, std::function<void(FzVeracity)> then);

    void then(FzValue *v, const FzSet &s);

private:
    static FzEngine *_globalEngine;
    Algorithm _a = Default;
    FzVeracity *_v;
};

#endif // FZENGINE_H
