#ifndef CONSTANTSHAPE_H
#define CONSTANTSHAPE_H

#include "abstractshape.h"

namespace FzL
{

class ConstantShape : public AbstractShape
{
public:
    ConstantShape(const QVariant &v):
        AbstractShape(v, v, Constant) {};

protected:
    virtual qreal weight(qreal start, qreal end, qreal value) const
    {
        if (start <= end) {
            return value >= start;
        }

        return value <= start;
    }

    virtual QVector<qreal> values(qreal start, qreal end, qreal weight) const
    {
        QVector<qreal> vals;
        if (weight >= 1)
            vals << start;

        return vals;
    };
};

}

#endif // CONSTANTSHAPE_H
