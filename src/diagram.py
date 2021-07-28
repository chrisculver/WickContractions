from src.operators import Epsilon_Tensor, Indexed_Object
from src.wick_utilities import permutations

class Diagram:
    def __init__(self, coefs, cis, qs):
        self.coef = coefs
        self.ci = cis[:] # I need this otherwise cis gets modified....  what????
        self.props = []
        for p in range(0,len(qs)//2):
            self.props.append(Full_Propagator(qs[2*p],qs[2*p+1]))
        ### Since all these diagrams are commuting, let's sort them, this will
        ### make comparisons across various diagrams much easier.
        self.ci=sorted(self.ci)
        #self.props=sorted(self.props)

    def __str__(self):
        ci_str = ''.join([str(c) for c in self.ci])
        prop_str = ''.join([str(p) for p in self.props])
        return str(self.coef) + ' ' + ci_str + prop_str

    def __eq__(self, other):
        return (self.coef == other.coef) and (self.ci==other.ci)


    #check whether or not two diagrams are related by any of the symmetries
    #provided, we allow a flexible list, since there's no point in using properties
    #of the epsilon tensor if there are no epsilon tensors. 
    def equivalent_to(self,other,symmetries):
        ## all objects in a diagram are sorted.
        ## We only have to look for symmetries/label swapping.
        for sym in symmetries():
            sother = sym(other)
            if(self.ci == sother.ci):
                return sother.coef

        return 0
    
    def laphify(self):
        for elem in self.props:
            for indices in [elem.left_indices, elem.right_indices]:
                color_idx = indices.c
                idx = 'l'+indices.c[1:]
                indices.c = idx
                self.ci.append(Indexed_Object('V',[color_idx, idx, indices.t]))


class Full_Propagator():
    def __init__(self,q,qbar):
        self.name = 'prop^'+q.flavor
        #if q.time=='ti' and qbar.time=='ti':
        #    self.name = 'pTi'
        #if q.time=='ti' and qbar.time=='tf':
        #    self.name = 'pFwd'
        #if q.time=='tf' and qbar.time=='ti':
        #    self.name = 'pBwd'
        #if q.time=='tf' and qbar.time=='tf':
        #    self.name = 'pTf'
        self.left_indices=Prop_Index(q.color,q.spin,q.time)
        self.right_indices=Prop_Index(qbar.color,qbar.spin,qbar.time)
        
    def __str__(self):
        return self.name + '_{' + str(self.left_indices) + ' | ' + str(self.right_indices) + '}'
    

    
class Prop_Index():
    def __init__(self,c,s,t):
        self.c=c
        self.s=s
        self.t=t
    def __str__(self):
        return self.c + self.s + self.t

    
class Short_Prop():
    def __init__(self, name, l, r, tl, tr):
        self.name = name
        self.l = l
        self.r = r
        self.tl = tl
        self.tr = tr
    
    def __str__(self):
        return self.name + '(' + self.tl + ',' + self.tr + ')' '_{' + self.l + ',' + self.r + '}'
    
