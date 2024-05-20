#ifndef LINEARSHAPE_H
#define LINEARSHAPE_H

#include "abstractshape.h"

namespace FzL
{

class LinearShape : public AbstractShape
{
public:
    LinearShape(const QVariant &start, const QVariant &end):
        AbstractShape(start, end, Linear) {};

protected:
    virtual qreal weight(qreal start, qreal end, qreal value) const
    {
        if (start == end){
            if (value == start)
                return 1;
            return 0;
        }

        // Reorder
        if (start > end) {
            qreal temp = start;
            start = end;
            end = temp;
        }

        // Trivial
        if (value <= start) return 0;
        if (value >= end) return 1;

        return (value - start) / (end - start);
    }

    virtual QVector<qreal> values(qreal start, qreal end, qreal weight) const
    {
        QVector<qreal> vals;

        qreal range = end - start;
        vals << start + range * weight;

        return vals;
    };
};

}

#endif // LINEARSHAPE_H
