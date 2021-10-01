from src.ops.indexed import *
import copy

def test_indexedobject():
    o = IndexedObject('A',['i','j','k'])
    ocycle = IndexedObject('A',['k','i','j'])
    o.cyclic_permute_indices()
    assert o==ocycle
    
    
    
def test_indexedfuncprint():
    f = IndexedFunction('f',['i','j'],['x','t'])
    f2 = copy.deepcopy(f)
    assert f2==f
    
    assert str(f)=='f(x,t)_{i j}'
    

def test_indexed_order():
    f = IndexedFunction('f',['i','j'],['x','t'])
    f2 = IndexedFunction('f',['i','k'],['x','t'])
    f3 = IndexedFunction('f',['i','k'],['y','t'])
    g = IndexedFunction('g',['i','j'],['x','t'])
                         
    assert (f<g)==True
    assert (f<f2)==True
    assert (f2<f3)==True
    assert (f<f3)==True