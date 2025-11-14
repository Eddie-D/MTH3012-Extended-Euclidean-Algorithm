# We will use operator overloading to represent rings where we overload so that a ring R has operations + and * 

# We create classes for the different types of rings
import numpy as np
from functools import partial
from rings import Zp, Frac

# We impose the following qualities on our ring objects:
# Implementation of *, + and -
# Implementation of a 'fromConsole' method that allows the user to input the ring element (this is enforced mostly so matrices can blend in)

# ASSUME FOR NOW THAT DIVISOR IS MONIC!

def getUserMatrix(n) :
    rows = []
    for i in range(n) :
        print("Please enter the values for row", i)
        tillValid(lambda: rows.append([int(x) for x in input().split(' ')]), "Please enter the integer values separated by spaces")
    return np.matrix(rows)

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

# Setup ring-specific variables
fromConsole = None
unit = None
zero = None

while(not fromConsole) :
    print("Please choose a field to operate in (Q, Z/p, Mn)")
    choice = input()
    match choice.lower() :
        case "z/p" | "zp" | "z":
            print("Please choose n for Z/n")
            n = int(input())
            # Define the ring specifically for our N
            fromConsole = lambda: tillValid(lambda: Zp(n, int(input())), "Please choose an integer mod p") 
            unit = Zp(n,1)
            zero = Zp(n,0)

        case "q" :
            fromConsole = lambda: tillValid(lambda: Frac(*[int(x) for x in input().split("/")]), "Enter a fraction in the form X/Y for integers X and Y")
            unit = Frac(1,1)
            zero = Frac(0,1)

        case "mn" | "m":
            print("Please choose n")
            n = tillValid(lambda: int(input()), "Enter an integer for the size of the square matrix")
            fromConsole = lambda: getUserMatrix(n)
            unit = np.identity(n)

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

# Performs polynomial long division assuming the underlying ring is a field.
def polyLongDivide(dividend, divisor) :
    remainder = list.copy(dividend)
    quotient = []

    def destroyLeading() :
        mult = remainder[0] / divisor[0]
        # print("Mult:" + str(mult) + "  Remainder: " + str(remainder[0]) + "  Divisor: " + str(divisor[0]))
        for i in range(len(divisor)) :
            remainder[i] = remainder[i] - (divisor[i] * mult)
        remainder.pop(0) # We can remove the first element as it will have cancelled
        quotient.append(mult)

    while(len(divisor) <= len(remainder)) :
        destroyLeading()

    return (quotient, remainder)

def strTerm(coeff, pow) :
    if coeff == zero :
        return ""
    elif pow >= 1:
        strCo = str(coeff) if coeff != unit else ""
        strX = f"X^{{{pow}}}" if pow > 1 else "X"
        return strCo + strX
    else :
        return str(coeff)

def strPoly(p) :
    if all(c == zero for c in p) :
        # Return constant zero if all coefficients are zero
        return str(zero)
    strP = [strTerm(p[i], len(p)-i-1) for i in range (0, len(p))]
    return " + ".join(filter(lambda s: s != "", strP))

md = open("ExtendedEuclideanOutput.md", "w")
md.write("# Extended Euclidean Algorithm \n")
md.write(f"### We find the gcd of ${strPoly(dividend)}$ and ${strPoly(divisor)}$\n\n")
results = []
while (len(divisor) > 0) :
    # Create the divisors monic associate
    # inverse = (unit / divisor[0])
    # divisor = [inverse * d for d in divisor]

    quotient, remainder = polyLongDivide(dividend, divisor)
    s = f"1. ${strPoly(dividend)} = ({strPoly(quotient)})({strPoly(divisor)}) + ({strPoly(remainder)})$"
    results.append([dividend, quotient, divisor, remainder])
    print(s)
    md.write(s + "\n\n")

    dividend = divisor
    divisor = remainder

    # Remove any leading zeroes
    while len(divisor) > 0 and divisor[0] == zero :
        divisor.pop(0)

monicMult = unit/(dividend[0])
gcd = [monicMult * d for d in dividend]
md.write(f"Overall the gcd is ${strPoly(dividend)}$ or as its monic associate, ${strPoly(gcd)}$\n\n")

md.write(f"### We use the Extended Euclidean algorithm to find coefficients $\mu$, $\lambda$ s.t. $\mu ({strPoly(dividend)}) + \lambda ({strPoly(divisor)}) = {strPoly(gcd)}$\n\n")
# print("$" + "$\n\n$".join(["$,$".join([strPoly(p) for p in r]) for r in results]) + "$")
# md.write("\n\n\n\n$" + "$\n\n$".join(["$,&nbsp;$".join([strPoly(p) for p in r]) for r in results]) + "$")

mu = monicMult
lam = unit
# Remove result with zero remainder
results.pop()
results.reverse()
for [dividend, quotient, divisor, remainder] in results :
    s = f"${strPoly(remainder)} = {strPoly(dividend)} - ({strPoly(quotient)})({strPoly(divisor)})$"
    md.write(f"{s}\n\n")

remainder = divided - (quotient * divisor)