from rings import IntegerRing, ZpRing, FractionRing, PolyRing
from extended_euclidean import extended_euclidean_algorithm
import os

# Setup ring-specific variables
ring = None
while not ring :
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

path = "./ExtendedEuclideanOutput.md"
# Delete the file if it already exists as it will be replaced
if os.path.exists(path) :
    os.remove(path)

# Open a file appender
writer = open(path, "w")
writer.write("# Extended Euclidean Algorithm \n")
extended_euclidean_algorithm(ring, e1, e2, writer=writer)
writer.close()
