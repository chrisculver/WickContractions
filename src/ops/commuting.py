from src.ops.indexed import IndexedObject
from src.wick.utilities import permutations, arePermsEqualParity


class Epsilon_Tensor(IndexedObject):
    """ Symbolic epsilon tensor
        :param indices: list of indices
    """
    def __init__(self,indices):
        """Constructor
        """
        self.name = 'eps'
        self.indices = [i for i in indices]

    def get_permutations(self):
        """Get all possible permutations from original indices
        """
        return [  Epsilon_Tensor(perm)
                    for perm in permutations(self.indices)  ]

    #return +1/-1 if eps is a even/odd permutation, 0 if not.
    #TODO: do I really need this and is it correct
    def sign_of_permutation(self, eps):
        """Gives sign of the permutation compared to a reference epsilon tensor
            :return: 1 if even, -1 if odd, 0 if not a permutation
        """
        if( eps in self.get_permutations() ):
            #[ print(idx) for idx in eps.indices ]
            #[ print(idx) for idx in self.indices ]
            return (1 if arePermsEqualParity(eps.indices, self.indices) else -1)
        else:
            return 0

    def get_labels(self):
        """Returns only the indices
        """
        return [ i for i in self.indices ]
