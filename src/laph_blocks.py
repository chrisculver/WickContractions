from src.indexed import Indexed_Function

class Short_Prop():
    def __init__(self, name, l, r, tl, tr):
        self.name = name
        self.l = l
        self.r = r
        self.tl = tl
        self.tr = tr
    
    def __str__(self):
        return self.name + '(' + self.tl + ',' + self.tr + ')' '_{' + self.l + ',' + self.r + '}'
    


def short_props(diag):
    new_props = []
    for prop in diag.props:
        new_props.append(Short_Prop(prop.name,
                                    prop.left_indices.c[1:],prop.right_indices.c[1:],
                                    prop.ti,prop.tf))
    diag.props = new_props
    return diag

def create_baryon_block(diag):
    while diag.get_first_idx_ends_of('eps')!=[]:
        idx_ends = diag.get_first_idx_ends_of('eps')
        #print(idx_ends)
        #to_remove = []
        time='?'
        for elem in diag.ci[:]:
            #print(elem)
            for idx in elem.indices:
                #print(idx[1:])
                if idx[1:] in idx_ends:
                    if(elem.name=='V'):
                        time = elem.arguments[0]
                    if(elem.name!='B'):
                        diag.ci.remove(elem)
                    break
        
        diag.ci.append(Indexed_Function('B',idx_ends,[time]))
    return diag

def create_baryon_source(diag):
    for b in diag.ci:    
        if b.arguments[0]=='tf':
            for i,contract_idx in enumerate(b.indices):
                for prop in diag.props:
                    if(contract_idx==prop.l):
                        b.indices[i]=prop.r
                        diag.props.remove(prop)
                        break
                        
            b.arguments += ['ti']
    return diag
            
    
def create_meson_block(diag):
    while diag.get_first_idx_ends_of('delta')!=[]:
        idx_ends = diag.get_first_idx_ends_of('delta')
        #print(idx_ends)
        #to_remove = []
        time='?'
        for elem in diag.ci[:]:
            #print(elem)
            for idx in elem.indices:
                #print(idx[1:])
                if idx[1:] in idx_ends:
                    if(elem.name=='V'):
                        time = elem.arguments[0]
                    if(elem.name!='M'):
                        diag.ci.remove(elem)
                    break
        
        diag.ci.append(Indexed_Function('M',idx_ends,[time]))
    return diag

def create_meson_source(diag):
    for m in diag.ci:    
        if m.arguments[0]=='tf':
            for i,contract_idx in enumerate(m.indices):
                for prop in diag.props:
                    if(contract_idx==prop.l):
                        m.indices[i]=prop.r
                        diag.props.remove(prop)
                        break
                        
            m.arguments += ['ti']
    return diag