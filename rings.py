from math import gcd
from extended_euclidean import euclidean_algorithm
import operator

# We qualify rings by their strongest property. We assign integer strengths. Then if we need a property we check less than or equality.
# We will pass in strengths at initialisation, eg to create a euclidean domain polynomial ring, we need to 
# Helper function to get data from console
def tillValid(GetElement, repeatMessage) :
    valid = False
    while not valid :
        valid = True
        try :
            e = GetElement()
        except KeyboardInterrupt:
            # We want keyboard interrupt to still exit the script
            raise KeyboardInterrupt
        except:
            # If we have invalid input in GetElement
           print(repeatMessage)
           valid = False
    return e

def getField() :
   while True :
        print("Please choose a field to operate over (Frac[E] (Fractions over a Euclidean Domain), Z/p (Integers mod P))")
        choice = input()
        match choice.lower() :
            case "z/p" | "zp" :
                return ZpRing()
            case "q" | "frac" | "e" | "f" | "fr" | "fe" | "frac[e]" | "frac(e)" :
                return FractionRing()
        print("That is not a valid ring")

def getEuclideanDomain() :
    while True :
        print("Please choose a Ring to operate in (Z (Integers), F[X] (Polynomials over a Field))")
        choice = input()
        match choice.lower() :
            case "z" :
                return IntegerRing

            case "f" | "f[x]" | "fx" | "f(x)":
                return PolyRing()
        print("That is not a valid ring")

class ZpRing :
    def __init__(self, p=None) :
        if not p :
            print("Please choose p for Z/p")
            p = tillValid(lambda: int(input()), "Please choose an integer mod p") 
        self.p = p
        self.unit = Zp(self.p, 1)
        self.zero = Zp(self.p, 0)

    def consoleElement (self) :
        return Zp(self.p, tillValid(lambda: int(input()), f"Please choose an integer mod {self.p}"))

class Zp:
    def __init__ (self, p, value) :
        self.p = p
        self.value = int(value) % p

    def check_arith_match(self, other) :
        if self.p != other.p : raise Exception("Modular arithmetic mismatch")
    
    def __add__ (self, other) :
        self.check_arith_match(other)
        return Zp(self.p, self.value + other.value)
    
    def __sub__ (self, other) :
        self.check_arith_match(other)
        return Zp(self.p, self.value - other.value)
    
    def __mul__ (self, other) :
        self.check_arith_match(other)
        return Zp(self.p, self.value * other.value)

    def __neg__ (self):
        return Zp(self.p, self.p - self.value)
    
    def __str__ (self) :
        return f"[{self.value}]_{{{self.p}}}"
    
    def __truediv__(self, other) :
        # Calculate the inverse by fermats little theorem
        self.check_arith_match(other)
        for _ in range(self.p - 2) :
            self *= other
        return self

    def __eq__(self, other):
        # Don't check arithmatch as we instead use n to check if values are equal
        return self.value == other.value and self.p == other.p


class FractionRing :
    def __init__(self, ring=None) :
        if not ring :
            ring = getEuclideanDomain()
        self.unit = Frac(ring, ring.unit, ring.unit)
        self.zero = Frac(ring, ring.zero, ring.unit)
        self.ring = ring

    def consoleElement (self) :
        if self.ring == IntegerRing :
            return tillValid(lambda: Frac(self.ring, *[int(x) for x in input().split("/")]), "Enter a fraction in the form X/Y for integers X and Y")

        else :
            print("Enter the numerator of the Fraction")
            num = self.ring.consoleElement()
            print("Enter the denominator of the Fraction")
            den = self.ring.consoleElement()
            return Frac(self.ring, num, den)

class Frac :
    def __init__ (self, ring, num, den) :
        if den == ring.zero : raise Exception("Fraction with denominator of zero")
        # Re-write the fraction as an irreducible
        self.ring = ring
        if num == ring.zero :
            self.num = ring.zero
            self.den = ring.unit
        else :
            gcd = euclidean_algorithm(ring, num, den)["gcd"]
            self.num, _ = ring.euclideanDivision(num, gcd)
            self.den, _ = ring.euclideanDivision(den, gcd)
    
    def __add__ (self, other) :
        return Frac(self.ring, self.num * other.den + other.num * self.den, self.den * other.den)

    def __sub__(self, other) :
        return Frac(self.ring, self.num * other.den - other.num * self.den, self.den * other.den)

    def __mul__(self, other) :
        return Frac(self.ring, self.num * other.num, self.den * other.den)

    def __neg__(self):
        return Frac(self.ring, -self.num, self.den) 

    def __truediv__(self, other) :
        return Frac(self.ring, self.num * other.den, self.den * other.num)
    
    def __str__(self) :
        if self.den == self.ring.unit : return str(self.num)
        else: return f"\\frac{{{self.num}}}{{{self.den}}}"

    def __eq__(self, other) :
        # Can check numerator and denominator equal as we store fractions uniquely as irreducibles with negatives ontop
        return self.num == other.num and self.den == other.den


