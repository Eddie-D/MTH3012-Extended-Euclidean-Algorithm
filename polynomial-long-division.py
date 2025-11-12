# We will use operator overloading to represent rings where we overload so that a ring R has operations + and * 

# We create classes for the different types of rings
import numpy as np
from functools import partial
from Rings import Zn

# We impose the following qualities on our ring objects:
# Implementation of *, + and -
# Implementation of a 'fromConsole' method that allows the user to input the ring element (this is enforced mostly so matrices can blend in)

# ASSUME FOR NOW THAT DIVISOR IS MONIC!

def getUserMatrix(n) :
    rows = []
    for i in range(n) :
        print("Please enter the values for row", i)
        rows.append([int(x) for x in input().split(' ')])
    return np.matrix(rows)

fromConsole = None
while(not fromConsole) :
    print("Please choose a ring to operate in (Z, Z/n, Mn)")
    choice = input()
    match choice.lower() :
        case "z/n" | "zn":
            print("Please choose n for Z/n")
            n = int(input())
            # Define the ring specifically for our N
            fromConsole = lambda: Zn(n, int(input()))
        
        case "z" :
            fromConsole = lambda: int(input())

        case "mn" | "m":
            print("Please choose n")
            n = int(input())
            fromConsole = lambda: getUserMatrix(n)


print("Please enter the degree of the dividend")
degree = int(input())
dividend = []
for i in range(degree,-1,-1) :
    print("Please enter the coefficient for X^", i)
    dividend.append(fromConsole())

print("Please enter the degree of the divisor")
degree = int(input())
divisor = []
for i in range(degree,-1,-1) :
    print("Please enter the coefficients for X^", i)
    divisor.append(fromConsole())

def polyLongDivide(dividend, divisor) :
    remainder = list.copy(dividend)
    quotient = []

    def destroyLeading() :
        mult = remainder[0]
        for i in range(len(divisor)) :
            remainder[i] = remainder[i] - (divisor[i] * mult)
        remainder.pop(0)
        quotient.append(mult)

    while(len(divisor) <= len(remainder)) :
        destroyLeading()
    return (quotient, remainder)

quotient, remainder = polyLongDivide(dividend, divisor)

print("The quotient is: ", [str(x) for x in quotient])
print("The remainder is: ", [str(x) for x in remainder])