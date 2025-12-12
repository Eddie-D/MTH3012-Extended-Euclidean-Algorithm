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

def euclidean_algorithm(ring, e1, e2, writer=None) :
    # Assign divisor and dividend where 0 keeps track of the originals
    dividend0, divisor0 = (e1, e2) if ring.euclideanFunction(e1) >= ring.euclideanFunction(e2) else (e2, e1)
    dividend, divisor = dividend0, divisor0

    if writer :
        writer.write(f"\\textbf{{We use the Euclidean Algorithm to find the gcd of ${divisor0}$ and ${dividend0}$}} \\\\\n")
        writer.write("\\begin{align*} \n")
    results = []
    remainder = None

    while (remainder is None or remainder != ring.zero) :
        quotient, remainder = ring.euclideanDivision(dividend, divisor)
        results.append([dividend, quotient, divisor])

        if writer :
            writer.write(f"{dividend} &= ({quotient})({divisor}) + ({remainder})   \\\\\n")

        dividend = divisor
        divisor = remainder

    gcd = dividend
    if writer :
        writer.write("\\end{align*} \n")
        writer.write(f"\\textbf{{Overall the gcd is ${gcd}$}} \\\\\n")

    return { "gcd":gcd, "results":results }

def extended_euclidean_algorithm(ring, e1, e2, writer=None) :
    euclid = euclidean_algorithm(ring, e1, e2, writer)
    gcd, results = euclid["gcd"], euclid["results"]
    dividend0, divisor0 = (e1, e2) if ring.euclideanFunction(e1) >= ring.euclideanFunction(e2) else (e2, e1)

    # Remove result with zero remainder
    results.pop()

    # Design is discussed in the report
    def extended_euclidean(n) :
        dividend, quotient, divisor = results[n]
        if n == len(results) - 1 :
            lamb, mu = ring.unit, -quotient
        else :
            # Swap and calculate new mu
            mu, lamb = extended_euclidean(n+1)
            mu = mu - (quotient * lamb)

        if writer :
            writer.write(f"{gcd} &= ({lamb})({dividend}) + ({mu})({divisor})    \\\\\n")
        return (lamb, mu)

    if(len(results) != 0) :
        if writer :
            writer.write(f"\\textbf{{We use the Extended Euclidean algorithm to find coefficients $\lambda$, $\mu$ s.t. $\lambda ({dividend0}) + \mu ({divisor0}) = {gcd}$}} \\\\\n")
        writer.write("\\begin{align*} \n")
        
        lamb, mu = extended_euclidean(0)

        if writer:
            writer.write("\\end{align*} \n")
            writer.write(f"\\textbf{{Overall we have: $\lambda = ({lamb})$ and $\mu = ({mu})$}} \\\\\n")
    else :
        # In trivial case, mu is the gcd
        lamb, mu = ring.zero, ring.unit

        if writer :
            writer.write(f"\\textbf{{We have trivially that $({lamb})({dividend0}) + ({mu})({divisor0}) = {gcd}$}} \\\\\n")
