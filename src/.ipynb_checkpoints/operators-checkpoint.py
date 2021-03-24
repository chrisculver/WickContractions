from src.wick_utilities import permutations, arePermsEqualParity

#This file contains the operator class, as well as elementals that are used to 
#create operators.  
class Operator:
    def __init__(self,a,ci,qj):
        self.coef=a        #overall coefficient
        self.ci=ci         #list of commuting Index objects
        self.qj=qj         #list of non-commuting quarks


# Base class for everything that isn't a quark, 
# aka commuting objects that are tensors
class Indexed_Object:
    def __init__(self,name,indices):
        self.name = name
        self.indices = indices
    
    def cyclic_permute_indices(self):
        self.indices.rotate(1)
        
    def __str__(self):
        idx_str = ''.join([idx.label for idx in self.indices])
        return self.name + '_{' + idx_str + '}'
    
    def __eq__(self, other):
        return (self.name == other.name) and (self.indices==other.indices)

# The type of the index refers to color/spin/....  Not sure if this is necessary yet.
# The label is what you write for the idx, s1, c0, alpha,...
class Index:
    def __init__(self,name,value):
        self.type = name
        self.label = value    
        
    def __eq__(self, other):
        return (self.type==other.type) and (self.label==other.label)
    
    def __str__(self):
        return '['+self.type+','+self.label+']'
    
    
#These basically just allow you to write nicer looking code below.
class Epsilon_Tensor(Indexed_Object):
    def __init__(self,indices):
        self.name = 'eps'
        self.indices = [Index('color',i) for i in indices]
        
    def get_permutations(self):
        return [  Epsilon_Tensor([ perm[i].label for i in range(0,len(perm))]) 
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
        return [ i.label for i in indices ]
        
        
class Spin_Matrix(Indexed_Object):
    def __init__(self,name,indices):
        self.name = name
        self.indices = [Index('spin',i) for i in indices]
        
class Full_Propagator(Indexed_Object):
    def __init__(self,q,qbar):
        self.name = 'D'+q.flavor+'^{-1}'
        self.indices=[Index('color',q.color),Index('spin',q.spin),
                      Index('color',qbar.color),Index('spin',qbar.spin)]
        