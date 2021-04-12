class Namespace:
    def __init__(self, **kwargs):
        self.CONSTANT = None
        self.SQUARE = None
        self.LINEAR = None
        self.SIGMOID = None
        self.SMOOTH = None
        self.GAUSSIAN = None
        self.BELL = None
        self.REVERSED_BELL = None
        self.REVERSED_GAUSSIAN = None
        self.HYPERBOLIC = None
        self.CENTROID = None
        self.CENTROID_LOWER = None
        self.CENTROID_HIGHER = None
        self.RANDOM = None
        self.RANDOM_TRUE = None
        self.RANDOM_CENTROID = None
        self.MEAN = None
        self.MEAN_HIGHER = None
        self.MEAN_LOWER = None
        self.__dict__.update(kwargs)


"""Enum of the shapes used as member functions of {@link FuzzySet}."""
FuzzyShape = Namespace(
    # The set has no boundary on the constant side, every value is in the set on this side.
    CONSTANT="constant",
    # There's no transition on the square side, the value is either in (1) or out (0) of the set.
    SQUARE="square",
    # The transition is linear.
    LINEAR="linear",
    # The transition is a sigmoid (i.e. S-Shape, smooth), using the logistic standard function.
    SIGMOID="sigmoid",
    # Alias for {@link FuzzyShape.SIGMOID}
    SMOOTH="sigmoid",
    # The transition has a "bell" shape, using the gaussian function.
    GAUSSIAN="gaussian",
    # Alias for {@link FuzzyShape.GAUSSIAN}
    BELL="gaussian",
    # Alias for {@link FuzzyShape.REVERSED_GAUSSIAN}
    REVERSED_BELL="reversed_gaussian",
    # The transition has a "reversed bell" shape, using the gaussian function.
    REVERSED_GAUSSIAN="reversed_gaussian")

"""Enum of the algorithms to use in the {@link FuzzyLogic} engine."""
FuzzyLogicAlgorithm = Namespace(
    # Uses Zadeh's method, resulting in a linear logic.
    LINEAR=0,
    # Uses Hyperbolic Parabloid logic, which is a bit heavier than linear, but may have more intuitive results.
    HYPERBOLIC=1)

"""Enum of the algorithms to use when crispifying values."""
FuzzyCrispAlgorithm = Namespace(
    # Uses the centroid method: combines all sets and values and gets the centroid.
    # This method works great to combine more than a couple of rules, but will not work with single rules.
    CENTROID=0,
    # When several values are possible from each set, prefer the lowest one, then combine them to get the
    # centroid. This method works like the centroid and works well even with single rules, but the returned
    # values will tend to be a bit lower.
    CENTROID_LOWER=1,
    # When several values are possible from each set, prefer the highest one, then combine them to get the centroid.
    # This method works like the centroid and works well even with single rules, but the returned values will tend to
    # be a bit higher.
    CENTROID_HIGHER=2,
    # NOT IMPLEMENTED YET
    # Returns a randomly chosen value from all possible values.
    RANDOM=3,
    # NOT IMPLEMENTED YET
    # Returns a randomly chosen value from all possible values from the set with the highest veracity.
    RANDOM_TRUE=4,
    # NOT IMPLEMENTED YET
    # Returns a single random value from each set then combines them to get the centroid.
    RANDOM_CENTROID=5,
    # Returns the mean value from all possible values from all the sets.
    # Unlike the centroid methods, the mean method does not take the veracity of each set into account.
    MEAN=6,
    # Returns the mean value from all the highest possible values from all the sets.
    # Unlike the centroid methods, the mean method does not take the veracity of each set into account.
    MEAN_HIGHER=7,
    # Returns the mean value from all the lowest possible values from all the sets.
    # Unlike the centroid methods, the mean method does not take the veracity of each set into account.
    MEAN_LOWER=8)
