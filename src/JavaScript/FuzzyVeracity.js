
/**
 * @class
 * @classdesc FuzzyVeracity is the fuzzy equivalent of a crisp boolean in boolean logic. It represents the result of logical operations (IS, AND, OR...).<br />
 * Its value can vary in the range [0.0, 1.0], 0.0 being the equivalent of "false" and 1.0 of "true".<br />
 * You can use it without other fuzzy logic components for simple cases, where you just need to combine several input values (ratios) to get a single output ratio.<br />
 * You can acces logic operators through instances of this class, which enable fluent syntax for rules (Except IS and IS_NOT which are members of {@link FuzzyValue}).<br />
 * Operators are methods in upper case.
 * @example
 * // A first "veracity", which usually is a specific input variable, converted to a ratio in [0.0, 1.0]
 * var firstValue = new FuzzyVeracity(0.2)
 * // A second "veracity"
 * var secondValue = new FuzzyVeracity(0.7);
 * // Combine both values to get a new ratio
 * var result = firstValue.AND( secondValue );
 * var outputRatio = result.veracity;
 * // The default algorithm is Zadeh's method, which is linear.
 * // Using an hyperbolic algorrithm may yield more intuitive and fine results, pass it to all FuzzyVeracity constructor:
 * var firstValue = new FuzzyVeracity(0.2, FuzzyLogicAlgorithm.HYPERBOLIC );
 * var secondValue = new FuzzyVeracity(0.7, FuzzyLogicAlgorithm.HYPERBOLIC );
 * @property {Number} veracity The veracity level in the range [0.0, 1.0]. 0.0 is equivelent to the boolean <code>false</code>, 1.0 is <code>true</code>
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
 
     var v = (1-weight)*x +  weight*y;
 
     return new FuzzyVeracity( v );
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
