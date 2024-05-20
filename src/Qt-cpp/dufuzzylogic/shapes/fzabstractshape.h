#ifndef ABSTRACTSHAPE_H
#define ABSTRACTSHAPE_H

#include <QVariant>
#include <QLine>
#include <QSize>
#include <QRect>
#include <QColor>
#include <cmath>

namespace FzL
{
class AbstractShape
{
public:

    enum Type {
        Constant,
        Square,
        Linear,
        Gaussian,
        ReversedGaussian,
        Sigmoid
    };

    AbstractShape(const QVariant &startValue, const QVariant &endValue, Type type):
        _start(startValue), _end(endValue), _type(type) {

        // Make sure we can handle the value
        Q_ASSERT(_start.type() == _end.type());

        auto t = static_cast<QMetaType::Type>(_start.type());
        Q_ASSERT(t == QMetaType::Int ||
                 t == QMetaType::UInt ||
                 t == QMetaType::Double ||
                 t == QMetaType::Float ||
                 t == QMetaType::QLine ||
                 t == QMetaType::QLineF ||
                 t == QMetaType::QPoint ||
                 t == QMetaType::QPointF ||
                 t == QMetaType::QSize ||
                 t == QMetaType::QSizeF ||
                 t == QMetaType::QRect ||
                 t == QMetaType::QRectF ||
                 t == QMetaType::QColor);
          };
    virtual ~AbstractShape() {};

    QVariant start() const { return _start; };
    QVariant end() const { return _end; };
    Type type() const { return _type; };

    qreal weight(const QVariant &value) const {

        qreal w = 0;

        auto t = static_cast<QMetaType::Type>(value.type());
        switch(t) {
        case QMetaType::Int:
        case QMetaType::UInt:
            w = weight(_start.toInt(), _end.toInt(), value.toInt());
            break;
        case QMetaType::Double:
        case QMetaType::Float:
            w = weight(_start.toDouble(), _end.toDouble(), value.toDouble());
            break;
        case QMetaType::QLine: {
            QLine st = _start.toLine();
            QLine e = _end.toLine();
            QLine v = value.toLine();
            qreal p1 = weight(st.p1(), e.p1(), v.p1());
            qreal p2 = weight(st.p2(), e.p2(), v.p2());
            w = (p1+p2)/2;
            break;
        }
        case QMetaType::QLineF: {
            QLineF st = _start.toLineF();
            QLineF e = _end.toLineF();
            QLineF v = value.toLineF();
            qreal p1 = weight(st.p1(), e.p1(), v.p1());
            qreal p2 = weight(st.p2(), e.p2(), v.p2());
            w = (p1+p2)/2;
            break;
        }
        case QMetaType::QPoint:
            w = weight(_start.toPoint(), _end.toPoint(), value.toPoint());
            break;
        case QMetaType::QPointF:
            w = weight(_start.toPointF(), _end.toPointF(), value.toPointF());
            break;
        case QMetaType::QSize:
            w = weight(_start.toSize(), _end.toSize(), value.toSize());
            break;
        case QMetaType::QSizeF:
            w = weight(_start.toSizeF(), _end.toSizeF(), value.toSizeF());
            break;
        case QMetaType::QRect: {
            QRect s = _start.toRect();
            QRect e = _end.toRect();
            QRect v = value.toRect();
            qreal tl = weight(s.topLeft(), e.topLeft(), v.topLeft());
            qreal sz = weight(s.size(), e.size(), v.size());
            w = (tl+sz)/2;
            break;
        }
        case QMetaType::QRectF: {
            QRectF s = _start.toRectF();
            QRectF e = _end.toRectF();
            QRectF v = value.toRectF();
            qreal tl = weight(s.topLeft(), e.topLeft(), v.topLeft());
            qreal sz = weight(s.size(), e.size(), v.size());
            w = (tl+sz)/2;
            break;
        }
        case QMetaType::QColor:  {
            QColor s = _start.value<QColor>();
            QColor e = _end.value<QColor>();
            QColor v = value.value<QColor>();
            qreal r = weight(s.redF(), e.redF(), v.redF());
            qreal g = weight(s.greenF(), e.greenF(), v.greenF());
            qreal b = weight(s.blueF(), e.blueF(), v.blueF());
            qreal a = weight(s.alphaF(), e.alphaF(), v.alphaF());
            w = (r+g+b+a) / 4;
            break;
        }
        default:
            break;
        };

        w = std::fmin(1, w);
        w = std::fmax(0, w);
        return w;
    }

