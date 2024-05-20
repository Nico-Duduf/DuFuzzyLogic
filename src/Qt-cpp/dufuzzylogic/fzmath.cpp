#include "fzmath.h"

#include <QVariantAnimation>
#include <QLine>
#include <QSize>
#include <QRect>
#include <QColor>

QVariant FzMath::mean(const QVariant &a, const QVariant &b)
{
    return mean({a, b});
}

QVariant FzMath::mean(const QVector<QVariant> values)
{
    auto t = static_cast<QMetaType::Type>(values.constFirst().type());
    QVariant sum;

    // We need to keep the alpha of colors
    // as it's clamped in QColor
    qreal colorA = 0;

    for (const auto &value: values) {
        switch(t) {
        case QMetaType::Int:
            sum = sum.toInt() + value.toInt();
            break;
        case QMetaType::UInt:
            sum = sum.toUInt() + value.toUInt();
            break;
        case QMetaType::Double:
            sum = sum.toDouble() + value.toDouble();
            break;
        case QMetaType::Float:
            sum = sum.toFloat() + value.toFloat();
            break;
        case QMetaType::QLine: {
            QLine a = sum.toLine();
            QLine b = value.toLine();
            sum = QLine(a.p1() + b.p1(), a.p2() + b.p2());
            break;
        }
        case QMetaType::QLineF: {
            QLineF a = sum.toLineF();
            QLineF b = value.toLineF();
            sum = QLineF(a.p1() + b.p1(), a.p2() + b.p2());
            break;
        }
        case QMetaType::QPoint:
            sum = sum.toPoint() + value.toPoint();
            break;
        case QMetaType::QPointF:
            sum = sum.toPointF() + value.toPointF();
            break;
        case QMetaType::QSize:
            sum = sum.toSize() + value.toSize();
            break;
        case QMetaType::QSizeF:
            sum = sum.toSizeF() + value.toSizeF();
            break;
        case QMetaType::QRect: {
            QRect a = sum.toRect();
            QRect b = value.toRect();
            sum = QRect(a.topLeft() + b.topLeft(), a.size() + b.size());
            break;
        }
        case QMetaType::QRectF: {
            QRectF a = sum.toRect();
            QRectF b = value.toRect();
            sum = QRectF(a.topLeft() + b.topLeft(), a.size() + b.size());
            break;
        }
        case QMetaType::QColor:  {
            QColor a = sum.value<QColor>();
            QColor b = value.value<QColor>();
            sum = QColor::fromRgbF(
                a.redF() + b.redF(),
                a.greenF() + b.greenF(),
                a.blueF() + b.blueF()
                );
            colorA += b.alphaF();
            break;
        }
        default:
            break;
        };
    }

    switch(t) {
    case QMetaType::Int:
        return sum.toInt() / values.count();
    case QMetaType::UInt:
        return sum.toUInt() / values.count();
    case QMetaType::Double:
        return sum.toDouble() / double(values.count());
    case QMetaType::Float:
        return sum.toFloat() / float(values.count());
    case QMetaType::QLine: {
        QLine l = sum.toLine();
        int c = values.count();
        return QLine(l.p1() / c, l.p2() / c);
    }
    case QMetaType::QLineF: {
        QLineF l = sum.toLineF();
        int c = values.count();
        return QLineF(l.p1() / c, l.p2() / c);
    }
    case QMetaType::QPoint:
        return sum.toPoint() / values.count();
    case QMetaType::QPointF:
        return sum.toPointF() / values.count();
    case QMetaType::QSize:
        return sum.toSize() / values.count();
    case QMetaType::QSizeF:
        return sum.toSizeF() / values.count();
    case QMetaType::QRect: {
        QRect r = sum.toRect();
        int c = values.count();
        return QRect(r.topLeft() / c, r.size() / c);
    }
    case QMetaType::QRectF: {
        QRectF r = sum.toRect();
        int c = values.count();
        return QRectF(r.topLeft() / c, r.size() / c);
    }
    case QMetaType::QColor:  {
        QColor col = sum.value<QColor>();
        qreal c = values.count();
        return QColor::fromRgbF(
            col.redF() / c,
            col.greenF() / c,
            col.blueF() / c,
            colorA / c
            );
    }
    default:
        break;
    };

    return QVariant();
}

