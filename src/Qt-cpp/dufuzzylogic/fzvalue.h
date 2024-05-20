#ifndef VALUE_H
#define VALUE_H

#include <QVariant>

#include "set.h"
#include "veracity.h"

namespace FzL
{

/**
 * @brief The DuFuzzyValue class is similar to the QVariant class,
 * except it's designed to be used with fuzzy logics and DuFuzzySet
 */
class Value
{
public:
    /**
     * @brief The CrispificationAlgorithm enum of the algorithms to use when crispifying values.
     */
    enum CrispificationAlgorithm {
        /**
     * Uses the centroid method: combines all sets and values and gets the centroid.<br />
     * This method works great to combine more than a couple of rules, but will not work with single rules.
     */
        CENTROID = 0,
        /**
     * When several values are possible from each set, prefer the lowest one, then combine them to get the centroid.<br />
     * This method works like the centroid and works well even with single rules, but the returned values will tend to be a bit lower.
     */
        CENTROID_LOWER = 1,
        /**
     * When several values are possible from each set, prefer the highest one, then combine them to get the centroid.<br />
     * This method works like the centroid and works well even with single rules, but the returned values will tend to be a bit higher.
     */
        CENTROID_HIGHER = 2,
        /**
     * NOT IMPLEMENTED YET
     * Returns a randomly chosen value from all possible values.
     */
        RANDOM = 3,
        /**
     * NOT IMPLEMENTED YET
     * Returns a randomly chosen value from all possible values from the set with the highest veracity.
     */
        RANDOM_TRUE = 4,
        /**
     * NOT IMPLEMENTED YET
     * Returns a single random value from each set then combines them to get the centroid.
     */
        RANDOM_CENTROID = 5,
        /**
     * Returns the mean value from all possible values from all the sets.<br />
     * Unlike the centroid methods, the mean method does not take the veracity of each set into account.
     */
        MEAN = 6,
        /**
     * Returns the mean value from all the highest possible values from all the sets.<br />
     * Unlike the centroid methods, the mean method does not take the veracity of each set into account.
     */
        MEAN_HIGHER = 7,
        /**
     * Returns the mean value from all the lowest possible values from all the sets.<br />
     * Unlike the centroid methods, the mean method does not take the veracity of each set into account.
     */
        MEAN_LOWER = 8
    };

    /**
     * @brief Value Constructs an empty fuzzy value
     */
    Value() {};

    /**
     * @brief Value Constructs a new fuzzy value from a crisp (standard) value
     * @param crispValue
     */
    Value(const QVariant &crispValue):
        _v(crispValue) {};

    /**
     * @brief Value Constructs a new fuzzy value from a crisp (standard) value,
     * and set the crispification algorithm to use to generate crisp values
     * @param crispValue
     * @param cripsAlgorithm
     */
    Value(const QVariant &crispValue, CrispificationAlgorithm cripsAlgorithm):
        _v(crispValue), _crispA(cripsAlgorithm) {};

    /**
     * @brief value The original crisp value which was set when constructing this fuzzy value
     * @return
     */
    QVariant value() const { return _v; };
    /**
     * @brief s Modifies the fuzzy value according to the inclusion in the given s,
     * Using the current global veracity (i.e. Engine::globalEngine()->veracity() )
     * @param s
     */
    void set(const Set &s);
    /**
     * @brief set Modifies the fuzzy value according to the inclusion in the given set
     * @param set
     * @param veracity of inclusion in the set
     */
    void set(const Set &set, const Veracity &veracity = true);

    /**
     * @brief crispificationAlgorithm
     * @return
     */
    CrispificationAlgorithm crispificationAlgorithm() const { return _crispA; };
    /**
     * @brief setCrispificationAlgorithm
     * @param algorithm
     */
    void setCrispificationAlgorithm(CrispificationAlgorithm algorithm) { _crispA = algorithm; };

    /**
     * @brief clear Empties all the rules (i.e. the values added using set() )
     */
    void clear() { rules.clear(); _crispCache.clear(); };
    /**
     * @brief clear Empties all the rules (i.e. the values added using set() )
     * And sets a new default crisp value
     * @param newValue
     */
    void clear(const QVariant &newValue) { clear(); _v = newValue; };

    /**
     * @brief crisp Calculates a crisp value using the current crispification algorithm
     * @return
     */
    QVariant crisp();
    /**
     * @brief crisp Calculates a crisp value using a custom crispification algorithm
     * @param algorithm
     * @return
     */
    QVariant crisp(CrispificationAlgorithm algorithm);

private:
    QVariant _v;
    QHash<CrispificationAlgorithm, QVariant> _crispCache;
    CrispificationAlgorithm _crispA = CENTROID_LOWER;

    QMultiHash<Set, Veracity> rules;
};

inline Veracity operator==(Value &value, const Set &set) {
    return set.contains(value);
}

inline Veracity operator==(QVariant &value, const Set &set) {
    return set.contains(value);
}

inline Veracity operator!=(Value &value, const Set &set) {
    return !set.contains(value);
}

inline Veracity operator!=(QVariant &value, const Set &set) {
    return !set.contains(value);
}

}

#endif // VALUE_H
