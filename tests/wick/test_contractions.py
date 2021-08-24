from src.wick.contract import contract, contract_quarks, contract_elementals
from src.ops.quarks import Quark
from src.ops.elemental import ElementalOperator
from src.ops.operator import Operator
from src.ops.commuting import IndexedObject
from src.diags.diagram import Diagram
from src.diags.propagator import FullPropagator

def test_quark_contraction():
    qubar0=Quark(True,'u',"s0","c0","t0","x0")
    qd1=Quark(False,'d',"s1","c1","t1","x1")
    qu2=Quark(False,'u',"s2","c2","t2","x2")

    assert contract_quarks([qubar0,qd1])==[]

    assert contract_quarks([qubar0,qu2])==[[qu2,qubar0]]
    assert contract_quarks([qu2,qubar0])==[[qu2,qubar0]]



def pion_creation_elemental():
    create_pion=ElementalOperator(1,
                                  [IndexedObject("Gamma",["alpha2","beta2"])],
                                  [Quark(True,'u',"alpha2","c2","t2","m2"),
                                   Quark(False,'d',"beta2","c2","t2","m2")]
                                 )
    return create_pion



def pion_annihilation_elemental():
    annihilate_pion=ElementalOperator(1,
                                        [IndexedObject("Gamma",["alpha1","beta1"])],
                                        [Quark(True,'d',"alpha1","c1","t1","m1"),
                                         Quark(False,'u',"beta1","c1","t1","m1")]
                                       )
    return annihilate_pion

def pion_expected():
    return [Diagram(-1,
                        [IndexedObject("Gamma",["alpha1","beta1"]),
                         IndexedObject("Gamma",["alpha2","beta2"])],
                         props=[
                         FullPropagator(Quark(False,'d',"beta2","c2","t2","x2"),
                                        Quark(True,'d',"alpha1","c1","t1","x1")),
                        FullPropagator(Quark(False,'u',"beta1","c1","t1","x1"),
                                       Quark(True,'u',"alpha2","c2","t2","x2"))]
                    )]


def test_elemental_pion_contraction():
    # Gattringer & Lang Equation 6.12
    create_pion=pion_creation_elemental()
    annihilate_pion=pion_annihilation_elemental()

    expected=pion_expected()

    print(contract_elementals(annihilate_pion,create_pion)[0])
    print(expected)

    assert contract_elementals(annihilate_pion,create_pion) == pion_expected()

def test_pion_contraction():
    create_pion=Operator([pion_creation_elemental()])
    annihilate_pion=Operator([pion_annihilation_elemental()])

    assert contract(annihilate_pion,create_pion)==pion_expected()


def nucleon_creation_elemental():
    create_nucleon = ElementalOperator(-1,
                                        [IndexedObject("epsilon",['a','b','c']),
                                        IndexedObject("Ppm",['g','gpp']),
                                        IndexedObject("CG5",['alpha','beta'])],
                                        [Quark(True,'u','alpha','a','t','x'),
                                        Quark(True,'d','beta','b','t','x'),
                                        Quark(True,'u','g','c','t','x')])
    return create_nucleon


def nucleon_annihilation_elemental():
    annihilate_nucleon = ElementalOperator(1,
                                            [IndexedObject("epsilon",['ap','bp','cp']),
                                            IndexedObject("Ppm",['gpp','gp']),
                                            IndexedObject("CG5",['alpha_p','beta_p'])],
                                            [Quark(False,'u','gp','cp','t0','x0'),
                                            Quark(False,'u','alpha_p','ap','t0','x0'),
                                            Quark(False,'d','beta_p','bp','t0','x0')])
    return annihilate_nucleon

def nucleon_expected():
    common_diagram_terms = [IndexedObject("epsilon",['ap','bp','cp']),
                            IndexedObject("Ppm",['gpp','gp']),
                            IndexedObject("CG5",['alpha_p','beta_p']),
                            IndexedObject("epsilon",['a','b','c']),
                            IndexedObject("Ppm",['g','gpp']),
                            IndexedObject("CG5",['alpha','beta'])]

    dprop = FullPropagator(Quark(False,'d','beta_p','bp','t0','x0'),Quark(True,'d','beta','b','t','x'))
    d0=Diagram(-1, common_diagram_terms,
                props=[FullPropagator(Quark(False,'u','gp','cp','t0','x0'),Quark(True,'u','alpha','a','t','x')),
                        dprop,
                        FullPropagator(Quark(False,'u','alpha_p','ap','t0','x0'),Quark(True,'u','g','c','t','x'))
                       ]
              )
    d1=Diagram(1, common_diagram_terms,
                props=[FullPropagator(Quark(False,'u','alpha_p','ap','t0','x0'),Quark(True,'u','alpha','a','t','x')),
                        dprop,
                       FullPropagator(Quark(False,'u','gp','cp','t0','x0'),Quark(True,'u','g','c','t','x'))]
              )

    return [d0,d1]

def test_nucleon_elemental_contraction():
    create_nucleon=nucleon_creation_elemental()
    annihilate_nucleon=nucleon_annihilation_elemental()

    print(contract_elementals(annihilate_nucleon,create_nucleon)[0])
    print(nucleon_expected()[0])
    print(contract_elementals(annihilate_nucleon,create_nucleon)[1])
    print(nucleon_expected()[1])

    assert contract_elementals(annihilate_nucleon,create_nucleon)==nucleon_expected()


def test_nucleon_contraction():
    create_nucleon=Operator([nucleon_creation_elemental()])
    annihilate_nucleon=Operator([nucleon_annihilation_elemental()])
    assert contract(annihilate_nucleon,create_nucleon)==nucleon_expected()
