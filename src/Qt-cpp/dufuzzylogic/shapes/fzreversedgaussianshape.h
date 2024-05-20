#ifndef FZREVERSEDGAUSSIANSHAPE_H
#define FZREVERSEDGAUSSIANSHAPE_H

#include "fzabstractshape.h"
#include "fzmath.h"

class FzReversedGaussianShape : public FzAbstractShape
{
public:
    FzReversedGaussianShape(const QVariant &start, const QVariant &end):
        FzAbstractShape(start, end, ReversedGaussian) {};

protected:
    virtual qreal weight(qreal start, qreal end, qreal value) const
    {
        qreal width = end - start;
        if (end > start)
            return FzMath::reversedGaussian( value, 0, 1, end, width);
        return FzMath::reversedGaussian( value, 0, 1, start, width);
    }

    virtual QVector<qreal> values(qreal start, qreal end, qreal weight) const
    {
        QVector<qreal> vals;

        if (end > start) {
            qreal width = end - start;
            const auto g = FzMath::inverseReversedGaussian( weight, 0, 1, end, width);
            vals << g.first();
        }
        else {
            qreal width = start - end;
            const auto g = FzMath::inverseReversedGaussian( 1-weight, 0, 1, start, width);
            vals << g.last();
        }

        return vals;
    };
};

#endif // FZREVERSEDGAUSSIANSHAPE_H
