import src.diags.diagram
from src.ops.indexed import IndexedFunction

class LDiagram(src.diags.diagram.Diagram):
    def __init__(self, diag):
        if(type(diag) is not src.diags.diagram.Diagram):
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
                else:
                    args.append(p.xf)
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
    
    
    def create_block(self, color_obj, name):
        while self.get_first_idx_ends_of(color_obj)!=[]:
            idx_ends = self.get_first_idx_ends_of(color_obj)
            time='?'
            args=[]
            for elem in self.commuting[:]:
                for idx in elem.indices:
                    if idx[1:] in idx_ends:
                        if(elem.name=='V'):
                            time = elem.arguments[0]
                        if(elem.name not in [color_obj,name,'V']):
                            args.append(elem.name)
                        if(elem.name!=name):
                            self.commuting.remove(elem)
                        break
            self.commuting.append(IndexedFunction(name,idx_ends,args+[time]))