QVariant operator*(const QVariant &value, qreal w)
{
    auto t = static_cast<QMetaType::Type>(value.type());
    switch(t) {
    case QMetaType::Int:
        return value.toInt() * w;
    case QMetaType::UInt:
        return value.toUInt() * w;
    case QMetaType::Double:
        return value.toDouble() * w;
    case QMetaType::Float:
        return value.toFloat() * w;
    case QMetaType::QLine: {
        QLine l = value.toLine();
        return QLine(l.p1() * w, l.p2() * w);
    }
    case QMetaType::QLineF: {
        QLineF l = value.toLineF();
        return QLineF(l.p1() * w, l.p2() * w);
    }
    case QMetaType::QPoint:
        return value.toPoint() * w;
    case QMetaType::QPointF:
        return value.toPointF() * w;
    case QMetaType::QSize:
        return value.toSize() * w;
    case QMetaType::QSizeF:
        return value.toSizeF() * w;
    case QMetaType::QRect: {
        QRect r = value.toRect();
        return QRect(r.topLeft() * w, r.size() * w);
    }
    case QMetaType::QRectF: {
        QRectF r = value.toRect();
        return QRectF(r.topLeft() * w, r.size() * w);
    }
    case QMetaType::QColor:  {
        QColor col = value.value<QColor>();
        return QColor::fromRgbF(
            col.redF() * w,
            col.greenF() * w,
            col.blueF() * w,
            col.alphaF() * w
            );
    }
    default:
        break;
    };

    return QVariant();
}

QVariant operator+(const QVariant &a, const QVariant &b)
{
    auto t = static_cast<QMetaType::Type>(a.type());
    switch(t) {
    case QMetaType::Int:
        return a.toInt() + a.toInt();
    case QMetaType::UInt:
        return a.toUInt() + a.toUInt();
    case QMetaType::Double:
        return a.toDouble() + a.toDouble();
    case QMetaType::Float:
        return a.toFloat() + a.toFloat();
    case QMetaType::QLine: {
        QLine al = a.toLine();
        QLine bl = b.toLine();
        return QLine(al.p1() + bl.p1(), al.p2() + bl.p2());
    }
    case QMetaType::QLineF: {
        QLineF al = a.toLineF();
        QLineF bl = b.toLineF();
        return QLineF(al.p1() + bl.p1(), al.p2() + bl.p2());
    }
    case QMetaType::QPoint:
        return a.toPoint() + a.toPoint();
    case QMetaType::QPointF:
        return a.toPointF() + a.toPointF();
    case QMetaType::QSize:
        return a.toSize() + a.toSize();
    case QMetaType::QSizeF:
        return a.toSizeF() + a.toSizeF();
    case QMetaType::QRect: {
        QRect ar = a.toRect();
        QRect br = b.toRect();
        return QRect(ar.topLeft() + br.topLeft(), ar.size() + br.size());
    }
    case QMetaType::QRectF: {
        QRectF ar = a.toRectF();
        QRectF br = b.toRectF();
        return QRectF(ar.topLeft() + br.topLeft(), ar.size() + br.size());
    }
    case QMetaType::QColor:  {
        QColor acol = a.value<QColor>();
        QColor bcol = b.value<QColor>();
        return QColor::fromRgbF(
            acol.redF() + bcol.redF(),
            acol.greenF() + bcol.greenF(),
            acol.blueF() + bcol.blueF(),
            acol.alphaF() + bcol.alphaF()
            );
    }
    default:
        break;
    };

    return QVariant();
}

QVariant operator/(const QVariant &a, qreal w) {
    return a * (1/w);
}
