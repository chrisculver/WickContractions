import WickContractions.corrs.diagram
import copy
from WickContractions.ops.indexed import IndexedFunction

class LDiagram(WickContractions.corrs.diagram.Diagram):
    def __init__(self, diag):
        if(type(diag) is not WickContractions.corrs.diagram.Diagram):
            raise ValueError("Must make Laph diagram out of src.diags.Diagram")
        self.coef = diag.coef
        self.commuting = diag.commuting
        self.props = diag.props
        self.Tblocks = {}
        self.Bblocks= {}
        
        lCnt=0
        for p in self.props:
            p.name='\\tau'
            for i,indices in enumerate([p.left_indices,p.right_indices]):
                # swap color for eigenvector idx
                color_idx = indices.c
                if color_idx[0:2] == 'c_':
                    idx='l_'+str(color_idx.split('_')[1])
                else:
                    idx='l_{'+str(lCnt)+'}'
                lCnt+=1
                indices.c=idx
                args=[]
                if i==0:
                    args.append(p.xi)
                    args.append(p.ti)
                else:
                    args.append(p.xf)
                    args.append(p.tf)
                if i==0: 
                    self.commuting.append(IndexedFunction('V*',[color_idx, idx],args))
                else:
                    self.commuting.append(IndexedFunction('V',[color_idx, idx], args))

    def get_first_idx_ends_of(self,name):
        """ generates a list of the end indices on a named object
        
        :param: name: A string
        
        :return: list of strings that are the end of the index or an empty list
                 if no object of that name is in the list.
        
        """
        for elem in self.commuting:
            if(elem.name==name):
                idx_ends=[]
                for idx in elem.indices:
                    idx_ends.append(idx[2:])
                return idx_ends
        return []
    
    
    def create_T_blocks(self):
        for color_obj_name in ['\\delta','\\epsilon']:

            epsilons=[]
            for elem in reversed(self.commuting):
                if elem.name==color_obj_name:
                    epsilons.append(elem)
                    self.commuting.remove(elem)
        
            for e in epsilons:
                # start a T function with no indices or arguments
                Tblock = IndexedFunction('T',[],[])
                TblockEquals = [e]
                for idx in e.indices:
                    for elem in self.commuting:
                        if elem.name not in ['T','T^*']:
                            if idx in elem.indices:
                                TblockEquals.append(elem)
                                new_indices = list(elem.indices)
                                new_indices.remove(idx)
                                for new_idx in new_indices:
                                    if new_idx not in Tblock.indices:
                                        Tblock.indices.append(new_idx)
                                    else:
                                        print("Warning this index is already in TBlock...\n DIdn't expect this")
                                if type(elem) == IndexedFunction:
                                    for new_arg in elem.arguments:
                                        if new_arg not in Tblock.arguments:
                                            Tblock.arguments.append(new_arg)
                                        # here I expect repeats of arguments
                                
                                self.commuting.remove(elem)
                                
                rhsString=''
                otherNames=[]
                for elem in TblockEquals:
                    rhsString+=str(elem)
                    if elem.name != '\\epsilon' and elem.name not in otherNames:
                        otherNames.append(elem.name)
                
                if len(otherNames)>1:
                    print("T has different kinds of V's in it...")
                    Tblock.name+='^?'
                elif otherNames[0]=='V*':
                    Tblock.name+='^*'
                
                self.Tblocks[str(Tblock)]=rhsString
                self.commuting.append(Tblock)
                
                
    def create_baryon_blocks(self):
        #combine epsilon tensor and leftover v's from creating tau
        self.create_T_blocks()
        
        # now combine gammas by matching evecs on props
        for elem in reversed(self.commuting):
            if elem.name not in ['T','T^*']:
                # get the evec index that matches each spin
                evec_match_indices = []
                for p in self.props:
                    if p.left_indices.s in elem.indices:
                        evec_match_indices.append(p.left_indices.c)
                    elif p.right_indices.s in elem.indices:
                        evec_match_indices.append(p.right_indices.c)
                
                for elem2 in reversed(self.commuting):
                    if elem2.name in ['T','T^*']:
                        if set(evec_match_indices) == set(elem2.indices):
                            #print('make baryon block')
                            Bblock=copy.deepcopy(elem2)
                            Bblock.name=Bblock.name.replace('T','B')
                            Bblock.indices+=elem.indices
                            Bblock.arguments+=[elem.name]
                            self.commuting.append(Bblock)
                            self.Bblocks[str(Bblock)]=str(elem2)+str(elem)
                            self.commuting.remove(elem)
                            self.commuting.remove(elem2)
            
        
    def combine_indices(self):
        new_props = []
        for p in self.props:
            if (get_int(p.left_indices.c) != get_int(p.left_indices.s)) or (get_int(p.right_indices.c) != get_int(p.right_indices.s)):
                raise ValueError("sub-sub script of indices dont match!\n Can't combine {} into combined indices".format(str(p)))
            
            new_props.append(ShortProp(p.name,
                                      get_int(p.left_indices.c),get_int(p.right_indices.c),
                                       p.ti, p.tf)
                                      )
        
        self.props=new_props
            
        new_commuting = []
        
        for c in self.commuting:
            new_indices=[]
            
            for idx in c.indices:
                new_idx = get_int(idx)
                if new_idx not in new_indices:
                    new_indices.append(new_idx)
                
                #"TODO: Check that one and only one other index matches")
            
            new_commuting.append( IndexedFunction(c.name,new_indices,c.arguments) )
            
        self.commuting=new_commuting
                
    def short_props(self):
        new_props = []
        for prop in self.props:
            new_props.append(ShortProp(prop.name,
                                    prop.left_indices.c[1:],prop.right_indices.c[1:],
                                    prop.ti,prop.tf))
        self.props = new_props
    
            
    def create_baryon_source(self):
        for b in self.commuting:    
            if b.arguments[1]=='t_f': #the other B always has same indices
                for i,contract_idx in enumerate(b.indices):
                    for prop in self.props:
                        if(contract_idx==prop.l):
                            b.indices[i]=prop.r
                            self.props.remove(prop)
                            break
                        
                b.arguments.insert(1,'t_i')
                

def get_int(idx):
    return idx.split('_')[1]
                
class ShortProp():
    def __init__(self, name, l, r, tl, tr):
        self.name = name
        self.l = l
        self.r = r
        self.tl = tl
        self.tr = tr
    
    def __str__(self):
        return self.name + '(' + self.tl + ',' + self.tr + ')' '_{' + self.l + ',' + self.r + '}'

