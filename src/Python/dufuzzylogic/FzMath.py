import math

# ====== SOME MATH FUNCTIONS =========

"""
Some general purpose Math functions
 @namespace
 """
FzMath = {}


def logistic(value, midValue=0, minimum=0, maximum=1, rate=1):
    """
    The logistic function (sigmoid)
    :param value: {Number} value The value
    :param midValue: {Number} [midValue=0] The midpoint value, at which the function returns maximum/2
    :param minimum: {Number} [minimum=0] The minimum return value
    :param maximum: {Number} [maximum=1] The maximum return value
    :param rate: {Number} [rate=1] The logistic growth rate or steepness of the function
    :return: {Number} The result in the range [minimum, maximum] (excluding minimum and maximum)
    """
    exp = -rate * (value - midValue)
    result = 1 / (1 + math.pow(math.e, exp))
    return result * (maximum - minimum) + minimum


def inverseLogistic(value, midValue=0, minimum=0, maximum=1, rate=1):
    """
    The inverse logistic function (inverse sigmoid)
    :param value: {Number} The value
    :param midValue: {Number} [midValue=0] The midpoint value, at which the function returns maximum/2 in the original logistic function
    :param minimum: {Number} [minimum=0] The minimum return value of the original logistic function
    :param maximum: {Number} [maximum=1] The maximum return value of the original logistic function
    :param rate: {Number} [rate=1] The logistic growth rate or steepness of the original logistic function
    :return: {Number} The result
    """
    if value == minimum:
        return 0

    return midValue - math.log((maximum - minimum) / (value - minimum) - 1) / rate


def gaussian(value, minimum=0, maximum=1, center=0, fwhm=1):
    """
    The gaussian function
    :param value: {Number} The value
    :param minimum: {Number} [minimum=0] The minimum return value
    :param maximum: {Number} [maximum=1] The maximum return value
    :param center: {Number} [center=0] The center of the peak
    :param fwhm: {Number} [fwhm=1] The full width at half maximum of the curve
    :return: {Number} The result
    """
    if fwhm == 0 and value == center:
        return maximum
    elif fwhm == 0:
        return 0

    exp = -4 * math.log(2)
    exp *= math.pow((value - center), 2)
    exp *= 1 / math.pow(fwhm, 2)
    result = math.pow(math.e, exp)
    return result * (maximum - minimum) + minimum


def reversedGaussian(value, minimum, maximum, center, fwhm):
    """
    A "reversed" gaussian function, growing faster with low value
    :param value: {Number} value The value
    :param minimum: {Number} [minimum=0] The minimum return value
    :param maximum: {Number} [maximum=1] The maximum return value
    :param center: {Number} [center=0] The center of the peak
    :param fwhm: {Number} [fwhm=1] The full width at half maximum of the curve
    :return: {Number} The result
    """
    r = - value - fwhm + 1
    return gaussian(value, minimum, maximum, center, r)


def inverseGaussian(value, minimum=0, maximum=1, center=0, fwhm=1):
    """
    The inverse gaussian function
    :param value: The value
    :param minimum: {Number} [minimum=0] The minimum return value of the corresponding gaussian function
    :param maximum: {Number} [maximum=1] The maximum return value of the corresponding gaussian function
    :param center: {Number} [center=0] The center of the peak of the corresponding gaussian function
    :param fwhm: {Number} [fwhm=1] The full width at half maximum of the curve of the corresponding gaussian function
    :return: {Number[]} The two possible results, the lower is the first in the list. If both are the same, it is the maximum
    """
    if value == 1:
        return [center, center]
    if value == 0:
        return [center + fwhm / 2, center - fwhm / 2]
    if fwhm == 0:
        return [center, center]

    result = (value - minimum) / (maximum - minimum)
    result = math.log(result) * math.pow(fwhm, 2)
    result = result / (-4 * math.log(2))
    result = math.sqrt(result)
    return [result + center, -result + center]


def inverseReversedGaussian(value, minimum, maximum, center, fwhm):
    """
    The inverse of the reversed gaussian function
    :param value: {Number} The value
    :param minimum: {Number} [minimum=0] The minimum return value of the corresponding gaussian function
    :param maximum: {Number} [maximum=1] The maximum return value of the corresponding gaussian function
    :param center: {Number} [center=0] The center of the peak of the corresponding gaussian function
    :param fwhm: {Number} [fwhm=1] The full width at half maximum of the curve of the corresponding gaussian function
    :return: {Number[]} The two possible results, the lower is the first in the list. If both are the same, it is the maximum
    """
    r = - value - fwhm + 1
    return inverseGaussian(value, minimum, maximum, center, r)


def mean(values):
    """
    Returns the mean of a set of values
    :param values: {Number[]} The values
    :return: {Number} The mean
    """
    num = len(values)
    result = 0
    for i in range(0, num):
        result += values[i]
    return result / num
