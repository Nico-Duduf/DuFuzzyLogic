#ifndef SIGMOIDSHAPE_H
#define SIGMOIDSHAPE_H

#include "abstractshape.h"
#include "math.h"

namespace FzL
{

class SigmoidShape : public AbstractShape
{
public:
    SigmoidShape(const QVariant &start, const QVariant &end):
        AbstractShape(start, end, Sigmoid) {};

protected:
    virtual qreal weight(qreal start, qreal end, qreal value) const
    {
        qreal mid = (start+end) / 2;
        qreal rate = 6 / (end - start);
        return Math::logistic(value, mid, 0, 1, rate);
    }

    virtual QVector<qreal> values(qreal start, qreal end, qreal weight) const
    {
        QVector<qreal> vals;

        qreal mid = (end + start) / 2;
       vals << Math::inverseLogistic(weight, mid);

        return vals;
    };
};

}
#endif // SIGMOIDSHAPE_H
