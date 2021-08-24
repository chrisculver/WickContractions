class IndexedObject:
    def __init__(self,name,indices):
        self.name = name
        self.indices = indices

    def cyclic_permute_indices(self):
        self.indices.rotate(1)

    def __str__(self):
        idx_str = ''.join([idx+' ' for idx in self.indices])
        return self.name + '_{' + idx_str + '}'

    def __eq__(self, other):
        return (self.name == other.name) and (self.indices==other.indices)

    def __lt__(self, other):
        if(self.name != other.name):
            return (self.name < other.name)
        else:
            return (self.indices < other.indices)


class IndexedFunction(IndexedObject):
    def __init__(self, name, indices, arguments):
        self.name = name
        self.indices = indices
        self.arguments = arguments

    def __str__(self):
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
        return (self.name == other.name) and (self.indices==other.indices) and (self.arguments==self.arguments)

    def __lt__(self, other):
        if(self.name != other.name):
            return (self.name < other.name)
        else:
            self_strings = self.indices + self.arguments
            other_strings = other.indices + other.arguments
            return (self_strings < other_strings)
