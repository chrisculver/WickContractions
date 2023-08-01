

class Operator:
    """ An operator is a linear combination of :class:`src.ops.ElementalOperator`.
        :param elementals: The elementals that create the operator
        :type elementals: List of :class:`src.ops.ElementalOperator`
    """
    def __init__(self, elementals):
        """Constructor
        """
        self.elementals=elementals

    def __str__(self):
        """Printer to str
        """
        eStr=""
        for e in self.elementals[:-1]:
            eStr+=str(e)+"+"
        return eStr+str(self.elementals[-1])
    
    def get_gammas(self):
        gammas = []
        for c in self.elementals[0].commuting:
            if "\\Gamma" in c.name:
                gammas.append(c.name)
        return gammas