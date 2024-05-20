#ifndef FZSIGMOIDSHAPE_H
#define FZSIGMOIDSHAPE_H

#include "fzabstractshape.h"
#include "fzmath.h"

class FzSigmoidShape : public FzAbstractShape
{
public:
    FzSigmoidShape(const QVariant &start, const QVariant &end):
        FzAbstractShape(start, end, Sigmoid) {};

protected:
    virtual qreal weight(qreal start, qreal end, qreal value) const
    {
        qreal mid = (start+end) / 2;
        qreal rate = 6 / (end - start);
        return FzMath::logistic(value, mid, 0, 1, rate);
    }

    virtual QVector<qreal> values(qreal start, qreal end, qreal weight) const
    {
        QVector<qreal> vals;

        qreal mid = (end + start) / 2;
       vals << FzMath::inverseLogistic(weight, mid);

        return vals;
    };
};

#endif // FZSIGMOIDSHAPE_H
