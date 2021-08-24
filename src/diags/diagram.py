from src.diags.propagator import FullPropagator

class Diagram:
    def __init__(self, coefs, cis, qs):
        self.coef = coefs
        self.ci = cis[:] # I need this otherwise cis gets modified....  what????
        self.props = []
        for p in range(0,len(qs)//2):
            self.props.append(FullPropagator(qs[2*p],qs[2*p+1]))
        ### Since all these diagrams are commuting, let's sort them, this will
        ### make comparisons across various diagrams much easier.
        self.ci=sorted(self.ci)
        #self.props=sorted(self.props)

    def __str__(self):
        ci_str = ''.join([str(c) for c in self.ci])
        prop_str = ''.join([str(p) for p in self.props])
        return str(self.coef) + ' ' + ci_str + prop_str

    def __eq__(self, other):
        return (self.coef == other.coef) and (self.ci==other.ci) and (self.props==other.props)

    def equivalent(self, other):
        return (self.ci==other.ci) and (self.props==other.props)
