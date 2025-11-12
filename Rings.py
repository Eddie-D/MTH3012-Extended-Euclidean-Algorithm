class Zn :
    def __init__ (self, n, value) :
        self.n = n
        self.value = int(value) % n

    def checkArithMatch(self, other) :
        if (self.n != other.n) : raise Exception("Modular arithmetic mismatch")
    
    def __add__ (self, other) :
        self.checkArithMatch(other)
        return Zn(self.n, self.value + other.value)
    
    def __sub__ (self, other) :
        self.checkArithMatch(other)
        return Zn(self.n, self.value - other.value)
    
    def __mul__ (self, other) :
        self.checkArithMatch(other)
        return Zn(self.n, self.value * other.value)
    
    def __str__ (self) :
        return str(self.value)
