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
        self.indices.rotate(1)

    def __str__(self):
        """String printer
        """
        idx_str = ''.join([idx+' ' for idx in self.indices])
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


class EpsilonTensor(IndexedObject):
    def __init__(self,indices):
        self.name = 'eps'
        self.indices = [i for i in indices]

    def get_permutations(self):
        return [  Epsilon_Tensor(perm)
                    for perm in permutations(self.indices)  ]

    #return +1/-1 if eps is a even/odd permutation, 0 if not.
    def sign_of_permutation(self, eps):
        if( eps in self.get_permutations() ):
            #[ print(idx) for idx in eps.indices ]
            #[ print(idx) for idx in self.indices ]
            return (1 if arePermsEqualParity(eps.indices, self.indices) else -1)
        else:
            return 0

    def get_labels(self):
        return [ i for i in indices ]


class SpinMatrix(IndexedObject):
    def __init__(self,name,indices):
        self.name = name
        self.indices = [i for i in indices]