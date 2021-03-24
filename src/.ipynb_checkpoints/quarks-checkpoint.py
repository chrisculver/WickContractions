#ShortQuark class used to efficiently store the minimal amount of information
#needed to do wick contractions
class ShortQuark:
    def __init__(self, b, f, l):
        self.barred=b
        self.flavor=f
        self.label=l
 
    def __str__(self):
        if self.barred:
            return "\\bar{" + str(self.flavor) + "}" + "_" + str(self.label) 
        else:
            return str(self.flavor) + "_" + str(self.label)
        
class Quark:
    def __init__(self, b, f, s, c):
        self.barred=b
        self.flavor=f
        self.spin=s
        self.color=c
    
    def __str__(self):
        if self.barred:
            return "\\bar{" + str(self.flavor) + "}" + "_{" + str(self.spin) + " " +  str(self.color) + "}"
        else:
            return str(self.flavor) + "_{" + str(self.spin) + " " +  str(self.color) + "}"
        
    def __eq__(self, other):
        return (self.barred==other.barred) and (self.flavor==other.flavor) and (self.spin==other.spin) and (self.color==other.color)