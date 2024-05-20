#ifndef REVERSEDGAUSSIANSHAPE_H
#define REVERSEDGAUSSIANSHAPE_H

#include "abstractshape.h"
#include "math.h"

namespace FzL
{

class ReversedGaussianShape : public AbstractShape
{
public:
    ReversedGaussianShape(const QVariant &start, const QVariant &end):
        AbstractShape(start, end, ReversedGaussian) {};

protected:
    virtual qreal weight(qreal start, qreal end, qreal value) const
    {
        qreal width = end - start;
        if (end > start)
            return Math::reversedGaussian( value, 0, 1, end, width);
        return Math::reversedGaussian( value, 0, 1, start, width);
    }

    virtual QVector<qreal> values(qreal start, qreal end, qreal weight) const
    {
        QVector<qreal> vals;

        if (end > start) {
            qreal width = end - start;
            const auto g = Math::inverseReversedGaussian( weight, 0, 1, end, width);
            vals << g.first();
        }
        else {
            qreal width = start - end;
            const auto g = Math::inverseReversedGaussian( 1-weight, 0, 1, start, width);
            vals << g.last();
        }

        return vals;
    };
};

}

#endif // REVERSEDGAUSSIANSHAPE_H
