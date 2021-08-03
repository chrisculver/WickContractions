from src.wick_utilities import permutations, arePermsEqualParity
from src.indexed import *

#This file contains the operator class, as well as elementals that are used to
#create operators.
class Operator:
    def __init__(self,a,ci,qj):
        self.coef=a        #overall coefficient
        self.ci=ci         #list of commuting Index objects
        self.qj=qj         #list of non-commuting quarks


#These basically just allow you to write nicer looking code below.
class Epsilon_Tensor(Indexed_Object):
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


class Spin_Matrix(Indexed_Object):
    def __init__(self,name,indices):
        self.name = name
        self.indices = [i for i in indices]


