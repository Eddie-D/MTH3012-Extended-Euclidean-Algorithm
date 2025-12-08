# We will use operator overloading to represent rings where we overload so that a ring R has operations + and * 

# We create classes for the different types of rings

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

def euclidean_algorithm(ring, e1, e2, writer=""):
    # Assign divisor and dividend where 0 keeps track of the originals
    dividend0, divisor0 = (e1, e2) if e1.euclideanFunction() >= e2.euclideanFunction() else (e2, e1)
    dividend, divisor = dividend0, divisor0

    if writer :
        writer.write(f"### We use the Euclidean Algorithm to find the gcd of ${divisor0}$ and ${dividend0}$\n\n")
    results = []
    remainder = None

    while (remainder is None or remainder != ring.zero) :
        quotient, remainder = ring.euclideanDivision(dividend, divisor)
        results.append([dividend, quotient, divisor])

        if writer :
            writer.write(f"1. ${dividend} = ({quotient})({divisor}) + ({remainder})$\n\n")

        dividend = divisor
        divisor = remainder

    gcd = dividend
    if writer :
        writer.write(f"Overall the gcd is ${gcd}$\n\n")

    return { "gcd":gcd, "results":results }

def extended_euclidean_algorithm(ring, e1, e2, writer="") :
    euclid = euclidean_algorithm(ring, e1, e2, writer)
    gcd, results = euclid["gcd"], euclid["results"]
    dividend0, divisor0 = (e1, e2) if e1.euclideanFunction() >= e2.euclideanFunction() else (e2, e1)

    if writer :
        writer.write(f"### We use the Extended Euclidean algorithm to find coefficients $\lambda$, $\mu$ s.t. $\lambda ({dividend0}) + \mu ({divisor0}) = {gcd}$\n\n")
        
    # Remove result with zero remainder
    results.reverse()
    results.pop(0)

    # Design is discussed in the report
    def extended_euclidean(n) :
        dividend, quotient, divisor = results[n]
        if n == 0 :
            lamb, mu = ring.unit, -quotient
        else :
            # Swap and calculate new mu
            mu, lamb = extended_euclidean(n-1)
            mu = mu - (quotient * lamb)

        if writer :
            writer.write(f"1. ${gcd} = ({lamb})({dividend}) + ({mu})({divisor})$\n\n")
        return (lamb, mu)

    if(len(results) != 0) :
        lamb, mu = extended_euclidean(len(results) - 1)
    else :
        # In trivial case where mu divides lambda we do need the division with zero remainder
        lamb, mu = ring.euclideanDivision(dividend0, divisor0)

    if writer:
        writer.write(f"### Overall we have: $\lambda = ({lamb})$ and $\mu = ({mu})$\n\n")

    print(f"Checksum, {gcd} = {(lamb*dividend0) + (mu*divisor0)}")
