#include "fzset.h"

#include <QVariantAnimation>

#include "fzmath.h"
#include "fzveracity.h"
#include "fzvalue.h"
#include "shapes/fzabstractshape.h"

FzSet::FzSet():
    _name("Empty"),
    _shapeIn(nullptr),
    _shapeOut(nullptr)
{ }

FzSet::FzSet(const QString &name,
                       FzAbstractShape *shapeIn,
                       FzAbstractShape *shapeOut
                       ):
    _name(name),
    _shapeIn(shapeIn),
    _shapeOut(shapeOut)
{ }

FzSet::~FzSet()
{
    // delete _shapeIn;
    // delete _shapeOut;
}

FzVeracity FzSet::contains(FzValue &value) const
{
    if (!isValid())
        return false;

    return contains(value.crisp());
}

FzVeracity FzSet::contains(const QVariant &value) const
{
    if (!isValid())
        return false;

    qreal inWeight = _shapeIn->weight(value);
    if (inWeight < 1) return inWeight;
    qreal outWeight = _shapeOut->weight(value);
    return outWeight;
}

QVector<QVariant> FzSet::values(const FzVeracity &veracity) const
{
    if (!isValid())
        return QVector<QVariant>();

    qreal w = veracity.value();

    QVector<QVariant> values = _shapeIn->values(w);

    if (w >= 1 ||
        (_shapeIn->type() == FzAbstractShape::Constant && _shapeOut->type() == FzAbstractShape::Constant)
       )
        values <<  FzMath::mean(_shapeIn->end(), _shapeOut->start());

    values << _shapeOut->values(w);

    return values;
}
