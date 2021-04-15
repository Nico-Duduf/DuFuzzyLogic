class FuzzyQuantifier():
    """! Enum of available quantifiers. """

    ## This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
    IS_NOT = "Not"
    ## This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
    LESS = "Less"
    ## Slightly
    DOUBLE_MINUS = "Slightly"
    ## Somewhat
    MINUS = "Somewhat"
    ## Moderately
    AVERAGE = "Moderately"
    ## None
    NONE = ""
    ## Very
    PLUS = "Very"
    ## Extremely
    DOUBLE_PLUS = "Extremely"
    ## This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
    IS = "Completely"
    ## This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
    MORE = "More"

    FuzzyQuantifierList = {
        IS_NOT: "Not", LESS: "Less", DOUBLE_MINUS: "Slightly", MINUS: "Somewhat", AVERAGE: "Moderately",
        NONE: "", PLUS: "Very", DOUBLE_PLUS: "Extremely", IS: "Completely", MORE: "More"
    }
