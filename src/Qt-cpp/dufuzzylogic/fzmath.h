#ifndef MATH_H
#define MATH_H

#include <cmath>

#include "qglobal.h"
#include <QVariant>

namespace FzL
{

    namespace Math
    {
        inline constexpr qreal logistic(qreal value, qreal midValue = 0, qreal min = 0, qreal max = 1, qreal rate = 1)
        {
            qreal exp = - rate * (value - midValue);
            qreal result = 1 / (1 + std::exp(exp));
            return result * (max-min) + min;
        }

        /**
            * The inverse logistic function (inverse sigmoid)
            * @param {Number} v The variable
            * @param {Number} [midValue=0] The midpoint value, at which the function returns max/2 in the original logistic function
            * @param {Number} [min=0] The minimum return value of the original logistic function
            * @param {Number} [max=1] The maximum return value of the original logistic function
            * @param {Number} [rate=1] The logistic growth rate or steepness of the original logistic function
            * @return {Number} The result
            */
        inline constexpr qreal inverseLogistic( qreal v, qreal midValue = 0, qreal min = 0, qreal max = 1, qreal rate = 1)
        {
            if (v == min) return 0;

            return midValue - std::log( (max-min)/(v-min) - 1) / rate;
        }


        /**
            * The inverse gaussian function
            * @param {Number} v The variable
            * @param {Number} [min=0] The minimum return value of the corresponding gaussian function
            * @param {Number} [max=1] The maximum return value of the corresponding gaussian function
            * @param {Number} [center=0] The center of the peak of the corresponding gaussian function
            * @param {Number} [fwhm=1] The full width at half maximum of the curve of the corresponding gaussian function
            * @return {Number[]} The two possible results, the lower is the first in the list. If both are the same, it is the maximum
            */
        inline QVector<qreal> inverseGaussian( qreal v, qreal min = 0, qreal max = 1, qreal center = 0, qreal fwhm = 1)
        {
            if (v == 1) return {center, center};
            if (v == 0) return {center + fwhm/2, center - fwhm/2};
            if (fwhm == 0) return {center, center};

            qreal result = (v-min)/(max-min);
            result = std::log( result ) * std::pow(fwhm,2);
            result = result / ( -4 * std::log(2) );
            result = std::sqrt( result );
            return { result + center, -result + center };
        }

        inline constexpr qreal gaussian(qreal value, qreal min = 0, qreal max = 1, qreal center = 0, qreal fwhm = 1)
        {
            if (fwhm == 0 && value == center) return max;
            else if (fwhm == 0) return 0;

            qreal exp = -4 * std::log(2);
            exp *= std::pow((value - center),2);
            exp *= 1/ std::pow(fwhm, 2);
            qreal result = std::exp(exp);
            return result * (max-min) + min;
        }

        inline constexpr qreal reversedGaussian(qreal value, qreal min = 0, qreal max = 1, qreal center = 0, qreal fwhm = 1)
        {
            qreal r = -value-fwhm+1;
            return gaussian( value, min, max, center, r);
        }


        /**
            * The inverse of the reversed gaussian function
            * @param {Number} value The variable
            * @param {Number} [min=0] The minimum return value of the corresponding gaussian function
            * @param {Number} [max=1] The maximum return value of the corresponding gaussian function
            * @param {Number} [center=0] The center of the peak of the corresponding gaussian function
            * @param {Number} [fwhm=1] The full width at half maximum of the curve of the corresponding gaussian function
            * @return {Number[]} The two possible results, the lower is the first in the list. If both are the same, it is the maximum
            */
        inline QVector<qreal> inverseReversedGaussian(qreal value, qreal min = 0, qreal max = 1, qreal center = 0, qreal fwhm  = 1)
        {
            qreal r = -value-fwhm+1;
            return inverseGaussian( value, min, max, center, r);
        }


        /**
         * @brief mean Calculates a mean value between the two QVariants
         * @param a
         * @param b
         * @return
         */
        QVariant mean(const QVariant &a, const QVariant &b);

        /**
         * @brief mean Calculate a mean value from a list of values
         * @param values
         * @param curve
         * @return
         */
        QVariant mean(const QVector<QVariant> values);

    }

    // Useful operators for some QVariant numeric types (the ones handled by DuFuzzyLogic)

    QVariant operator*(const QVariant &value, qreal w);
    QVariant operator+(const QVariant &a, const QVariant &b);
    QVariant operator/(const QVariant &a, qreal w);

}
#endif // MATH_H
