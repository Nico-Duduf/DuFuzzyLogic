#ifndef GAUSSIANSHAPE_H
#define GAUSSIANSHAPE_H

#include "abstractshape.h"
#include "math.h"

namespace FzL
{

class GaussianShape : public AbstractShape
{
public:
    GaussianShape(const QVariant &start, const QVariant &end):
        AbstractShape(start, end, Gaussian) {};

protected:
    virtual qreal weight(qreal start, qreal end, qreal value) const
    {
        qreal width = end - start;
        if (end > start)
            return Math::gaussian( value, 0, 1, end, width);
        return Math::gaussian( value, 0, 1, start, width);
    }

    virtual QVector<qreal> values(qreal start, qreal end, qreal weight) const
    {
        QVector<qreal> vals;

        if (end > start) {
            qreal width = end - start;
            const auto g = Math::inverseGaussian( weight, 0, 1, end, width);
            vals << g.first();
        }
        else {
            qreal width = start - end;
            const auto g = Math::inverseGaussian( weight, 0, 1, start, width);
            vals << g.last();
        }

        return vals;
    };
};

}
#endif // GAUSSIANSHAPE_H
