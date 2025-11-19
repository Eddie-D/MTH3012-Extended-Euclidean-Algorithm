# We will use operator overloading to represent rings where we overload so that a ring R has operations + and * 

# We create classes for the different types of rings
import numpy as np
from rings import IntegerRing, ZpRing, FractionRing, PolyRing

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



# Setup ring-specific variables
ring = None
while(not ring) :
    print("Please choose a Ring to operate in (Q, Z/p, Mn, F[X])")
    choice = input()
    match choice.lower() :
        case "z" :
            ring = IntegerRing

        case "z/p" | "zp" :
            ring = ZpRing()
            # Define the ring specifically for our N

            # fromConsole = lambda: tillValid(lambda: Zp(n, int(input())), "Please choose an integer mod p") 
            # unit = Zp(n,1)
            # zero = Zp(n,0)

        case "q" :
            ring = FractionRing()
            # fromConsole = lambda: tillValid(lambda: Frac(*[int(x) for x in input().split("/")]), "Enter a fraction in the form X/Y for integers X and Y")
            # unit = Frac(1,1)
            # zero = Frac(0,1)

        case "mn" | "m":
            pass
            # print("Please choose n")
            # n = tillValid(lambda: int(input()), "Enter an integer for the size of the square matrix")
            # fromConsole = lambda: getUserMatrix(n)
            # unit = np.identity(n)

        case "f" | "f[X]" | "fx" | "f(x)":
            ring = PolyRing()

print("Enter the two elements to run the Extended Euclidean Algorithm on")
print("Enter the first element:")
e1 = ring.consoleElement()

print("Enter the second element:")
e2 = ring.consoleElement()

# Assign divisor and dividend assuming
dividend, divisor = (e1, e2) if e1.euclideanFunction() >= e2.euclideanFunction() else (e2, e1)

md = open("ExtendedEuclideanOutput.md", "w")
md.write("# Extended Euclidean Algorithm \n")
md.write(f"### We find the gcd of ${e1}$ and ${e2}$\n\n")
results = []
remainder = None
while (remainder is None or remainder != ring.zero) :
    quotient, remainder = ring.euclideanDivision(dividend, divisor)
    print(f"Quotient: {quotient}, Remainder: {remainder}")
    s = f"1. ${dividend} = ({quotient})({divisor}) + ({remainder})$"
    results.append([dividend, quotient, divisor, remainder])
    print(s)
    md.write(s + "\n\n")

    dividend = divisor
    divisor = remainder

gcd = dividend
md.write(f"Overall the gcd is ${gcd}$\n\n")

md.write(f"### We use the Extended Euclidean algorithm to find coefficients $\mu$, $\lambda$ s.t. $\mu ({e1}) + \lambda ({e2}) = {gcd}$\n\n")
# print("$" + "$\n\n$".join(["$,$".join([strPoly(p) for p in r]) for r in results]) + "$")
# md.write("\n\n\n\n$" + "$\n\n$".join(["$,&nbsp;$".join([strPoly(p) for p in r]) for r in results]) + "$")

mu = ring.unit
lam = ring.unit
# Remove result with zero remainder
results.pop()
r, end, q, oor = results[0]
# Start at bottom for backwards substitution
results.reverse()

for [dividend, quotient, divisor, remainder] in results :
    t = f"{r} = {end} - ({q})({oor})"
    s = f"${remainder} = {dividend} - ({quotient})({divisor})$"
    oor = end
    end = (ring.zero - q) * dividend
    q = ring.unit + (q*quotient)
    print(f"The overall is : {end - (q * oor)}")
    md.write(f"${t}$\n\n")
