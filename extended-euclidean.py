# We will use operator overloading to represent rings where we overload so that a ring R has operations + and * 

# We create classes for the different types of rings
import numpy as np
from rings import IntegerRing, ZpRing, FractionRing, PolyRing

# We impose the following qualities on our ring objects:
# Implementation of *, + and -
# Implementation of a 'fromConsole' method that allows the user to input the ring element (this is enforced mostly so matrices can blend in)

# ASSUME FOR NOW THAT DIVISOR IS MONIC!
'''
def getUserMatrix(n) :
    rows = []
    for i in range(n) :
        print("Please enter the values for row", i)
        tillValid(lambda: rows.append([int(x) for x in input().split(' ')]), "Please enter the integer values separated by spaces")
    return np.matrix(rows)
'''

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

        case "q" :
            ring = FractionRing()

        case "mn" | "m":
            pass

        case "f" | "f[X]" | "fx" | "f(x)":
            ring = PolyRing()

print("Enter the two elements to run the Extended Euclidean Algorithm on")
print("Enter the first element:")
e1 = ring.consoleElement()

print("Enter the second element:")
e2 = ring.consoleElement()

# Assign divisor and dividend where 0 keeps track of the originals
dividend0, divisor0 = (e1, e2) if e1.euclideanFunction() >= e2.euclideanFunction() else (e2, e1)
dividend, divisor = dividend0, divisor0

md = open("ExtendedEuclideanOutput.md", "w")
md.write("# Extended Euclidean Algorithm \n")
md.write(f"### We find the gcd of ${divisor0}$ and ${dividend0}$\n\n")
results = []
remainder = None

while (remainder is None or remainder != ring.zero) :
    quotient, remainder = ring.euclideanDivision(dividend, divisor)
    results.append([dividend, quotient, divisor])

    s = f"1. ${dividend} = ({quotient})({divisor}) + ({remainder})$"
    md.write(s + "\n\n")

    dividend = divisor
    divisor = remainder

gcd = dividend
md.write(f"Overall the gcd is ${gcd}$\n\n")

md.write(f"### We use the Extended Euclidean algorithm to find coefficients $\lambda$, $\mu$ s.t. $\lambda ({dividend0}) + \mu ({divisor0}) = {gcd}$\n\n")

# Remove result with zero remainder
results.reverse()
results.pop(0)

def extendedEuclidean(n) :
    dividend, quotient, divisor = results[n]
    if n == 0 :
        lamb, mu = ring.unit, -quotient
    else :
        # Swap and calculate new mu
        mu, lamb = extendedEuclidean(n-1)
        mu = mu - (quotient * lamb)

    md.write(f"1. ${gcd} = ({lamb})({dividend}) + ({mu})({divisor})$\n\n")
    return (lamb, mu)

if(len(results) != 0) :
    lamb, mu = extendedEuclidean(len(results) - 1)
else :
    # In trivial case where mu divides lambda we do need the division with zero remainder
    lamb, mu = ring.euclideanDivision(dividend0, divisor0)

md.write(f"### Overall we have: $\lambda = ({lamb})$ and $\mu = ({mu})$\n\n")

print(f"Checksum, {gcd} = {(lamb*dividend0) + (mu*divisor0)}")
