// ====== SOME MATH FUNCTIONS =========

/**
 * Some general purpose Math functions 
 * @namespace
 */
FzMath = {};

/**
    * The logistic function (sigmoid)
    * @param {Number} value The value
    * @param {Number} [midValue=0] The midpoint value, at which the function returns max/2
    * @param {Number} [min=0] The minimum return value
    * @param {Number} [max=1] The maximum return value
    * @param {Number} [rate=1] The logistic growth rate or steepness of the function
    * @return {Number} The result in the range [min, max] (excluding min and max)
    */
FzMath.logistic = function( value, midValue, min, max, rate)
{
    if (typeof midValue === "undefined") midValue = 0;
    if (typeof min === "undefined") min = 0;
    if (typeof max === "undefined") max = 1;
    if (typeof rate === "undefined") rate = 1;
    var exp = -rate*(value - midValue);
    var result = 1 / (1 + Math.pow(Math.E, exp));
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
FzMath.inverseLogistic = function ( v, midValue, min, max, rate)
{
    if (typeof midValue === "undefined") midValue = 0;
    if (typeof max === "undefined") max = 1;
    if (typeof min === "undefined") min = 0;
    if (typeof rate === "undefined") rate = 1;

    if (v == min) return 0;
    
    return midValue - Math.log( (max-min)/(v-min) - 1) / rate;
}

/**
    * The gaussian function
    * @param {Number} value The variable
    * @param {Number} [min=0] The minimum return value
    * @param {Number} [max=1] The maximum return value
    * @param {Number} [center=0] The center of the peak
    * @param {Number} [fwhm=1] The full width at half maximum of the curve
    * @return {Number} The result
    */
FzMath.gaussian = function( value, min, max, center, fwhm)
{
    if (typeof max === "undefined") max = 1;
    if (typeof min === "undefined") min = 0;
    if (typeof center === "undefined") center = 0;
    if (typeof fwhm === "undefined") fwhm = 1;
    if (fwhm === 0 && value == center) return max;
    else if (fwhm === 0) return 0;

    var exp = -4 * Math.LN2;
    exp *= Math.pow((value - center),2);
    exp *= 1/ Math.pow(fwhm, 2);
    var result = Math.pow(Math.E, exp);
    return result * (max-min) + min;
}

/**
    * A "reversed" gaussian function, growing faster with low value
    * @param {Number} value The variable
    * @param {Number} [min=0] The minimum return value
    * @param {Number} [max=1] The maximum return value
    * @param {Number} [center=0] The center of the peak
    * @param {Number} [fwhm=1] The full width at half maximum of the curve
    * @return {Number} The result
    */
FzMath.reversedGaussian = function ( value, min, max, center, fwhm )
{
    r = -value-fwhm+1;
    return gaussian( value, min, max, center, r);
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
FzMath.inverseGaussian = function( v, min, max, center, fwhm)
{
    if (typeof max === "undefined") max = 1;
    if (typeof min === "undefined") min = 0;
    if (typeof center === "undefined") center = 0;
    if (typeof fwhm === "undefined") fwhm = 1;
    if (v == 1) return [center, center];
    if (v === 0) return [center + fwhm/2, center - fwhm/2];
    if (fwhm === 0) return [center, center];

    var result = (v-min)/(max-min);
    result = Math.log( result ) * Math.pow(fwhm,2);
    result = result / ( -4 * Math.LN2 );
    result = Math.sqrt( result );
    return [ result + center, -result + center ];
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
FzMath.inverseReversedGaussian = function( value, min, max, center, fwhm)
{
    r = -value-fwhm+1;
    return inverseGaussian( value, min, max, center, r);
}

/**
    * Returns the mean of a set of values
    * @param {Number[]} values The values
    * @return {Number} The mean
    */
FzMath.mean = function( values )
{
    var num = values.length;
    var result = 0;
    for (var i = 0; i < num; i++)
    {
        result += values[i];
    }
    return result / num;
}

// =========== FUZZY SETS ============

/**
    * Do not use the constructor of this class, use {@link FuzzyLogic.newSet} to create a new set.<br >
    * Most of the time you won't need to access the properties nor use the methods of this class, but use the methods of {@link FuzzyLogic}, {@link FuzzyValue}, {@link FuzzyVeracity}
    * @class
    * @classdesc A Fuzzy set.
    * @property {string} name The name of this set .
    * @property {Number} valueNOT One of the closest value which is not in the set (either above or below).
    * @property {Number} valueIS The value which best fits in the set, the most extreme/maximum in the set.
    * @property {FuzzyShape} shape The shape (i.e. interpolation or transition) when getting in (below) the set.
    * @property {FuzzyShape} shapeAbove The shape (i.e. interpolation or transition) when getting out (above) of the set.
    * @property {Number} plateauMin The value above which a value is considered completely included.
    * @property {Number} plateauMax The value under which a value is considered completely included.
    */
function FuzzySet( name, valueNot, valueIS, shape, shapeAbove, plateauMin, plateauMax, algorithm)
{
    var min;
    var max;
    if (valueNot > valueIS){
        max = valueNot;
        min = valueNot - (valueNot - valueIS) * 2;
    }
    else
    {
        min = valueNot;
        max = valueNot + (valueIS - valueNot) * 2;
    }

    if (typeof shape === "undefined") shape = FuzzyShape.LINEAR;
    if (typeof shapeAbove === "undefined") shapeAbove = shape;
    if (typeof plateauMin === "undefined") plateauMin = FzMath.mean([min, max]);
    if (typeof plateauMax === "undefined") plateauMax = FzMath.mean([min, max]);

    this.name = name;
    this.min = min;
    this.max = max;
    this.shapeIn = shape;
    this.shapeOut = shapeAbove;
    this.plateauMin = plateauMin;
    this.plateauMax = plateauMax;

    this.algorithm = algorithm;
}

/**
    * Checks if a value is contained in the set.
    * @param {Number|FuzzyValue} v The value to test.
    * @param {FuzzyQuantifier|String} [quantifier=FuzzyQuantifier.NONE] Checks in which part of the set the value is in.
    * @return {FuzzyVeracity} The veracity.
    */
FuzzySet.prototype.contains = function ( v, quantifier )
{
    var value;
    if (v instanceof FuzzyValue) value = v.crispify(false);
    else value = v;

    quantifier = FuzzyLogic.getQuantifier(quantifier);

    if (value >= this.plateauMin && value <= this.plateauMax)
    {
        return quantifier(1, this.algorithm);
    }
    else if (value < this.plateauMin)
    {
        if (this.shapeIn === FuzzyShape.CONSTANT)
        {
            return quantifier(1, this.algorithm);
        }
        else if (this.shapeIn === FuzzyShape.SQUARE)
        {
            var min = FzMath.mean(this.plateauMin, this.min);
            if (value >= min) return quantifier(1, this.algorithm);
            else return quantifier(0, this.algorithm);
        }
        else if (this.shapeIn === FuzzyShape.LINEAR)
        {
            if (value < this.min) return quantifier(0, this.algorithm);
            else return quantifier( (value-this.min) / (this.plateauMin - this.min), this.algorithm );
        }
        else if (this.shapeIn === FuzzyShape.SIGMOID)
        {
            var mid = (this.plateauMin + this.min) / 2;
            var rate = 6 / (this.plateauMin - this.min);
            return quantifier(FzMath.logistic(value, mid, 0, 1, rate), this.algorithm);
        }
        else if (this.shapeIn === FuzzyShape.GAUSSIAN)
        {
            var width = this.plateauMin - this.min;
            return quantifier( FzMath.gaussian( value, 0, 1, this.plateauMin, width) , this.algorithm);
        }
        else if (this.shapeIn === FuzzyShape.REVERSED_GAUSSIAN)
        {
            var width = this.plateauMin - this.min;
            return quantifier( FzMath.reversedGaussian( value, 0, 1, this.plateauMin, width) , this.algorithm );
        }
        else return quantifier(0, this.algorithm);
    }
    else
    {
        if (this.shapeOut === FuzzyShape.CONSTANT)
        {
            return quantifier(1, this.algorithm);
        }
        else if (this.shapeOut === FuzzyShape.SQUARE)
        {
            var max = FzMath.mean(this.plateauMax, this.max);
            if (value <= max) return quantifier(1, this.algorithm);
            else return quantifier(0, this.algorithm);
        }
        else if (this.shapeOut === FuzzyShape.LINEAR)
        {
            if (value > this.max) return quantifier(0, this.algorithm);
            else return quantifier (1 - ((value - this.plateauMax ) / (this.max - this.plateauMax) ), this.algorithm);
        }
        else if (this.shapeOut === FuzzyShape.SIGMOID)
        {
            var mid = (this.plateauMax + this.max) / 2;
            var rate = 6 / (this.max - this.plateauMax);
            return quantifier( 1 - FzMath.logistic(value, mid, 0, 1, rate) , this.algorithm);
        }
        else if (this.shapeOut === FuzzyShape.GAUSSIAN)
        {
            var width = this.max - this.plateauMax;
            return quantifier( FzMath.gaussian( value, 0, 1, this.plateauMax, width), this.algorithm );
        }
        else if (this.shapeOut === FuzzyShape.REVERSED_GAUSSIAN)
        {
            var width = this.max - this.plateauMax;
            return quantifier( FzMath.reversedGaussian( value, 0, 1, this.plateauMax, width), this.algorithm );
        }
        else return quantifier(0, this.algorithm);
    } 
}

/**
    * Gets a list of precise values from the set corresponding to the given veracity.
    * @param {FuzzyVeracity|Number} [veracity=0.5] The veracity
    * @return {Number[]} The list of possible crisp values, ordered from min to max.
    */
FuzzySet.prototype.getValues = function ( veracity )
{
    if (typeof veracity === "undefined") veracity = 0.5;
    if (veracity instanceof FuzzyVeracity) veracity = veracity.veracity;

    var defaultValue = FzMath.mean( [this.plateauMin, this.plateauMax] );

    if ( this.shapeIn === FuzzyShape.CONSTANT && this.shapeOut === FuzzyShape.CONSTANT ) return [ this.min, this.plateauMin, defaultValue, this.plateauMax, this.max];
    
    var crisp = [];
    
    if (veracity >= 1) crisp = [this.plateauMin, defaultValue, this.plateauMax];

    // below
    if (this.shapeIn === FuzzyShape.CONSTANT && veracity == 1)
    {
        crisp.push(this.min);
    }
    else if (this.shapeIn === FuzzyShape.SQUARE)
    {
        if (veracity >= 0.5) crisp.push( this.plateauMin );
        else crisp.push( this.min );
    }
    else if (this.shapeIn === FuzzyShape.LINEAR)
    {
        range = this.plateauMin - this.min;

        crisp.push( this.min + range * veracity );
    }
    else if (this.shapeIn === FuzzyShape.SIGMOID)
    {
        mid = (this.plateauMin + this.min) / 2;
        crisp.push( FzMath.inverseLogistic(veracity, mid) );
    }
    else if (this.shapeIn === FuzzyShape.GAUSSIAN)
    {
        var width = this.plateauMin - this.min;
        var g = FzMath.inverseGaussian( veracity, 0, 1, this.plateauMin, width);
        crisp.push( g[0] );
    }
    else if (this.shapeIn === FuzzyShape.REVERSED_GAUSSIAN)
    {
        var width = this.plateauMin - this.min;
        var g = FzMath.inverseReversedGaussian( veracity, 0, 1, this.plateauMin, width);
        crisp.push( g[0] );
    }

    //above
    if (this.shapeOut === FuzzyShape.CONSTANT && veracity == 1)
    {
        crisp.push(this.max);
    }
    if (this.shapeOut === FuzzyShape.SQUARE)
    {
        if (veracity >= 0.5) crisp.push( this.plateauMax );
        else crisp.push( this.max );
    }
    else if (this.shapeOut === FuzzyShape.LINEAR)
    {
        range = this.max - this.plateauMax;

        crisp.push( this.max + 1 - (range * veracity) );
    }
    else if (this.shapeOut === FuzzyShape.SIGMOID)
    {
        mid = (this.plateauMax + this.max) / 2;
        crisp.push( FzMath.inverseLogistic( 1-veracity, mid, 0, 1 ) );
    }
    else if (this.shapeOut === FuzzyShape.GAUSSIAN)
    {
        width = this.max - this.plateauMax;
        var g = FzMath.inverseGaussian( 1-veracity, 0, 1, this.plateauMax, width);
        crisp.push( g[1] );
    }
    else if (this.shapeOut === FuzzyShape.REVERSED_GAUSSIAN)
    {
        width = this.max - this.plateauMax;
        var g = FzMath.inverseReversedGaussian( 1-veracity, 0, 1, this.plateauMax, width);
        crisp.push( g[1] );
    }

    // Clamp
    for(var i = 0, num = crisp.length; i < num; i++)
    {
        if ( crisp[i] > this.max ) crisp[i] = this.max;
        if ( crisp[i] < this.min ) crisp[i] = this.min;
    }

    return crisp.sort();
}

/**
    * Gets a list of precise values from the set corresponding to the quantifier
    * @param {FuzzyModifier} [quantifier=FuzzyModifier.AVERAGE] The quantifier
    * @param {FuzzyVeracity|Number} [veracity=0.5] The veracity
    * @return {Number[]} The list of possible crisp values, ordered from min to max.
    */
FuzzySet.prototype.crispify = function ( quantifier, veracity )
{
    quantifier = FuzzyQuantifier.getQuantifier(quantifier);
    var v;
    if (typeof veracity === "undefined") v = quantifier();
    else if (veracity instanceof FuzzyVeracity) v = veracity.veracity;
    else v = veracity;

    v = quantifier(v, this.algorithm, true).veracity;
    return this.getValues( v );
}

/**
 * Gets the closest quantifier to this value
 * @param {Number|FuzzyValue} val The value to quantify
 * @return {FuzzyQuantifier} The quantifier
 */
FuzzySet.prototype.quantify = function ( value )
{
    if (!(value instanceof FuzzyValue)) value = new FuzzyValue(value, "", this.algorithm);
    var val = value.crispify(false);

    if ( this.shapeIn === FuzzyShape.CONSTANT && this.shapeOut === FuzzyShape.CONSTANT ) return FuzzyQuantifier.IS;
    if (val < this.min && this.shapeIn === FuzzyShape.CONSTANT ) return FuzzyQuantifier.IS;
    if (val < this.min) return FuzzyQuantifier.IS_NOT;
    if (val > this.max && this.shapeOut === FuzzyShape.CONSTANT ) return FuzzyQuantifier.IS;
    if (val > this.max) return FuzzyQuantifier.IS_NOT;
    if (val >= this.plateauMin && val <= this.plateauMax) return FuzzyQuantifier.IS;

    var quantifier = FuzzyQuantifier.NOT;
    var veracity = this.contains(val).veracity;

    var distance = 1;
    for (var i in FuzzyQuantifier)
    {
        var q = FuzzyQuantifier[i];
        var test = Math.abs( q() - veracity );
        
        if (test < distance)
        {
            distance = test;
            quantifier = q;
        }
    }

    return quantifier;
}

/**
 * Gets the name of this set.
 * @return {string} The name of the set.
 */
FuzzySet.prototype.toString = function ()
{
    return this.name;
}

// ========= FUZZY VALUES =============

/**
 * Do not use the constructor of this class, use {@link FuzzyLogic.newSet} to create a new set.<br >
 * @class
 * @classdesc FuzzyValue is a value to be used with Fuzzy Logic. It's inclusion in a set can be tested with {@link FuzzyValue.IS} or {@link FuzzyValue.IS_NOT},<br />
 * Use {@link FuzzyValue.SET} or {@link FuzzyLogic.THEN} to change this value using a {@link FuzzySet}
 * @example
 * var logic = new FuzzyLogic();
 * var comfortable = logic.newSet("Warm", 17, 20);
 * var temperature = logic.newValue( 18 );
 * // Test if this temperature is comfortable
 * logic.IF(
 *    temperature.IS_NOT(comfortable);
 * )
 * // Set it very comfortable
 * logic.THEN ( temperature.SET(comfortable, "Very"); )
 * @property {string} unit The unit to display when returning this value as a string.
 * @property {bool} reportEnabled Enables or disable report generation when crispifying. Disabled by default to improve performance.
 * @property {string[][]} report The report (explanation) of the latest crispification {@link FuzzyValue.crispify}.<br />
 * It is an Array containing Arrays of strings. Each sub-array is the report of one rule, which you can print with <code>.join(newLine)</code> for example.
 */
function FuzzyValue( value, unit, algorithm, crispAlgorithm )
{
    if (typeof unit === "undefined") unit = "";
    if (typeof value === "undefined") value = 0;
    this.value = value;
    this.unit = unit;
    this.sets = [];
    this.algorithm = algorithm;
    this.crispAlgorithm = crispAlgorithm;

    this.report = [];
    this.reportEnabled = false;
    this.numRules = 0;
}

/**
 * Tests the inclusion of the value in the set
 * @param {FuzzySet} set The set which may include the value.
 * @param {FuzzyQuantifier|string} quantifier A quantifier.
 * @return {FuzzyVeracity} The veracity of the inclusion of the value in the set.
 */
FuzzyValue.prototype.IS = function(set, quantifier)
{
    var v = set.contains( this, quantifier );
    return v;
}

/**
 * Tests the exclusion of the value in the set
 * @param {FuzzySet} set The set which may (not) include the value.
 * @param {FuzzyQuantifier|string} quantifier A quantifier.
 * @return {FuzzyVeracity} The veracity of the exclusion of the value in the set.
 */
FuzzyValue.prototype.IS_NOT = function (set, quantifier)
{
    var x = set.contains( this.value, quantifier );
    return x.NEGATE();
}

/**
 * Changes the value according to a new veracity.
 * @param {FuzzySet} set The set.
 * @param {FuzzyModifier} [quantifier=FuzzyModifier.NONE] The quantifier
 * @param {FuzzyVeracity} [veracity] The veracity.
 */
FuzzyValue.prototype.SET = function ( set,  quantifier, veracity )
{
    if (typeof veracity === "undefined") veracity = new FuzzyVeracity(1, this.algorithm);
    
    quantifier = FuzzyQuantifier.getQuantifier(quantifier);
    
    this.numRules++;
    veracity.ruleNum = this.numRules;

    // Check if this set is already here
    for (var i = 0, num = this.sets.length; i < num; i++)
    {
        if (set.name == this.sets[i].name) 
        {
            this.sets[i].quantifiers.push(quantifier);
            this.sets[i].veracities.push(veracity);
            return;
        }
    }

    //otherwise, add it
    set.quantifiers = [quantifier];
    set.veracities = [veracity];
    this.sets.push( set );
}

/**
 * Computes a crisp value depending on the inclusions which have been set before using {@link FuzzyValue.SET}.
 * @param {bool} [clearSets=true] When crispifying, the sets added with {@link FuzzyValue.SET} are cleared, this means changes made before the call to crispify() will be lost in subsequent calls. Set this parameter to false to keep these previous changes.
 * @param {FuzzyCrispAlgorithm} [algorithm] Change the algorithm to use for crispification.
 * @return {Number} The crisp (i.e. standard) value.
 */
FuzzyValue.prototype.crispify = function ( clearSets, algorithm )
{
    if (typeof clearSets === "undefined") clearSets = true;
    if (typeof algorithm === "undefined") algorithm = this.crispAlgorithm;

    if (this.sets.length == 0) return this.value;

    var crisp = 0;
    this.report = [];

    function ruleSorter(a, b)
    {
        return a.number - b.number;
    }

    // get all average values
    // and veracities from the sets
    var sumWeights = 0;
    for (var i = 0, num = this.sets.length; i < num; i++)
    {
        var set = this.sets[i];
        for( var j = 0, numV = set.veracities.length; j < numV; j++)
        {
            // the veracity
            var v = set.veracities[j];
            var q = set.quantifiers[j];
            // the corresponding values
            var vals = set.crispify( q, v );
            var val;
            var ver;

            if (algorithm == FuzzyCrispAlgorithm.CENTROID || algorithm == FuzzyCrispAlgorithm.MEAN) val = FzMath.mean(vals);
            else if (algorithm == FuzzyCrispAlgorithm.CENTROID_LOWER || algorithm == FuzzyCrispAlgorithm.MEAN_LOWER) val = vals[0];
            else if (algorithm == FuzzyCrispAlgorithm.CENTROID_HIGHER || algorithm == FuzzyCrispAlgorithm.MEAN_HIGHER) val = vals[vals.length-1];

            if (algorithm == FuzzyCrispAlgorithm.CENTROID || algorithm == FuzzyCrispAlgorithm.CENTROID_LOWER || algorithm == FuzzyCrispAlgorithm.CENTROID_HIGHER)
            {
                crisp += val * v.veracity;
                ver = v.veracity;
            }
            else if (algorithm == FuzzyCrispAlgorithm.MEAN || algorithm == FuzzyCrispAlgorithm.MEAN_LOWER || algorithm == FuzzyCrispAlgorithm.MEAN_HIGHER)
            {
                crisp += val;
                ver = 1;
            }

            sumWeights += ver;
            

            // generate report
            if (this.reportEnabled)
            {
                for (var iVals = 0, numVals = vals.length; iVals < numVals; iVals++)
                {
                    vals[iVals] = Math.round(vals[iVals]*1000)/1000;
                }

                var reportRule = [];
                reportRule.push( "Rule #" + v.ruleNum +": Set " + set.toString() + " (" + q.toString() + ")" );
                reportRule.push( "Gives value: " + Math.round(val*1000)/1000 + " from these values: [ " + vals.join(", ") + " ]");
                reportRule.push( "With a veracity of: " + Math.round(ver*1000)/1000 );
                reportRule.number = v.ruleNum;
                this.report.push( reportRule );
            }
        }
    }
            
    if (sumWeights != 0) crisp = crisp / sumWeights;


    //sort the report
    if (this.reportEnabled) this.report.sort(ruleSorter);

    if (clearSets)
    {
        // freeze all
        this.value = crisp;
        //reset sets
        this.sets = [];
    }

    return crisp;
}

/**
 * This is an alias for {@link FuzzyValue.prototype.crispify};
 * @method
 */
FuzzyValue.prototype.toNumber = FuzzyValue.prototype.crispify;
/**
 * This is an alias for {@link FuzzyValue.prototype.crispify};
 * @method
 */
FuzzyValue.prototype.toFloat = FuzzyValue.prototype.crispify;
/**
 * This is an alias for {@link FuzzyValue.prototype.crispify};
 * @method
 */
FuzzyValue.prototype.defuzzify = FuzzyValue.prototype.crispify;

/**
 * Returns the closest quantifier for this value in this set
 * @param {FuzzySet} set The set
 * @return {FuzzyQuantifier} The quantifier
 */
FuzzyValue.prototype.quantify = function (set)
{
    return set.quantify(this);
}

/**
 * Returns a string representation of the value with its unit (if any)
 * @param {FuzzyCrispAlgorithm} [crispAlgorithm] The algorithm to use for crispification before returning the string. Uses the algorithm set when creating the {@link FuzzyLogic} instance by default.
 * @param {FuzzySet} [set] A set to quantify the value
 * @return {string} The description of the value
 */
FuzzyValue.prototype.toString = function( crispAlgorithm, set )
{
    var v = this.crispify( false, crispAlgorithm );
    v = Math.round( v * 100 ) / 100;
    var str = v + this.unit;
    if (typeof set !== "undefined") str += " is " + set.quantify(this).toString() + " " + set.toString();
    return str;
}

// ========== FUZZY VERACITY ==========

/**
 * @class
 * @classdesc FuzzyVeracity is the fuzzy equivalent of a crisp boolean in boolean logic. It represents the result of logical operations (IS, AND, OR...).<br />
 * Its value can vary in the range [0.0, 1.0], 0.0 being the equivalent of "false" and 1.0 of "true".<br />
 * You can acces logic operators through instances of this class, which enable fluent syntax for rules (Except IS and IS_NOT which are members of {@link FuzzyValue}).<br />
 * Operators are methods in upper case.
 * @example
 * var logic = new FuzzyLogic();
 * var intense = logic.newSet("Intense", 0, 255);
 * // An RGB color to test
 * var color = [255,200,10];
 * // Separate channels
 * var redChannel = logic.newValue( color[0] );
 * var greenChannel = logic.newValue( color[1] );
 * var blueChannel = logic.newValue( color[2] );
 * // isRed will be a FuzzyVeracity, the result of the test.
 * // Note that FuzzyValue.IS returns a FuzzyVeracity, on which the methods AND and NOR are called.
 * // But this is all internal and you don't really need to know that to use this syntax.
 * var isRed = redChannel.IS( intense )
 *      .AND(
 *         greenChannel.IS( intense ).
 *         NOR( blueChannel.IS( intense ))
 *      )
 * @property {Number} veracity The veracity level in the range [0.0, 1.0]
 */
function FuzzyVeracity( veracity, algorithm )
{
    if (typeof algorithm === "undefined") algorithm = FuzzyLogicAlgorithm.LINEAR;
    this.veracity = veracity;
    this.algorithm = algorithm;
}

/**
 * Negates the current veracity. A new veracity is returned, and the current veracity is not changed.
 * @return {FuzzyVeracity} The negation of this veracity.
 */
FuzzyVeracity.prototype.NEGATE = function()
{
    return new FuzzyVeracity( 1 - this.veracity, this.algorithm );
}

/**
 * The equivalent of the boolean operation <code>this && other</code>
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.AND = function( other )
{
    var x = this.veracity;
    var y = other.veracity;

    var v = 0;
    if (this.algorithm == FuzzyLogicAlgorithm.LINEAR) v = Math.min(x, y);
    else v = x*y;

    return new FuzzyVeracity( v, this.algorithm );
}

/**
 * The equivalent of the boolean operation <code>this || other</code>
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.OR = function( other )
{
    var x = this.veracity;
    var y = other.veracity;

    var v = 0;
    if (this.algorithm == FuzzyLogicAlgorithm.LINEAR) v = Math.max(x, y);
    else v = x + y - x*y;

    return new FuzzyVeracity( v, this.algorithm );
}

/**
 * The equivalent of the boolean operation <code>this != other</code>
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.XOR = function( other )
{
    var x = this.veracity;
    var y = other.veracity;

    var v = 0;
    if (this.algorithm == FuzzyLogicAlgorithm.LINEAR) v = x+y - 2*Math.min(x,y);
    else v = x+y - 2*x*y;

    return new FuzzyVeracity( v, this.algorithm );
}

/**
 * The equivalent of the boolean operation <code>this != other</code>
 * @method
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.IS_NOT = FuzzyVeracity.prototype.XOR;

/**
 * The equivalent of the boolean operation <code>this != other</code>
 * @method
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.DIFFERENT = FuzzyVeracity.prototype.XOR;

/**
 * The equivalent of the boolean operation <code>this == other</code>
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.NXR = function( other )
{
    var x = this.veracity;
    var y = other.veracity;

    var v = 0;
    if (this.algorithm == FuzzyLogicAlgorithm.LINEAR) v = 1-x-y + 2*Math.min(x,y);
    else v = 1-x-y + 2*x*y;

    return new FuzzyVeracity( v, this.algorithm );
}

/**
 * The equivalent of the boolean operation <code>this == other</code>
 * @method
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.IS = FuzzyVeracity.prototype.NXR;

/**
 * The equivalent of the boolean operation <code>this == other</code>
 * @method
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.EQUALS = FuzzyVeracity.prototype.NXR;

/**
 * The equivalent of the boolean operation <code>!(this && other)</code> or <code>!this || other</code>
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.IMPLIES = function( other )
{
    var x = this.veracity;
    var y = other.veracity;

    var v = 0;
    if (this.algorithm == FuzzyLogicAlgorithm.LINEAR) v = 1-Math.min(x, 1-y);
    else v = 1-x + x*y;

    return new FuzzyVeracity( v, this.algorithm );
}

/**
 * The equivalent of the boolean operation <code>!(this && other)</code> or <code>!this || other</code>
 * @method
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.WITH = FuzzyVeracity.prototype.IMPLIES;

/**
 * The equivalent of the boolean operation <code>!(this && other)</code> or <code>!this || other</code>
 * @method
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.HAS = FuzzyVeracity.prototype.IMPLIES;

/**
 * The equivalent of the boolean operation <code>this && !other</code> or <code>!(this || other)</code>
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.DOES_NOT_IMPLY = function( other )
{
    var x = this.veracity;
    var y = other.veracity;

    var v = 0;
    if (this.algorithm == FuzzyLogicAlgorithm.LINEAR) v = Math.min(x, 1-y);
    else v = x*(1-y);

    return new FuzzyVeracity( v );
}

/**
 * The equivalent of the boolean operation <code>this && !other</code> or <code>!(this || other)</code>
 * @method
 * @method
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.WITHOUT = FuzzyVeracity.prototype.DOES_NOT_IMPLY;

/**
 * The equivalent of the boolean operation <code>this && !other</code> or <code>!(this || other)</code>
 * @method
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.DOES_NOT_HAVE = FuzzyVeracity.prototype.DOES_NOT_IMPLY;


/**
 * The equivalent of the boolean operation <code>this && !other</code> or <code>!(this || other)</code>
 * @method
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.AND_NOT = FuzzyVeracity.prototype.DOES_NOT_IMPLY;

/**
 * The equivalent of the boolean operation <code>!(this && other)</code>
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.NAND = function( other )
{
    var x = this.veracity;
    var y = other.veracity;

    var v = 0;
    if (this.algorithm == FuzzyLogicAlgorithm.LINEAR) v = 1 - Math.min(x, y);
    else v = 1 - x*y;

    return new FuzzyVeracity( v );
}

/**
 * The equivalent of the boolean operation <code>!(this && other)</code>
 * @method
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.NOT_BOTH = FuzzyVeracity.prototype.NAND;

/**
 * The equivalent of the boolean operation <code>!(this || other)</code>
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.NOR = function( other )
{
    var x = this.veracity;
    var y = other.veracity;

    var v = 0;
    if (this.algorithm == FuzzyLogicAlgorithm.LINEAR) v = 1 - Math.max(x, y);
    else v = 1-x-y + x*y;

    return new FuzzyVeracity( v );
}

/**
 * The equivalent of the boolean operation <code>!(this || other)</code>
 * @method
 * @param {FuzzyVeracity} other The other operand.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.NONE = FuzzyVeracity.prototype.NOR;

/**
 * Weights this and other according to a given factor.<br />
 * The weight factor is applied to the other operand, and the <code>1 - weight</code> factor is applied to this.
 * @param {FuzzyVeracity} other The other operand.
 * @param {Number} weight The weight.
 * @return {FuzzyVeracity}
 */
FuzzyVeracity.prototype.WEIGHTED = function( other, weight )
{
    var x = this.veracity;
    var y = other.veracity;

    var v = (1-w)*x +  w*y;

    return new FuzzyVeracity( v );
}


// ========= FUZZY  LOGIC ==========

/**
    * Creates a new Fuzzy Logic Engine.
    * @class
    * @classdesc The Fuzzy Logic engine
    * @author Nicolas Dufresne
    * @copyright 2020 Nicolas Dufresne and contributors
    * @version 1.0.0
    * @license GPL-3.0
    * @param {FuzzyLogicAlgorithm} [algorithm=FuzzyLogicAlgorithm.LINEAR] The algorithm to use for logic operations
    * @param {FuzzyCrispAlgorithm} [crispAlgorithm=FuzzyCrispAlgorithm.CENTROID] The algorithm to use for crispification
    */
function FuzzyLogic( algorithm, crispAlgorithm )
{
    if (typeof algorithm === "undefined") algorithm = FuzzyLogicAlgorithm.LINEAR;
    if (typeof crispAlgorithm === "undefined") crispAlgorithm = FuzzyCrispAlgorithm.CENTROID;
    this.algorithm = algorithm;
    this.veracity = new FuzzyVeracity(0);
    this.crispAlgorithm = crispAlgorithm
}

/**
 * Creates a new {@link FuzzyValue}
 * @param {Number} [value] The initial crisp value.
 * @param {string} [unit] The unit to display when returning this value as a string.
 * @return {FuzzyValue} The value.
 */
FuzzyLogic.prototype.newValue = function (value, unit)
{
    return new FuzzyValue( value, unit, this.algorithm, this.crispAlgorithm );
}

/**
 * Creates a new {@link FuzzyVeracity}
 * @param {Number} veracity The initial veracity, in the range [0.0, 1.0].
 * @return {FuzzyVeracity} The veracity.
 */
FuzzyLogic.prototype.newVeracity = function (veracity)
{
    return new FuzzyVeracity(veracity, this.algorithm);
}

/**
    * Creates a new {@link FuzzySet}.
    * @example
    * var logic = new FuzzyLogic();
    * // Temperatures between 15 and 25 will be considered comfortable, 20 being the most comfortable
    * var comfortabble = logic.newSet("Warm", 15, 20);
    * // Temperatures under 17 are cold, and temperatures under 0 are the most cold (because of the constant shape below)
    * var cold = logic.newSet("Cold", 17, 0, FuzzyShape.CONSTANT);
    * // Temperatures above 23 are hot, and all temperatures above 35 are the most hot (because of the constant shape above)
    * var hot = logic.newSet("Hot", 23, 35, FuzzyShape.GAUSSIAN, FuzzyShape.CONSTANT);
    * @param {string} name The unique name of this set (e.g. "hot", "fast", "red", "flower addict"...). <strong>It must be unique!</strong>
    * @property {Number} valueNOT One of the closest value which is not in the set (either above or below).
    * @property {Number} valueIS The value which best fits in the set, the most extreme/maximum in the set.
    * @param {FuzzyShape} [shapeBelow=FuzzyShape.LINEAR] The shape (i.e. interpolation or transition) when getting in the set.
    * @param {FuzzyShape} [shapeAbove=shape] The shape (i.e. interpolation or transition) when getting out of the set. By default, same as shape.
    * @param {Number} [plateauMin] The value above which it is considered completely included. By default, it is at the middle between min and max.
    * @param {Number} [plateauMax] The value under which it is considered completely included. By default, it is at the middle between min and max.
    * @return {FuzzySet} The set.
    */
FuzzyLogic.prototype.newSet = function ( name, extremeValue, referenceValue, shape, shapeAbove, plateauMin, plateauMax)
{
    return new FuzzySet(name, extremeValue, referenceValue, shape, shapeAbove, plateauMin, plateauMax, this.algorithm);
}

/**
 * This function internally stores the veracity to be used with {@link FuzzyLogic.THEN}.
 * @example
 * var logic = new FuzzyLogic();
 * var comfortable = logic.newSet("Warm", 17, 20);
 * var temperature = logic.newValue( 18 );
 * // Test if this temperature is comfortable
 * logic.IF(
 *    temperature.IS_NOT(comfortable);
 * )
 * // Set it very comfortable
 * logic.THEN ( temperature.SET(comfortable, "Very"); )
 * @param {FuzzyVeracity} [fzVeracity] The veracity of the statement.
 * @return {FuzzyVeracity} The value passed as argument.
 */ 
FuzzyLogic.prototype.IF = function ( veracity )
{
    this.veracity = veracity;
    return veracity;
}

/**
 * This function sets a value in a new set, using the veracity resulting from the previous call to {@link FuzzyLogic.IS}.<br /|
 * It can be called several times after any call to IF.
 * @example
 * var logic = new FuzzyLogic();
 * var comfortable = logic.newSet("Warm", 17, 20);
 * var power = logic.newSet("Fan power", 0, 100);
 * var temperature = logic.newValue( 18 );
 * var fanPower = logic.newValue();
 * // Test if this temperature is comfortable
 * logic.IF(
 *    temperature.IS_NOT(comfortable);
 * )
 * // Set it very comfortable
 * logic.THEN ( temperature.SET(comfortable, "Very"); )
 * // and turn on the fan
 * logic.THEN ( fanPower.SET( power ); )
 * @param {FuzzyValue} [value] The value to set.
 * @param {FuzzySet} [set] The set the value has to be included in.
 * @param {FuzzyQuantifier} [quantifier] A quantifier to apply for setting the value.
 */
FuzzyLogic.prototype.THEN = function ( value, set, quantifier )
{
    value.SET(set, quantifier, this.veracity);
}

// ========= ENUMS =============

// Quantifiers
{
    /**
        * Enum of quantifiers. You can use both the JS name (e.g. FuzzyQuantifier.MINUS) or the string (e.g. "Somewhat") in your code.
        * @namespace
        */
    FuzzyQuantifier = {};

    /**
     * This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
     * @type {string}
     * @default "Not"
     */
    FuzzyQuantifier.IS_NOT = function (v, algorithm, inverse) {
        if (typeof v === "undefined") return 0;
        var q = inverse ? 0 : 1;
        return new FuzzyVeracity(q, algorithm);
    };
    FuzzyQuantifier.IS_NOT.toString = function() {return "Not"; };

    /**
     * This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
     * @type {string}
     * @default "Less"
     */
    FuzzyQuantifier.LESS = function (v, algorithm, inverse) {
        if (typeof v === "undefined") return 0;
        var q = inverse ? 0 : 1;
        return new FuzzyVeracity(q, algorithm);
    };
    FuzzyQuantifier.LESS.toString = function() {return "Less"; };

    /**
     * @type {string}
     * @default "Slightly"
     */
    FuzzyQuantifier.DOUBLE_MINUS = FuzzyQuantifier.createQuantifier( 1/3, "Slightly");

    /**
     * @type {string}
     * @default "Somewhat"
     */
    FuzzyQuantifier.MINUS = FuzzyQuantifier.createQuantifier( 0.5, "Somewhat");

    /**
     * @type {string}
     * @default "Moderately"
     */
    FuzzyQuantifier.AVERAGE = function (v, algorithm) {
        if (typeof v === "undefined") return 0.5;
        else return new FuzzyVeracity( v, algorithm);
    };
    FuzzyQuantifier.AVERAGE.toString = function() {return "Moderately"; };

    /**
     * @type {string}
     * @default "Very"
     */
    FuzzyQuantifier.PLUS = FuzzyQuantifier.createQuantifier( 2, "Very");

    /**
     * @type {string}
     * @default "Extremely"
     */
    FuzzyQuantifier.DOUBLE_PLUS = FuzzyQuantifier.createQuantifier( 3, "Extremely");

    /**
     * This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
     * @type {string}
     * @default "Completely"
     */
    FuzzyQuantifier.IS = function (v, algorithm, inverse) { 
        if (typeof v === "undefined") return 1;
        var q = inverse ? 1 : 0;
        return new FuzzyVeracity( q, algorithm);
    };
    FuzzyQuantifier.IS.toString = function() { return "Completely"; };

    /**
     * This quantifier is meant to be used for crispification (with {@link FuzzyLogic.SET} or {@link FuzzyValue.SET})
     * @type {string}
     * @default "More"
     */
    FuzzyQuantifier.MORE = function (v, algorithm, inverse) {
        if (typeof v === "undefined") return 1;
        var q = inverse ? 1 : 0;
        return new FuzzyVeracity( q, algorithm);
    };
    FuzzyQuantifier.MORE .toString = function() {return "More"; };


    // ====== LOW-LEVEL UTILS =====

    // low-level undocumented function.
    // gets a quantifier by its name
    FuzzyQuantifier.getQuantifier = function( quantifier )
    {
        if (typeof quantifier === "undefined") return FuzzyQuantifier.AVERAGE;
        if (typeof quantifier === "function") return quantifier;
        if (quantifier === "") return FuzzyQuantifier.AVERAGE;
        
        quantifier = quantifier.toLowerCase();

        for(var i in FuzzyQuantifier)
        {
            var q = FuzzyQuantifier[i];
            var n = q.toString().toLowerCase();

            if (n === quantifier) return q;
        }

        throw ("Quantifier \"" + quantifier + "\" is unknown.");
    }

    // low-level undocumented function.
    // creates a quantifier
    FuzzyQuantifier.createQuantifier = function(q , name )
    {
        function qObj (v, algorithm, inverse) {
            if (typeof v === "undefined") return Math.pow( 0.5, 1/q);
            var p = inverse ? 1/q : q;
            return new FuzzyVeracity( Math.pow(v, p), algorithm);
        };
        qObj.toString = function (){return name;};
        return qObj;
    }

}

/**
    * Enum of the shapes used as member functions of {@link FuzzySet}.
    * @namespace
    */
FuzzyShape = {
    /**
     * The set has no boundary on the constant side, every value is in the set on this side.
     */
    CONSTANT: "constant",
    /**
     * There's no transition on the square side, the value is either in (1) or out (0) of the set.
     */
    SQUARE: "square",
    /**
     * The transition is linear.
     */
    LINEAR: "linear",
    /**
     * The transition is a sigmoid (i.e. S-Shape, smooth), using the logistic standard function.
     */
    SIGMOID: "sigmoid",
    /**
     * Alias for {@link FuzzyShape.SIGMOID}
     */
    SMOOTH: "sigmoid",
    /**
     * The transition has a "bell" shape, using the gaussian function.
     */
    GAUSSIAN: "gaussian",
    /**
     * Alias for {@link FuzzyShape.GAUSSIAN}
     */
    BELL: "gaussian",
    /**
     * Alias for {@link FuzzyShape.REVERSED_GAUSSIAN}
     */
    REVERSED_BELL: "reversed_gaussian",
    /**
     * The transition has a "reversed bell" shape, using the gaussian function.
     */
    REVERSED_GAUSSIAN: "reversed_gaussian"
}


/**
    * Enum of the algorithms to use in the {@link FuzzyLogic} engine.
    * @namespace
    */
FuzzyLogicAlgorithm = {
    /**
     * Uses Zadeh's method, resulting in a linear logic.
     */
    LINEAR: 0,
    /**
     * Uses Hyperbolic Parabloid logic, which is a bit heavier than linear, but may have more intuitive results.
     */
    HYPERBOLIC: 1
}

/**
    * Enum of the algorithms to use when crispifying values.
    * @namespace
    */
FuzzyCrispAlgorithm = {
    /**
     * Uses the centroid method: combines all sets and values and gets the centroid.<br />
     * This method works great to combine more than a couple of rules, but will not work with single rules.
     */
    CENTROID: 0,
    /**
     * When several values are possible from each set, prefer the lowest one, then combine them to get the centroid.<br />
     * This method works like the centroid and works well even with single rules, but the returned values will tend to be a bit lower.
     */
    CENTROID_LOWER: 1,
    /**
     * When several values are possible from each set, prefer the highest one, then combine them to get the centroid.<br />
     * This method works like the centroid and works well even with single rules, but the returned values will tend to be a bit higher.
     */
    CENTROID_HIGHER: 2,
    /**
     * NOT IMPLEMENTED YET
     * Returns a randomly chosen value from all possible values. 
     */
    RANDOM: 3,
    /**
     * NOT IMPLEMENTED YET
     * Returns a randomly chosen value from all possible values from the set with the highest veracity. 
     */ 
    RANDOM_TRUE: 4,
    /**
     * NOT IMPLEMENTED YET
     * Returns a single random value from each set then combines them to get the centroid.
     */ 
    RANDOM_CENTROID: 5,
    /**
     * Returns the mean value from all possible values from all the sets.<br />
     * Unlike the centroid methods, the mean method does not take the veracity of each set into account.
     */
    MEAN: 6,
    /**
     * Returns the mean value from all the highest possible values from all the sets.<br />
     * Unlike the centroid methods, the mean method does not take the veracity of each set into account.
     */
    MEAN_HIGHER: 7,
    /**
     * Returns the mean value from all the lowest possible values from all the sets.<br />
     * Unlike the centroid methods, the mean method does not take the veracity of each set into account.
     */
    MEAN_LOWER: 8
}
