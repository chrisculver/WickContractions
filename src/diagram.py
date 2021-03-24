from src.operators import Full_Propagator, Epsilon_Tensor
from src.wick_utilities import permutations

class Diagram:
    def __init__(self, coefs, cis, qs):
        self.coef = coefs
        self.ci = cis[:] # I need this otherwise cis gets modified....  what????
        for p in range(0,len(qs)//2):
            self.ci.append(Full_Propagator(qs[2*p],qs[2*p+1]))
        ### Since all these diagrams are commuting, let's sort them, this will
        ### make comparisons across various diagrams much easier.
        self.ci=sorted(self.ci)

    def __str__(self):
        ci_str = ''.join([str(c) for c in self.ci])
        return str(self.coef) + ' ' + ci_str

    def __eq__(self, other):
        return (self.coef == other.coef) and (self.ci==other.ci)

    #check whether or not two diagrams are related by any of the symmetries
    #provided, we allow a flexible list, since there's no point in using properties
    #of the epsilon tensor if there are no epsilon tensors. 
    def equivalent_to(self,other,symmetries):
        ## all objects in a diagram are sorted.
        ## We only have to look for symmetries/label swapping.
        for sym in symmetries():
            sother = sym(other)
            if(self.ci == sother.ci):
                return sother.coef

        return 0

"""
    def relabel_colors(self):
        epsilons = []
        for c in self.ci:
            if(type(c)==Epsilon_Tensor):
                epsilons.append(c)

        start_labels = [ e.get_labels() for e in epsilons ]

        relabeled = []

        for labels in start_labels:
            for p in permutations(labels):
"""
