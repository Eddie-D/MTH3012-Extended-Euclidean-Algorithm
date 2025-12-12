from rings import getEuclideanDomain
from extended_euclidean import extended_euclidean_algorithm
import os

# Setup ring-specific variables
ring = getEuclideanDomain()

print("Enter the two elements to run the Extended Euclidean Algorithm on")
print("Enter the first element:")
e1 = ring.console_element()

print("Enter the second element:")
e2 = ring.console_element()

path = "./ExtendedEuclideanOutput.tex"
# Delete the file if it already exists as it will be replaced
if os.path.exists(path) :
    os.remove(path)

# Open a file appender
writer = open(path, "w")
writer.write("\\textbf{Extended Euclidean Algorithm,} \\\\\n")
extended_euclidean_algorithm(ring, e1, e2, writer=writer)
print("Extended Euclidean Algorithm Completed successfully, see ExtendedEuclideanOutput.tex")
writer.close()
