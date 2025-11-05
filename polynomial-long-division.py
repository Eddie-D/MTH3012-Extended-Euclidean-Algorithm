# We will use operator overloading to represent rings where we overload so that a ring R has operations + and * 

# We create classes for the different types of rings
from functools import partial

class Zn :
    def __init__ (self, n, value) :
        self.n = n
        self.value = int(value) % n
    
    def checkArithMatch(self, other) :
        if (self.n != other.n) : raise Exception("Modular arithmetic mismatch")
    
    def __add__ (self, other) :
        self.checkArithMatch(other)
        return Zn(n, (self.value + other.value) % n)
    
    def __sub__ (self, other) :
        self.checkArithMatch(other)
        return Zn(n, (self.value - other.value) % n)
    
    def __mul__ (self, other) :
        self.checkArithMatch(other)
        return Zn(n, (self.value * other.value) % n)
    
    def __str__ (self) :
        return str(self.value)


# ASSUME FOR NOW THAT DIVISOR IS MONIC!
print("Please choose a ring to operate in (R, Z/n)")
choice = input()

if(choice == "Z/n") :
    print("Please choose N")
    n = int(input())
    # Define the ring specifically for our N
    ring = partial(Zn, n) 

if(choice == "R") :
    ring = int

print("Please enter the coefficients for the dividend")
dividend = [ring(x) for x in input().split(' ')]

print("Please enter the coefficients for the divisor")
divisor = [ring(x) for x in input().split(' ')]
quotient = []

def destroyLeading() :
    mult = dividend[0]
    for i in range(len(divisor)) :
        dividend[i] = dividend[i] - (divisor[i] * mult)
    dividend.pop(0)
    quotient.append(mult)

while(len(divisor) <= len(dividend)) :
    destroyLeading()
    
print("The quotient is: ", [str(x) for x in quotient])
print("The remainder is: ", [str(x) for x in dividend])