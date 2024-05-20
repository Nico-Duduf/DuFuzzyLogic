#ifndef SQUARESHAPE_H
#define SQUARESHAPE_H

#include "abstractshape.h"

namespace FzL
{

class SquareShape : public AbstractShape
{
public:
    SquareShape(const QVariant &start, const QVariant &end):
        AbstractShape(start, end, Square) {};

protected:
    virtual qreal weight(qreal start, qreal end, qreal value) const
    {
        qreal mid = (start+end)/2;

        if (start <= end) {
            return value >= mid;
        }

        return value <= mid;
    }

    virtual QVector<qreal> values(qreal start, qreal end, qreal weight) const
    {
        QVector<qreal> vals;

        if (weight >= 0.5) {
            vals << end;
        }
        if (weight <= 0.5) {
            vals << start;
        }

        return vals;
    };
};

}

#endif // SQUARESHAPE_H
