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
