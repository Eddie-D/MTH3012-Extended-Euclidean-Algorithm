from rings import IntegerRing, ZpRing, FractionRing, PolyRing, Polynomial, Zp

print("Sample Driver")
zRing = ZpRing(5)
ring = PolyRing(zRing)

p1 = Polynomial(zRing, [Zp(5, x) for x in [2, 4, 3, 1]])
p2 = Polynomial(zRing, [Zp(5,x) for x in [0, 3, 1, 1]])
print(f"p1: {p1}")
print(f"-p1: {-p1}")
print(f"p2: {p2}")
q,r = ring.euclideanDivision(p1, p2)

print(f"Division: Quo:{q}, Rem:{r}")