    QVector<QVariant> values(qreal weight) const {
        QVector<QVariant> vals;
        if (weight <= 0) return vals;

        auto t = static_cast<QMetaType::Type>(_start.type());
        switch(t) {
        case QMetaType::Int:
        case QMetaType::UInt: {
            const auto vs = values(_start.toInt(), _end.toInt(), weight);
            for (const auto v: vs)
                vals << v;
            return vals;
        }
        case QMetaType::Double:
        case QMetaType::Float: {
            const auto vs = values(_start.toDouble(), _end.toDouble(), weight);
            for (const auto v: vs)
                vals << v;
            return vals;
        }
        case QMetaType::QLine: {
            QLine st = _start.toLine();
            QLine e = _end.toLine();
            const auto vp1 = values(st.p1(), e.p1(), weight);
            const auto vp2 = values(st.p2(), e.p2(), weight);
            QVector<QVariant> lines;
            for (int i =0; i < vp1.count(); ++i) {
                lines << QLine(vp1.at(i), vp2.at(i));
            }
            return lines;
        }
        case QMetaType::QLineF: {
            QLineF st = _start.toLine();
            QLineF e = _end.toLine();
            const auto vp1 = values(st.p1(), e.p1(), weight);
            const auto vp2 = values(st.p2(), e.p2(), weight);
            QVector<QVariant> lines;
            for (int i =0; i < vp1.count(); ++i) {
                lines << QLineF(vp1.at(i), vp2.at(i));
            }
            return lines;
        }
        case QMetaType::QPoint: {
            const auto vs = values(_start.toInt(), _end.toInt(), weight);
            for (const auto v: vs)
                vals << v;
            return vals;
        }
        case QMetaType::QPointF: {
            const auto vs = values(_start.toInt(), _end.toInt(), weight);
            for (const auto v: vs)
                vals << v;
            return vals;
        }
        case QMetaType::QSize: {
            QSize st = _start.toSize();
            QSize e = _end.toSize();
            const auto vp1 = values(st.width(), e.width(), weight);
            const auto vp2 = values(st.height(), e.height(), weight);
            QVector<QVariant> lines;
            for (int i =0; i < vp1.count(); ++i) {
                lines << QSize(vp1.at(i), vp2.at(i));
            }
            return lines;
        }
        case QMetaType::QSizeF: {
            QSizeF st = _start.toSize();
            QSizeF e = _end.toSize();
            const auto vp1 = values(st.width(), e.width(), weight);
            const auto vp2 = values(st.height(), e.height(), weight);
            QVector<QVariant> lines;
            for (int i =0; i < vp1.count(); ++i) {
                lines << QSizeF(vp1.at(i), vp2.at(i));
            }
            return lines;
        }
        case QMetaType::QRect: {
            QRect st = _start.toRect();
            QRect e = _end.toRect();
            const auto vp1 = values(st.topLeft(), e.topLeft(), weight);
            const auto vp2 = values(st.size(), e.size(), weight);
            QVector<QVariant> lines;
            for (int i =0; i < vp1.count(); ++i) {
                lines << QRect(vp1.at(i), vp2.at(i));
            }
            return lines;
        }
        case QMetaType::QRectF:  {
            QRectF st = _start.toRectF();
            QRectF e = _end.toRectF();
            const auto vp1 = values(st.topLeft(), e.topLeft(), weight);
            const auto vp2 = values(st.size(), e.size(), weight);
            QVector<QVariant> lines;
            for (int i =0; i < vp1.count(); ++i) {
                lines << QRectF(vp1.at(i), vp2.at(i));
            }
            return lines;
        }
        case QMetaType::QColor:  {
            QColor s = _start.value<QColor>();
            QColor e = _end.value<QColor>();
            const auto rs = values(s.redF(), e.redF(), weight);
            const auto gs = values(s.greenF(), e.greenF(), weight);
            const auto bs = values(s.blueF(), e.blueF(), weight);
            const auto as = values(s.alphaF(), e.alphaF(), weight);
            QVector<QVariant> colors;
            for (int i =0; i < rs.count(); ++i) {
                colors << QColor::fromRgbF(
                    rs.at(i),
                    gs.at(i),
                    bs.at(i),
                    as.at(i)
                    );
            }
            return colors;
        }
        default:
            break;
        };

        return QVector<QVariant>();
    }

protected:

