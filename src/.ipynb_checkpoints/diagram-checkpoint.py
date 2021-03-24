from src.operators import Full_Propagator, Epsilon_Tensor
from src.wick_utilities import permutations

class Diagram:
    def __init__(self, coefs, cis, qs):
        self.coef = coefs
        self.ci = cis[:] # I need this otherwise cis gets modified....  what????
        for p in range(0,len(qs)//2):
            self.ci.append(Full_Propagator(qs[2*p],qs[2*p+1]))
            
    def __str__(self):
        ci_str = ''.join([str(c) for c in self.ci])
        return str(self.coef) + ' ' + ci_str
    
    #THIS IS HORRIBLY INEFFICIENT RIGHT NOW!
    #check whether or not this diagram is equivalent to another one 
    #I want to rewrite this to take a list of symetries (as functions)
    def equivalent_to(self,other):
        ## try swapping around color indices and relabelling the indices.
        new_diag = Diagram(1,[],[])
        for c in other.ci:
            if(type(c)==Epsilon_Tensor):
                for perm in c.get_permutations():
                    new_d = Diagram(other.coef*c.sign_of_permutation(perm), [perm if elem==c else elem for elem in other.ci], [])
                    
                    for re_d in new_d.relabel_colors():
                        if(self.ci == re_d):
                            return re_d.coef
                    

        return 0
    
    
    def relabel_colors(self):
        epsilons = []
        for c in self.ci:
            if(type(c)==Epsilon_Tensor):
                epsilons.append(c)
            
        start_labels = [ e.get_labels() for e in epsilons ]
        
        relabeled = []
        
        for labels in start_labels:
            for p in permutations(labels):
                
        
    
    
    
            
        