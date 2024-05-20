#ifndef FZCONSTANTSHAPE_H
#define FZCONSTANTSHAPE_H

#include "fzabstractshape.h"

class FzConstantShape : public FzAbstractShape
{
public:
    FzConstantShape(const QVariant &v):
        FzAbstractShape(v, v, Constant) {};

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

#endif // FZCONSTANTSHAPE_H
