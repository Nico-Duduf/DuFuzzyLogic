#include "value.h"

#include "math.h"
#include "veracity.h"
#include "engine.h"

void FzL::Value::set(const Set &s)
{
    set(s, currentVeracity());

    _crispCache.clear();
}

void FzL::Value::set(const Set &set, const Veracity &veracity)
{
    rules.insert(set, veracity);

    _crispCache.clear();
}

QVariant FzL::Value::crisp()
{
    return crisp(_crispA);
}

QVariant FzL::Value::crisp(CrispificationAlgorithm algorithm)
{
    if (rules.isEmpty())
        return _v;

    QVariant cache = _crispCache.value(algorithm);
    if (cache.isValid())
        return cache;

    QVariant crisp;

    // get all average values
    // and veracities from the sets
    qreal sumWeights = 0;
    QHashIterator<Set,Veracity> i(rules);
    while( i.hasNext()) {
        i.next();
        Set set = i.key();
        Veracity v = i.value();

        QVector<QVariant> ruleValues = set.values(v);
        QVariant ruleValue;

        switch(algorithm) {
        case CENTROID:
        case MEAN:
            ruleValue = Math::mean(ruleValues);
            break;
        case CENTROID_LOWER:
        case MEAN_LOWER:
            ruleValue = ruleValues.first();
            break;
        case CENTROID_HIGHER:
        case MEAN_HIGHER:
            ruleValue = ruleValues.last();
            break;
        case RANDOM:
        case RANDOM_TRUE:
        case RANDOM_CENTROID:
            // TODO
            return QVariant();
        }

        if (!crisp.isValid()) {
            crisp = ruleValue;
            continue;
        }

        switch(algorithm) {
        case CENTROID:
        case CENTROID_LOWER:
        case CENTROID_HIGHER:
        case RANDOM_CENTROID:
            crisp = crisp + ( ruleValue * v.value() );
            sumWeights += v.value();
            break;
        case MEAN:
        case MEAN_LOWER:
        case MEAN_HIGHER:
        case RANDOM:
            crisp = crisp + ruleValue;
            sumWeights += 1;
            break;
        case RANDOM_TRUE:
            // TODO
            return QVariant();
        }
    }

    // Weight
    if (sumWeights != 0) crisp = crisp / sumWeights;

    _crispCache.insert(algorithm, crisp);
    return crisp;
}