#TODO this should probably inherit from IndexedFunction?
class FullPropagator():
    """Container for all dependencies of a propagator
        :param q: The quark
        :param qbar: The antiquark
    """
    def __init__(self,q,qbar):
        """Constructor
        """
        self.name = 'prop^'+q.flavor
        self.left_indices=PropIndex(q.color,q.spin)
        self.right_indices=PropIndex(qbar.color,qbar.spin)
        self.ti = q.time
        self.xi = q.position
        self.tf = qbar.time
        self.xf = qbar.position

    def __str__(self):
        """String printer
        """
        return self.name + '(' + self.xi + self.ti + '\\mid ' + self.xf + self.tf + ')' + '_{\\substack{' + self.left_indices.s + '\\\\' + self.left_indices.c + '}' +  '\\substack{' + self.right_indices.s + '\\\\' + self.right_indices.c + '}}'

    def __eq__(self,other):
        """Equality comparison
        """
        return self.name==other.name and self.left_indices==other.left_indices and self.right_indices==other.right_indices and self.ti==other.ti and self.tf==other.tf

#TODO this is probably overkill, just remove it...
class PropIndex():
    """Container for color and string of propagator
        :param c: color
        :param s: spin
    """
    def __init__(self,c,s):
        """Constructor
        """
        self.c=c
        self.s=s
    def __str__(self):
        """String printer
        """
        return self.c + ' ' + self.s
    def __eq__(self,other):
        """Equality comparison
        """
        return self.c==other.c and self.s==other.s
