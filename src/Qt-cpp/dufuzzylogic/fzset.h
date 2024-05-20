#ifndef SET_H
#define SET_H

#include <QVariant>
#include <QEasingCurve>

namespace FzL
{

class Veracity;
class Value;
class AbstractShape;

/**
 * @brief The DuFuzzySet class represents a set of fuzzy values,
 * i.e. a qualifier for values.
 */
class Set
{
public:

    /**
     * @brief Set Construcst a default, invalid and always empty set
     */
    Set();

    /**
     * @brief Set
     * @param name should be unique
     * @param shapeIn The shape on the minimum side of the set
     * @param shapeOut The shape on the maximum side of the set
     */
    Set(const QString &name,
        AbstractShape *shapeIn,
        AbstractShape *shapeOut
        );

    /**
     * Destructor
     */
    ~Set();

    /**
     * @brief contains Checks if the set contains the given value
     * @param value
     * @return
     */
    Veracity contains(Value &value) const;

    /**
     * @brief contains Checks if the set contains the given value
     * @param value
     * @return
     */
    Veracity contains(const QVariant &value) const;

    /**
     * @brief values are a list of crisp and valid values for a given veracity.
     * @param veracity
     * @return
     */
    QVector<QVariant> values(const Veracity &veracity) const;

    /**
     * @brief name is a (unique) name for this set, set with the constructor
     * @return
     */
    QString name() const { return _name; };

    /**
     * @brief isValid An invalid set is always empty.
     * @return
     */
    bool isValid() const { return _shapeIn && _shapeOut; };

private:
    QString _name;
    AbstractShape *_shapeIn;
    AbstractShape *_shapeOut;
};

inline bool operator==(const Set &a, const Set &b) {
    return a.name() == b.name();
}

inline uint qHash(const Set &set) {
    return qHash(set.name());
}

}

#endif // SET_H
