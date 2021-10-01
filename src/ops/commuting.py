from src.ops.indexed import IndexedObject
from src.wick.utilities import permutations, arePermsEqualParity

class EpsilonTensor(IndexedObject):
    def __init__(self,indices):
        self.name = 'eps'
        self.indices = [i for i in indices]

    def get_permutations(self):
        return [  EpsilonTensor(perm)
                    for perm in permutations(self.indices)  ]

    #return +1/-1 if eps is a even/odd permutation, 0 if not.
    def sign_of_permutation(self, eps):
        if( eps in self.get_permutations() ):
            #[ print(idx) for idx in eps.indices ]
            #[ print(idx) for idx in self.indices ]
            return (1 if arePermsEqualParity(eps.indices, self.indices) else -1)
        else:
            return 0


class SpinMatrix(IndexedObject):
    def __init__(self,name,indices):
        self.name = name
        self.indices = [i for i in indices]