# Ring of polynomials, Character is the letter used for the unknown and ring is the underlying ring
class PolyRing :
    def __init__(self, ring=None, character=None) :
        if not character :
            print("Enter a letter to represent the indeterminate (typically X)")
            def getChar() :
                c = input()
                if len(c) != 1 or not c.isalpha() :
                    raise Exception("Not a character")
                return c
            self.indeterminate = tillValid(getChar, "Enter an alphabetical character")
            
        ring = getField()

        self.ring = ring
        self.zero = Polynomial(ring, [ring.zero], self.indeterminate)
        self.unit = Polynomial(ring, [ring.unit], self.indeterminate)
    
    def consoleElement (self) :
        print("Enter a degree for the polynomial")
        degree = tillValid(lambda: int(input()), "Enter an integer degree")

        values = []
        for i in range(degree,-1,-1) :
            # Difficult to make gramatical sense
            print(f"Enter the coefficient for X^{i} by entering a ring value:")
            values.insert(0, self.ring.consoleElement())
        return Polynomial(self.ring, values, self.indeterminate)

    # The euclidean division over polynomials is polynomial long division
    def euclideanDivision(self, dividend, divisor) :
        remainder = dividend
        quotient = self.zero

        while(divisor.length() <= remainder.length()) :
            # Create constant polynomial of the division of the two highest coefficients
            mult = Polynomial(self.ring, [self.ring.zero for _ in range(remainder.length() - divisor.length())] + [remainder.highestCoeff() / divisor.highestCoeff()], self.indeterminate)
            remainder = remainder - (divisor * mult)
            quotient = quotient + mult

        return (quotient, remainder)

    # Not the traditional euclidean function in F[X] which is deg(f), but is a valid one nonetheless
    @staticmethod
    def euclideanFunction(p) :
        return p.length()
    
class Polynomial :
    # We store polynomials as a + bx + cx^2 + ... + dx^n = [a b c ... d] 
    def __init__(self, ring, values, indeterminate="X") :
        self.indeterminate = indeterminate
        self.ring = ring
        # Remove leading zeroes
        while len(values) > 0 and values[-1] == ring.zero:
            values.pop()
        self.values = values
    
    def length(self) :
        return len(self.values)

    def strTerm(self, coeff, pow) :
        if coeff == self.ring.zero:
            return ""
        elif pow >= 1:
            strCo = str(coeff) if coeff != self.ring.unit else ""
            strX = f"{self.indeterminate}^{{{pow}}}" if pow > 1 else f"{self.indeterminate}"
            return strCo + strX
        else :
            return str(coeff)

    def __str__(self) :
        if self.values == [] :
            # Return constant zero for zero polynomial
            return str(self.ring.zero)

        # Create string representation of polynomial 
        # TODO Check this is a smart implementation
        rVals = [self.values[-i] for i in range(1, self.length() + 1)]
        strP = [self.strTerm(rVals[i], len(rVals)-i-1) for i in range (0, len(rVals))]
        return " + ".join(filter(lambda s: s != "", strP))

    # We use coeffwise to simplify the other methods
    def coeffwise(self, other, op) :
        length = max(self.length(), other.length())

        def withLeadingZeroes(l, length) :
            # Add leading zeroes till the list goes up to the desired length
            return l + [self.ring.zero for _ in range(length - len(l))]
        
        p1, p2 = withLeadingZeroes(self.values, length), withLeadingZeroes(other.values, length)
        return Polynomial(self.ring, [op(p1[i], p2[i]) for i in range(length)], self.indeterminate)
        
    def __add__ (self, other) :
        return self.coeffwise(other, operator.add)

    def __sub__(self, other) :
        return self.coeffwise(other, operator.sub)
    
    def __mul__(self, other) :
        total = Polynomial(self.ring, [self.ring.zero], self.indeterminate)
        for i, x in enumerate(self.values) :
            total = total + Polynomial(self.ring, [self.ring.zero for _ in range(i)] + [x*y for y in other.values], self.indeterminate)
            # print(f"Total: {total}")
        return total
    
    def __eq__(self, other) :
        # Efficient for polynomials of different lengths
        if self.length() != other.length() :
            return False
        # Iterate over self and other simultaneously
        for x, y in zip(self.values, other.values) :
            if x != y :
                return False
        return True

    def __neg__(self) :
        return Polynomial(self.ring, [-x for x in self.values], self.indeterminate)
    
    def highestCoeff(self) :
        return self.values[-1] if self.length() > 0 else self.ring.zero #Check zero is the reasonable return

# IntegerRing is static as it doesn't need paramaters at initialisation
class IntegerRing :
    zero = 0
    unit = 1
    @staticmethod
    def consoleElement() :
        return tillValid(lambda: int(input()), f"Please choose an integer")
    
    @staticmethod
    def euclideanFunction(x) :
        return abs(x)
    
    @staticmethod
    def euclideanDivision(x,y) :
        return (x // y, x % y)
