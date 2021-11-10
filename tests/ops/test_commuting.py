from WickContractions.ops.commuting import *

def test_epsilon():
    eps3 = EpsilonTensor(['a','b','c'])
    assert eps3.name=='eps'
    assert eps3.indices==['a','b','c']
    
    epsPLUS = EpsilonTensor(['b','c','a'])
    epsMINUS = EpsilonTensor(['b','a','c'])
    epsZERO = EpsilonTensor(['a','a','a'])
    
    assert eps3.sign_of_permutation(epsPLUS)==1
    assert eps3.sign_of_permutation(epsMINUS)==-1
    assert eps3.sign_of_permutation(epsZERO)==0
    
def test_spinmat():
    gamma5 = SpinMatrix('g5',['s0','s1'])
    
    assert gamma5.name=='g5'
    assert gamma5.indices==['s0','s1']