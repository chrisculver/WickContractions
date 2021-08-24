

class ElementalOperator:
    """ An :class:`src.ops.Operator` is a linear combination of elementals.
        :param coef: Coefficient of this term.
        :type coef: double
        :param commuting: List of commuting objects within the elemental
        :type commuting: List containing many different types, must be printable to str
        :param quarks: List of quarks in the operators
        :type quarks: List of `src.ops.quark`
    """
    def __init__(self, coef, commuting, quarks):
        """Constructor
        """
        self.coef=coef
        self.commuting=commuting
        self.quarks=quarks

    def __str__(self):
        """Printing to string
        """
        cStr="*"
        for c in commuting[:-1]:
            cStr+=str(c)+"*"
        cStr+=str(commuting[-1])
        qStr=""
        for q in quarks[:-1]:
            qStr+=str(q)+"*"
        qStr+=str(quarks[-1])
        return str(coef)+cStr+qStr
