class FuzzyQuantifier:
    """! Enum of available quantifiers. """

    ## This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
    IS_NOT = "Not",
    ## This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
    LESS = "Less",
    ## Slightly
    DOUBLE_MINUS = "Slightly",
    ## Somewhat
    MINUS = "Somewhat",
    ## Moderately
    AVERAGE = "Moderately",
    ## None
    NONE = "",
    ## Very
    PLUS = "Very",
    ## Extremely
    DOUBLE_PLUS = "Extremely",
    ## This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
    IS = "Completely",
    ## This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
    MORE = "More"

    FuzzyQuantifierList = {
        IS_NOT: "Not", LESS: "Less", DOUBLE_MINUS: "Slightly", MINUS: "Somewhat", AVERAGE: "Moderately",
        NONE: "", PLUS: "Very", DOUBLE_PLUS: "Extremely", IS: "Completely", MORE: "More"
    }


class FuzzyShape():
    """! Enum of the shapes used as member functions of {@link FuzzySet}. """

    ## The set has no boundary on the constant side, every value is in the set on this side.
    CONSTANT = "constant",
    ## There's no transition on the square side, the value is either in (1) or out (0) of the set.
    SQUARE = "square",
    ## The transition is linear.
    LINEAR = "linear",
    ## The transition is a sigmoid (i.e. S-Shape, smooth), using the logistic standard function.
    SIGMOID = "sigmoid",
    ## Alias for {@link FuzzyShape.SIGMOID}
    SMOOTH = "sigmoid",
    ## The transition has a "bell" shape, using the gaussian function.
    BELL = "gaussian",
    ## Alias for {@link FuzzyShape.GAUSSIAN}
    GAUSSIAN = "gaussian",
    ## The transition has a "reversed bell" shape, using the gaussian function.
    REVERSED_BELL = "reversed_gaussian",
    ## Alias for {@link FuzzyShape.REVERSED_GAUSSIAN}
    REVERSED_GAUSSIAN = "reversed_gaussian"


class FuzzyLogicAlgorithm():
    """! Enum of the algorithms to use in the {@link FuzzyLogic} engine. """

    ## Uses Zadeh's method, resulting in a linear logic.
    LINEAR = 0,
    ## Uses Hyperbolic Parabloid logic, which is a bit heavier than linear, but may have more intuitive results.
    HYPERBOLIC = 1


class FuzzyCrispAlgorithm():
    """! Enum of the algorithms to use when crispifying values. """

    ## Uses the centroid method: combines all sets and values and gets the centroid.
    ## This method works great to combine more than a couple of rules, but will not work with single rules.
    CENTROID = 0,
    ## When several values are possible from each set, prefer the lowest one, then combine them to get the
    ## centroid. This method works like the centroid and works well even with single rules, but the returned
    ## values will tend to be a bit lower.
    CENTROID_LOWER = 1,
    ## When several values are possible from each set, prefer the highest one, then combine them to get the centroid.
    ## This method works like the centroid and works well even with single rules, but the returned values will tend to
    ## be a bit higher.
    CENTROID_HIGHER = 2,
    ## NOT IMPLEMENTED YET
    ## Returns a randomly chosen value from all possible values.
    RANDOM = 3,
    ## NOT IMPLEMENTED YET
    ## Returns a randomly chosen value from all possible values from the set with the highest veracity.
    RANDOM_TRUE = 4,
    ## NOT IMPLEMENTED YET
    ## Returns a single random value from each set then combines them to get the centroid.
    RANDOM_CENTROID = 5,
    ## Returns the mean value from all possible values from all the sets.
    ## Unlike the centroid methods, the mean method does not take the veracity of each set into account.
    MEAN = 6,
    ## Returns the mean value from all the highest possible values from all the sets.
    ## Unlike the centroid methods, the mean method does not take the veracity of each set into account.
    MEAN_HIGHER = 7,
    ## Returns the mean value from all the lowest possible values from all the sets.
    ## Unlike the centroid methods, the mean method does not take the veracity of each set into account.
    MEAN_LOWER = 8
