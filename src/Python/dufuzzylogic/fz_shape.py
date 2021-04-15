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
