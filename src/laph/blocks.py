from src.ops.indexed import IndexedFunction

class ShortProp():
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
        new_props.append(ShortProp(prop.name,
                                    prop.left_indices.c[1:],prop.right_indices.c[1:],
                                    prop.ti,prop.tf))
    diag.props = new_props
    return diag


def create_baryon_source(diag):
    for b in diag.commuting:    
        if b.arguments[2]=='tf': #only if the baryon has 2 gammas, aka SU(4) only
            for i,contract_idx in enumerate(b.indices):
                for prop in diag.props:
                    if(contract_idx==prop.l):
                        b.indices[i]=prop.r
                        diag.props.remove(prop)
                        break
                        
            b.arguments += ['ti']
    return diag