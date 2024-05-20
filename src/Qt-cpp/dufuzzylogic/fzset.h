#ifndef FZSET_H
#define FZSET_H

#include <QVariant>
#include <QEasingCurve>

class FzVeracity;
class FzValue;
class FzAbstractShape;

/**
 * @brief The DuFuzzySet class represents a set of fuzzy values,
 * i.e. a qualifier for values.
 */
class FzSet
{
public:

    /**
     * @brief FzSet Construcst a default, invalid and always empty set
     */
    FzSet();

    /**
     * @brief FzSet
     * @param name should be unique
     * @param shapeIn The shape on the minimum side of the set
     * @param shapeOut The shape on the maximum side of the set
     */
    FzSet(const QString &name,
        FzAbstractShape *shapeIn,
        FzAbstractShape *shapeOut
        );

    /**
     * Destructor
     */
    ~FzSet();

    /**
     * @brief contains Checks if the set contains the given value
     * @param value
     * @return
     */
    FzVeracity contains(FzValue &value) const;

    /**
     * @brief contains Checks if the set contains the given value
     * @param value
     * @return
     */
    FzVeracity contains(const QVariant &value) const;

    /**
     * @brief values are a list of crisp and valid values for a given veracity.
     * @param veracity
     * @return
     */
    QVector<QVariant> values(const FzVeracity &veracity) const;

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
    FzAbstractShape *_shapeIn;
    FzAbstractShape *_shapeOut;
};

inline bool operator==(const FzSet &a, const FzSet &b) {
    return a.name() == b.name();
}

inline uint qHash(const FzSet &set) {
    return qHash(set.name());
}

#endif // FZSET_H
