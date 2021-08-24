from src.wick.contract import contract, contract_quarks, contract_elementals
from src.ops.quarks import Quark
from src.ops.elemental import ElementalOperator
from src.ops.operator import Operator
from src.diags.diagram import Diagram

def test_quark_contraction():
    qubar0 = Quark(True,'u',"s0","c0","t0","x0")
    qd1 = Quark(False,'d',"s1","c1","t1","x1")
    qu2 = Quark(False,'u',"s2","c2","t2","x2")

    assert contract_quarks([qubar0,qd1])==[]

    assert contract_quarks([qubar0,qu2])==[[qu2,qubar0]]
    assert contract_quarks([qu2,qubar0])==[[qu2,qubar0]]



#def test_elemental_pion_contraction():
