#ShortQuark class used to efficiently store the minimal amount of information
#needed to do wick contractions
class ShortQuark:
    def __init__(self, b, f, l):
        self.barred=b ##is anti-quark?
        self.flavor=f
        self.label=l

    def __str__(self):
        if self.barred:
            return "\\bar{" + str(self.flavor) + "}" + "_" + str(self.label)
        else:
            return str(self.flavor) + "_" + str(self.label)

class Quark:
    def __init__(self, b, f, s, c, t, x):
        self.barred=b ##is anti-quark
        self.flavor=f
        self.spin=s
        self.color=c
        self.time=t
        self.position = x

    def __str__(self):
        if self.barred:
            return "\\bar{" + str(self.flavor) + "}" + "_{" + str(self.spin) + " " +  str(self.color) + " " + str(self.time) + "}"
        else:
            return str(self.flavor) + "_{" + str(self.spin) + " " +  str(self.color) + " " + str(self.time) + "}"

    def __eq__(self, other):
        return (self.barred==other.barred) and (self.flavor==other.flavor) and (self.spin==other.spin) and (self.color==other.color)
