# Quantifiers

To improve the precision of the rules, we can use quantifiers, i.e. instead of just checking `IF temperature IS hot` we could check `IF temperature IS *VERY* hot` or `IF temperature IS *SLIGHTLY* hot`.

Quantifiers are mostly used when checking the inclusion of a value in a set (i.e. the veracity of a propostion like "IF anything IS *VERY* something"), but they can also be used for setting a value (e.g. in the statement "THEN SET something *VERY* anything")

## Condition quantifiers

Quantifiers could also be useful to adjust the global veracity of a statement instead of the veracity of each operand. For example, the statement `IF temperature IS SOMEWHAT hot AND humidity IS SOMEWHAT high` could become `MAYBE temperature IS hot AND humidity IS high`.

In this case a possible list of these "quantified conditions" could be:  
***If, Probably, Maybe, Somewhat, Not***

## A Game of words

Depending on the implementation of Fuzzy Logic, there may be several ways to represent quantifiers. They could be a value, for example varying in a [0, 1] range from "just a bit" to "extremely". Or they may be linguistic, actual words, to keep the language intuitive and easy to use and understand, close to natural language.

Linguistic quantifiers are also easier to differenciate from veracities which can also be reprensented as values in the range [0, 1] and could be easily confused with them. As veracities need to be precise, they need to be actual numbers. On the contrary, quantifiers do not need that precision and can be represented by a carefully chosen set of words.

In case of linguistic quantifiers, the choice of the words to use is importanat: their interpretation will influence how they are used when coding with Fuzzy Logic. There can be three ways of defining linguistic quantifiers, to make them both easy to use and remember, and more or less precise or subtle:

1. ***Linguistic***: actual words (English, or any other language) with their true meaning.
2. ***Newlinguistic*** or ***Orwellian***: neologisms, like those Orwell describres in his *newspeak* in the novel *1984*, created to simplify natural language and make it both less subtle and more objective.
3. ***Symbolic***: adjectives from natural language, but used differently than their true meanings, like the some properties of quantic particles, for example the *color charges* - red, green, blue, antigreen, antiblue, antired - or the *flavors* of quarks - strange, charm, bottom, top... - which obviously do not really describe any color or strangeness.

### Linguistic

As one goal of programming with Fuzzy Logic is to keep it simple and natural, using actual language and the *linguistic* version of quantifiers would be best, as they make the most intuitive and subtle possible. But with all the ambiguity and subjectiveness of language, this is *quite* a *very* difficult task to implement, unless each quantifier is precisely described in the documentation. Which makes it paradoxically *a bit* counter-intuitive.

A possible list of English quantifiers could be (in this order ?):  
***Not, least, a bit, lesser, less than, quite (UK), rather, fairly, more or less, average, quite (US), very, extremely, almost, completely...***

### Newlinguistic - Orwellian (Newspeak)

*Orwellian Newspaak* makes things easier while keeping the vocabulary user-friendly even if it is - by design - less subtle and more abstract.

Newspeak quantifiers are a composite of the word *Plus* or *Minus* with a multiplier, to which we can add *Not*, *Average* and *Completely*, which gives us this list:  
***Not, tripleminus, doubleminus, minus, average, plus, doubleplus, tripleplus, completely***.

And this list can be expanded at will.

### Symbolic

Symbolic quantifiers are another way to abstractify the words describing quantifiers, while keeping them easy to use and remember.

They could be adjectives which could be *more or less* intuitively sorted, like "bright" and "dark" or "light" and "heavy", but it may be difficult to build a list long enough to allow the precision needed with some systems. One could combine different meanings and arbitrarily sort them to have a list like this:  
***Not, gaseous, light, liquid, fluid, floppy, solid, hard, heavy...***

Or one could use alphabetically sorted adjectives:  
***able, bad, cool, dark...***

Or even adjectives sorted by their number of letters:  
***Not, cool, green, purple, abstract, objective...***

For systems which do not need too many quantifiers and thus too many words to remember, this method can actually be useful and funny to use.