    virtual qreal weight(qreal start, qreal end, qreal value) const = 0;

    virtual qreal weight(QPoint start, QPoint end, QPoint value) const {
        qreal x = weight(start.x(), end.x(), value.x());
        qreal y = weight(start.x(), end.x(), value.x());
        return (x+y)/2;
    }

    virtual qreal weight(QPointF start, QPointF end, QPointF value) const {
        qreal x = weight(start.x(), end.x(), value.x());
        qreal y = weight(start.x(), end.x(), value.x());
        return (x+y)/2;
    }

    virtual qreal weight(QSize start, QSize end, QSize value) const {
        qreal w = weight(start.width(), end.width(), value.width());
        qreal h = weight(start.height(), end.height(), value.height());
        return (w+h)/2;
    }

    virtual qreal weight(QSizeF start, QSizeF end, QSizeF value) const {
        qreal w = weight(start.width(), end.width(), value.width());
        qreal h = weight(start.height(), end.height(), value.height());
        return (w+h)/2;
    }

    virtual QVector<qreal> values(qreal start, qreal end, qreal weight) const = 0;

    virtual QVector<QPoint> values(QPoint start, QPoint end, qreal weight) const {
        const auto xs = values(start.x(), end.x(), weight);
        const auto ys = values(start.y(), end.y(), weight);
        QVector<QPoint> points;
        for (int i = 0; i < xs.count(); ++i) {
            points << QPoint(xs.at(i), ys.at(i));
        }
        return points;
    }

    virtual QVector<QPointF> values(QPointF start, QPointF end, qreal weight) const {
        const auto xs = values(start.x(), end.x(), weight);
        const auto ys = values(start.y(), end.y(), weight);
        QVector<QPointF> points;
        for (int i = 0; i < xs.count(); ++i) {
            points << QPointF(xs.at(i), ys.at(i));
        }
        return points;
    }

    virtual QVector<QSize> values(QSize start, QSize end, qreal weight) const {
        const auto xs = values(start.width(), end.width(), weight);
        const auto ys = values(start.height(), end.height(), weight);
        QVector<QSize> points;
        for (int i = 0; i < xs.count(); ++i) {
            points << QSize(xs.at(i), ys.at(i));
        }
        return points;
    }

    virtual QVector<QSizeF> values(QSizeF start, QSizeF end, qreal weight) const {
        const auto xs = values(start.width(), end.width(), weight);
        const auto ys = values(start.height(), end.height(), weight);
        QVector<QSizeF> points;
        for (int i = 0; i < xs.count(); ++i) {
            points << QSizeF(xs.at(i), ys.at(i));
        }
        return points;
    }

private:
    QVariant _start;
    QVariant _end;
    Type _type;
};

}

#endif // ABSTRACTSHAPE_H
