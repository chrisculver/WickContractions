from WickContractions.ops.operator import *
from WickContractions.ops.elemental import *
from WickContractions.ops.commuting import *
from WickContractions.ops.quarks import *

def test_op_str():
    g=SpinMatrix('g',['s0','s1'])
    q=Quark(True,'u','s0','c','t0','x5')
    elem = ElementalOperator(1.5,[g],[q])
    
    expected = '1.5g_{s0 s1}\\bar{u}_{s0 c}(x5, t0)'
    
    assert str(elem) == expected
    
    g2=SpinMatrix('h',['alpha','beta'])
    q2=Quark(False,'f','s','a','t','x')
    elem2 = ElementalOperator(-1.0,[g,g2],[q,q2])
    
    expected2 = '-1.0g_{s0 s1}h_{alpha beta}\\bar{u}_{s0 c}(x5, t0)f_{s a}(x, t)'
    
    assert str(elem2)==expected2
    
    op = Operator([elem,elem])
    
    assert str(op) == expected+'+'+expected
    