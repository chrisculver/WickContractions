import src.wick_contract as wc
from src.operators import Operator,Spin_Matrix,Epsilon_Tensor,Full_Propagator
from src.quarks import Quark
from src.diagram import Diagram



def test_pion():
    create_pion = Operator(1,[Spin_Matrix('Gamma',['alpha_1','beta_1'])],
                            [Quark(True,'u','alpha_2','c_2'),Quark(False,'d','beta_2','c_2')])
    annihilate_pion = Operator(1,[Spin_Matrix('Gamma',['alpha_2','beta_2'])],
                            [Quark(True,'d','alpha_1','c_1'),Quark(False,'u','beta_1','c_1')])

    #From Gattringer & Lang Equation 6.12
    expected = Diagram( -1, [Spin_Matrix('Gamma',['alpha_1','beta_1']),
                             Spin_Matrix('Gamma',['alpha_2','beta_2']),
                             Full_Propagator(Quark(False,'u','beta_1','c_1'),Quark(True,'u','alpha_2','c_2')),
                             Full_Propagator(Quark(False,'d','beta_2','c_2'),Quark(True,'d','alpha_1','c_1'))], [])


    assert wc.contract(annihilate_pion, create_pion) == [expected]



def test_proton():
    create_nucleon = Operator(-1, [Epsilon_Tensor(['a','b','c']),
                                 Spin_Matrix('Ppm',['g','gpp']),
                                 Spin_Matrix('CG5',['alpha','beta'])],
                                 [Quark(True,'u','alpha','a'),
                                 Quark(True,'d','beta','b'),
                                 Quark(True,'u','g','c')]
                                 )
    annihilate_nucleon = Operator(1, [Epsilon_Tensor(['ap','bp','cp']),
                                     Spin_Matrix('Ppm',['gpp','gp']),
                                     Spin_Matrix('CG5',['alpha_p','beta_p'])],
                                     [
                                     Quark(False,'u','gp','cp'),
                                     Quark(False,'u','alpha_p','ap'),
                                     Quark(False,'d','beta_p','bp')])

    #From Gattringer & Lang Equation 6.21
    #without using that P^2=P
    common_diagram_terms = [Epsilon_Tensor(['a','b','c']),
                             Epsilon_Tensor(['ap','bp','cp']),
                             Spin_Matrix('Ppm',['g','gpp']),
                             Spin_Matrix('Ppm',['gpp','gp']),
                             Spin_Matrix('CG5',['alpha_p','beta_p']),
                             Spin_Matrix('CG5',['alpha','beta']),
                             Full_Propagator(Quark(False,'d','beta_p','bp'),Quark(True,'d','beta','b'))]

    expected = [Diagram(-1,  common_diagram_terms +
                 [Full_Propagator(Quark(False,'u','alpha_p','ap'),Quark(True,'u','g','c')),
                 Full_Propagator(Quark(False,'u','gp','cp'),Quark(True,'u','alpha','a'))],
                 []),
                 Diagram(1,   common_diagram_terms +
                             [Full_Propagator(Quark(False,'u','alpha_p','ap'),Quark(True,'u','alpha','a')),
                             Full_Propagator(Quark(False,'u','gp','cp'),Quark(True,'u','g','c'))],
                             [])
                ]

    assert wc.contract(annihilate_nucleon, create_nucleon) == expected
