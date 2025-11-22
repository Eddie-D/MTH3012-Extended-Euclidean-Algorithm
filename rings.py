from math import gcd
import operator

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

    def checkArithMatch(self, other) :
        if (self.p != other.p) : raise Exception("Modular arithmetic mismatch")
    
    def __add__ (self, other) :
        # print(f"Zp adding, self: {self}, other: {other}, yields: {Zp(self.p, self.value + other.value)}")
        self.checkArithMatch(other)
        return Zp(self.p, self.value + other.value)
    
    def __sub__ (self, other) :
        self.checkArithMatch(other)
        return Zp(self.p, self.value - other.value)
    
    def __mul__ (self, other) :
        self.checkArithMatch(other)
        return Zp(self.p, self.value * other.value)

    def __neg__ (self):
        return Zp(self.p, self.p - self.value)
    
    def __str__ (self) :
        return f"[{self.value}]_{{{self.p}}}"
    
    def __truediv__(self, other) :
        # Calculate the inverse by fermats little theorem
        self.checkArithMatch(other)
        for i in range(self.p - 2) :
            self *= other
        return self

    def __eq__(self, other):
        # Don't check arithmatch as we instead use n to check if values are equal
        return self.value == other.value and self.p == other.p

class Frac :
    def __init__ (self, num, den=1) :
        if den == 0 : raise Exception("Fraction with denominator of zero")
        # Re-write the fraction as an irreducible
        # Ensure den is non-negative (solves issue of -1/-1 instead of 1/1)
        factor = (1 if den > 0 else -1) * gcd(num, den)
        self.num = int(num / factor)
        self.den = int(den / factor)
    
    def __add__ (self, other) :
        return Frac(self.num * other.den + other.num * self.den, self.den * other.den)

    def __sub__(self, other) :
        return Frac(self.num * other.den - other.num * self.den, self.den * other.den)

    def __mul__(self, other) :
        return Frac(self.num * other.num, self.den * other.den)

    def __neg__(self):
        return Frac(-self.num, self.den) 

    def __truediv__(self, other) :
        return Frac(self.num * other.den, self.den * other.num)
    
    def __str__(self) :
        if self.den == 1 : return str(self.num)
        else: return f"\\frac{{{self.num}}}{{{self.den}}}"

    def __eq__(self, other) :
        # Can check numerator and denominator equal as we store fractions uniquely as irreducibles with negatives ontop
        return self.num == other.num and self.den == other.den

# FractionRing is static as it doesn't need paramaters at initialisation (here fractions are only over the integers, not an integral domain)
class FractionRing :
    zero = Frac(0,1)
    unit = Frac(1,1)
    @staticmethod
    def consoleElement () :
        return tillValid(lambda: Frac(*[int(x) for x in input().split("/")]), "Enter a fraction in the form X/Y for integers X and Y")


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
            
        if not ring :
            while(not ring) :
                print("Please choose a field to operate over (Q, Z/p)")
                choice = input()
                match choice.lower() :
                    case "z" :
                        ring = IntegerRing

                    case "z/p" | "zp" :
                        # Define the ring
                        ring = ZpRing()
                    case "q" :
                        ring = FractionRing()
                        # Instantiation not necessary (assumed over integers)
                        ring = FractionRing

                    case "f" | "f[X]" | "fx" | "f(x)":
                        ring = PolyRing()
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
            arr1 = [self.ring.zero for _ in range(remainder.length() - divisor.length())]
            arr2 = [remainder.highestCoeff() / divisor.highestCoeff()]
            arr = arr1 + arr2
            print(f"Mult: {mult}")
            print(f"Remainder: {remainder}, Mult: {mult}, Divisor: {divisor}")
            print(f"Divisor*mult: {divisor*mult}")
            # print("Mult:" + str(mult) + "  Remainder: " + str(remainder[0]) + "  Divisor: " + str(divisor[0]))
            remainder = remainder - (divisor * mult)
            quotient = quotient + mult

        return (quotient, remainder)

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
    
    
    # Not the traditional euclidean function in F[X] which is deg(f), but is a valid one nonetheless
    def euclideanFunction(self) :
        return self.length()
    
    def highestCoeff(self) :
        return self.values[-1] if self.length() > 0 else self.ring.zero #Check zero is the reasonable return


# IntegerRing is static as it doesn't need paramaters at initialisation
class IntegerRing :
    zero = 0
    unit = 1
    @staticmethod
    def consoleElement() :
        return tillValid(lambda: int(input()), f"Please choose an integer") 
