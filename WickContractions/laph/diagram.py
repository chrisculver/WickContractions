import WickContractions.corrs.diagram
from WickContractions.ops.indexed import IndexedFunction

class LDiagram(WickContractions.corrs.diagram.Diagram):
    def __init__(self, diag):
        if(type(diag) is not WickContractions.corrs.diagram.Diagram):
            raise ValueError("Must make Laph diagram out of src.diags.Diagram")
        self.coef = diag.coef
        self.commuting = diag.commuting
        self.props = diag.props
        
        for p in self.props:
            for i,indices in enumerate([p.left_indices,p.right_indices]):
                color_idx = indices.c
                idx='l'+indices.c[1:]
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
                    idx_ends.append(idx[1:])
                return idx_ends
        return []
    
    
    def create_baryon_blocks(self):
        # TODO make it handle V and V* better to create T and T^*
        color_obj='eps'
        name=''
        while self.get_first_idx_ends_of(color_obj)!=[]:
            idx_ends = self.get_first_idx_ends_of(color_obj)
            time='?'
            args=[]
            for elem in self.commuting[:]:
                for idx in elem.indices:
                    if idx[1:] in idx_ends:
                        if(elem.name=='V'):
                            name = 'B'
                            time=elem.arguments[1]
                        if(elem.name=='V*'):
                            name = 'B*'
                            time=elem.arguments[1]
                        if(elem.name not in [color_obj,name,'V','V*']):
                            args.append(elem.name)
                        if(elem.name!=name):
                            self.commuting.remove(elem)
                        break
            self.commuting.append(IndexedFunction(name,idx_ends,args+[time]))

    def short_props(self):
        new_props = []
        for prop in self.props:
            new_props.append(ShortProp(prop.name,
                                    prop.left_indices.c[1:],prop.right_indices.c[1:],
                                    prop.ti,prop.tf))
        self.props = new_props

            
    def create_baryon_source(self):
        for b in self.commuting:    
            if b.arguments[1]=='tf': #only if the baryon has 2 gammas, aka SU(4) only
                for i,contract_idx in enumerate(b.indices):
                    for prop in self.props:
                        if(contract_idx==prop.l):
                            b.indices[i]=prop.r
                            self.props.remove(prop)
                            break
                        
                b.arguments += ['ti']
                
                
                
class ShortProp():
    def __init__(self, name, l, r, tl, tr):
        self.name = name
        self.l = l
        self.r = r
        self.tl = tl
        self.tr = tr
    
    def __str__(self):
        return self.name + '(' + self.tl + ',' + self.tr + ')' '_{' + self.l + ',' + self.r + '}'

