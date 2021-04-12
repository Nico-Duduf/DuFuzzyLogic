import math

# ====== SOME MATH FUNCTIONS =========

"""
Some general purpose Math functions
 @namespace
 """
FzMath = {}


def logistic(value, midValue = 0, min = 0, max = 1, rate = 1):
    """
    The logistic function (sigmoid)
    :param value: {Number} value The value
    :param midValue: {Number} [midValue=0] The midpoint value, at which the function returns max/2
    :param min: {Number} [min=0] The minimum return value
    :param max: {Number} [max=1] The maximum return value
    :param rate: {Number} [rate=1] The logistic growth rate or steepness of the function
    :return: {Number} The result in the range [min, max] (excluding min and max)
    """
    exp = -rate * (value - midValue)
    result = 1 / (1 + math.pow(math.e, exp))
    return result * (max - min) + min


def inverseLogistic(v, midValue, min, max, rate):
    """
    The inverse logistic function (inverse sigmoid)
    :param v: {Number} v The variable
    :param midValue: {Number} [midValue=0] The midpoint value, at which the function returns max/2 in the original logistic function
    :param min: {Number} [min=0] The minimum return value of the original logistic function
    :param max: {Number} [max=1] The maximum return value of the original logistic function
    :param rate: {Number} [rate=1] The logistic growth rate or steepness of the original logistic function
    :return: {Number} The result
    """
    midValue = midValue or 0
    max = max or 1
    min = min or 0
    rate = rate or 1

    if v == min:
        return 0

    return midValue - math.log((max - min) / (v - min) - 1) / rate


def gaussian(value, min, max, center, fwhm):
    """
    The gaussian function
    :param value: {Number} value The variable
    :param min: {Number} [min=0] The minimum return value
    :param max: {Number} [max=1] The maximum return value
    :param center: {Number} [center=0] The center of the peak
    :param fwhm: {Number} [fwhm=1] The full width at half maximum of the curve
    :return: {Number} The result
    """
    max = max or 1
    min = min or 0
    center = center or 0
    fwhm = fwhm or 1

    if fwhm == 0 & value == center:
        return max
    elif fwhm == 0:
        return 0

    exp = -4 * math.log(2)
    exp *= math.pow((value - center), 2)
    exp *= 1 / math.pow(fwhm, 2)
    result = math.pow(math.e, exp)
    return result * (max - min) + min


def reversedGaussian(value, min, max, center, fwhm):
    """
    A "reversed" gaussian function, growing faster with low value
    :param value: {Number} value The variable
    :param min: {Number} [min=0] The minimum return value
    :param max: {Number} [max=1] The maximum return value
    :param center: {Number} [center=0] The center of the peak
    :param fwhm: {Number} [fwhm=1] The full width at half maximum of the curve
    :return: {Number} The result
    """
    r = -value - fwhm + 1
    return gaussian(value, min, max, center, r)


def inverseGaussian(v, min, max, center, fwhm):
    """
    The inverse gaussian function
    :param v: v The variable
    :param min: {Number} [min=0] The minimum return value of the corresponding gaussian function
    :param max: {Number} [max=1] The maximum return value of the corresponding gaussian function
    :param center: {Number} [center=0] The center of the peak of the corresponding gaussian function
    :param fwhm: {Number} [fwhm=1] The full width at half maximum of the curve of the corresponding gaussian function
    :return: {Number[]} The two possible results, the lower is the first in the list. If both are the same, it is the maximum
    """
    max = max or 1
    min = min or 0
    center = center or 0
    fwhm = fwhm or 1
    if v == 1:
        return [center, center]
    if v == 0:
        return [center + fwhm / 2, center - fwhm / 2]
    if fwhm == 0:
        return [center, center]

    result = (v - min) / (max - min)
    result = math.log(result) * math.pow(fwhm, 2)
    result = result / (-4 * math.log(2))
    result = math.sqrt(result)
    return [result + center, -result + center]


def inverseReversedGaussian(value, min, max, center, fwhm):  # remplace v par value (ligne 125 en js)
    """
    The inverse of the reversed gaussian function
    :param value: {Number} v The variable
    :param min: {Number} [min=0] The minimum return value of the corresponding gaussian function
    :param max: {Number} [max=1] The maximum return value of the corresponding gaussian function
    :param center: {Number} [center=0] The center of the peak of the corresponding gaussian function
    :param fwhm: {Number} [fwhm=1] The full width at half maximum of the curve of the corresponding gaussian function
    :return: {Number[]} The two possible results, the lower is the first in the list. If both are the same, it is the maximum
    """
    r = -value - fwhm + 1
    return inverseGaussian(value, min, max, center, r)


def mean(values):
    """
    Returns the mean of a set of values
    :param values: {Number[]} values The values
    :return: {Number} The mean
    """
    num = len(values)
    result = 0
    for i in range(0, num):
        result += values[i]
    return result / num


