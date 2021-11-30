from WickContractions.corrs.propagator import FullPropagator

class Diagram:
    """Container for the commuting objects and propagators that need to be
        computed after wick contractions.  The correlation function is a linear
        combination of diagrams.  Either quarks or propagators could be
        passed to the correlator but not both.
        :param coef: Diagram coefficient
        :param commuting: Commuting objectings
        :param qs: List of quarks to turn into propagators
        :param props: List of propagators (should only be used for testing)
    """
    def __init__(self, coef, commuting, qs=[], props=[]):
        """Constructor
        """
        self.coef = coef
        self.commuting = commuting[:] # I need this otherwise cis gets modified....  what????

        if qs!=[]:
            self.props = []
            for p in range(0,len(qs)//2):
                self.props.append(FullPropagator(qs[2*p],qs[2*p+1]))
        elif props!=[]:
            self.props=props
        else:
            raise ValueError("Either qs or props must be passed to Diagram constructor")

        ### Since all these diagrams are commuting, let's sort them, this will
        ### make comparisons across various diagrams much easier.
        self.commuting=sorted(self.commuting)
        #self.props=sorted(self.props)

    def __str__(self):
        """Printer to str
        """
        ci_str = ''.join([str(c) for c in self.commuting])
        prop_str = ''.join([str(p) for p in self.props])
        return str(self.coef) + ' ' + ci_str + prop_str

    def __eq__(self, other):
        """Equality comparison
        """
        return (self.coef == other.coef) and (self.commuting==other.commuting) and (self.props==other.props)
