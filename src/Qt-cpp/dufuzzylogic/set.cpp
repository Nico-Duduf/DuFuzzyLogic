#include "set.h"

#include <QVariantAnimation>

#include "math.h"
#include "veracity.h"
#include "value.h"
#include "shapes/abstractshape.h"

FzL::Set::Set():
    _name("Empty"),
    _shapeIn(nullptr),
    _shapeOut(nullptr)
{ }

FzL::Set::Set(const QString &name,
                       AbstractShape *shapeIn,
                       AbstractShape *shapeOut
                       ):
    _name(name),
    _shapeIn(shapeIn),
    _shapeOut(shapeOut)
{ }

FzL::Set::~Set()
{
    delete _shapeIn;
    delete _shapeOut;
}

FzL::Veracity FzL::Set::contains(Value &value) const
{
    if (!isValid())
        return false;

    return contains(value.crisp());
}

FzL::Veracity FzL::Set::contains(const QVariant &value) const
{
    if (!isValid())
        return false;

    qreal inWeight = _shapeIn->weight(value);
    if (inWeight < 1) return inWeight;
    qreal outWeight = _shapeOut->weight(value);
    return outWeight;
}

QVector<QVariant> FzL::Set::values(const Veracity &veracity) const
{
    if (!isValid())
        return QVector<QVariant>();

    qreal w = veracity.value();

    QVector<QVariant> values = _shapeIn->values(w);

    if (w >= 1 ||
        (_shapeIn->type() == AbstractShape::Constant && _shapeOut->type() == AbstractShape::Constant)
       )
        values <<  Math::mean(_shapeIn->end(), _shapeOut->start());

    values << _shapeOut->values(w);

    return values;
}
