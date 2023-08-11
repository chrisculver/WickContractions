from collections import deque

class IndexedObject:
    """Container for an object that has indices
        :param name: Name of the object
        :param indices: Indices attached to it
    """
    def __init__(self,name,indices):
        """Constructor
        """
        self.name = name
        self.indices = indices

    def cyclic_permute_indices(self):
        """Return the object with it's indices cyclicly permuted once.
        """
        tmp=deque(self.indices)
        tmp.rotate(1)
        self.indices=list(tmp)

    def id(self):
        return self.name

    def __str__(self):
        """String printer
        """
        idx_str = ''
        for i in range(len(self.indices)):
            idx_str += self.indices[i]
            if(i!=len(self.indices)-1):
                idx_str += ' '
        return self.name + '_{' + idx_str + '}'

    def __eq__(self, other):
        """Equality comparison
        """
        return (self.name == other.name) and (self.indices==other.indices)

    def __lt__(self, other):
        """Less then operator
        """
        if(self.name != other.name):
            return (self.name < other.name)
        else:
            return (self.indices < other.indices)


class IndexedFunction(IndexedObject):
    """Container for an object with indices and arguments
        :param name: Name of the object
        :param indices: Indices attached to the argument
        :param arguments: Arguments the object depends on
    """
    def __init__(self, name, indices, arguments):
        """Constructor
        """
        self.name = name
        self.indices = indices
        self.arguments = arguments

    def __str__(self):
        """String printer
        """
        idx_str = ''
        for i in range(len(self.indices)):
            idx_str += self.indices[i]
            if(i!=len(self.indices)-1):
                idx_str += ' '
        arg_str = ''
        for i in range(len(self.arguments)):
            arg_str += self.arguments[i]
            if(i!=len(self.arguments)-1):
                arg_str += ','
        return self.name + '(' + arg_str + ')_{' + idx_str + '}'

    def __eq__(self, other):
        """Equality comparison
        """
        return (self.name == other.name) and (self.indices==other.indices) and (self.arguments==self.arguments)

    def __lt__(self, other):
        """Less then operator
        """
        if(self.name != other.name):
            return (self.name < other.name)
        else:
            self_strings = self.indices + self.arguments
            other_strings = other.indices + other.arguments
            return (self_strings < other_strings)

    def id(self):
        arg_str = ''
        for i in range(len(self.arguments)):
            arg_str += self.arguments[i]
            if(i!=len(self.arguments)-1):
                arg_str += ','
        
        return self.name + '(' + arg_str + ')'
        
