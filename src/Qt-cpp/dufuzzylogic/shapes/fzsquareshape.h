#ifndef FZSQUARESHAPE_H
#define FZSQUARESHAPE_H

#include "fzabstractshape.h"

class FzSquareShape : public FzAbstractShape
{
public:
    FzSquareShape(const QVariant &start, const QVariant &end):
        FzAbstractShape(start, end, Square) {};

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

#endif // FZSQUARESHAPE_H
