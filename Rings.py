from math import gcd
import math

class Zp :
    def __init__ (self, n, value) :
        self.n = n
        self.value = int(value) % n

    def checkArithMatch(self, other) :
        if (self.n != other.n) : raise Exception("Modular arithmetic mismatch")
    
    def __add__ (self, other) :
        self.checkArithMatch(other)
        return Zp(self.n, self.value + other.value)
    
    def __sub__ (self, other) :
        self.checkArithMatch(other)
        return Zp(self.n, self.value - other.value)
    
    def __mul__ (self, other) :
        self.checkArithMatch(other)
        return Zp(self.n, self.value * other.value)
    
    def __str__ (self) :
        return f"[{self.value}]_{{{self.n}}}"
    
    def __truediv__(self, other) :
        # Calculate the inverse by fermats little theorem
        self.checkArithMatch(other)
        for i in range(self.n - 2) :
            self *= other
        return self

    def __eq__(self, other):
        # Don't check arithmatch as we instead use n to check if values are equal
        return self.value == other.value and self.n == other.n

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

    def __truediv__(self, other) :
        return Frac(self.num * other.den, self.den * other.num)
    
    def __str__(self) :
        if self.den == 1 : return str(self.num)
        else: return f"\\frac{{{self.num}}}{{{self.den}}}"

    def __eq__(self, other) :
        # Can check numerator and denominator equal as we store fractions uniquely as irreducibles with negatives ontop
        return self.num == other.num and self.den == other.den