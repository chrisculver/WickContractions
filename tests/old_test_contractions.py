#import WickContractions.wick_contract as wc
#from WickContractions.elemental_operator import ElementalOperator,Spin_Matrix,Epsilon_Tensor
#from WickContractions.quarks import Quark
#from WickContractions.diagram import Diagram, Full_Propagator



#def test_pion():
    #create_pion = ElementalOperator(1,[Spin_Matrix('Gamma',['alpha_1','beta_1'])],
    #                        [Quark(True,'u','alpha_2','c_2','t2','x2'),Quark(False,'d','beta_2','c_2','t2','x2')])
    #annihilate_pion = ElementalOperator(1,[Spin_Matrix('Gamma',['alpha_2','beta_2'])],
    #                        [Quark(True,'d','alpha_1','c_1','t1','x1'),Quark(False,'u','beta_1','c_1','t1','x1')])

    #From Gattringer & Lang Equation 6.12
#    expected = Diagram( -1, [Spin_Matrix('Gamma',['alpha_1','beta_1']),
#                             Spin_Matrix('Gamma',['alpha_2','beta_2']),
                             #Full_Propagator(Quark(False,'u','beta_1','c_1','t1','x1'),Quark(True,'u','alpha_2','c_2','t2','x2')),
#                             #Full_Propagator(Quark(False,'d','beta_2','c_2','t2','x2'),Quark(True,'d','alpha_1','c_1','t1','x1'))], [])


#    assert wc.contract(annihilate_pion, create_pion) == [expected]



#def test_proton():
#    create_nucleon = ElementalOperator(-1, [Epsilon_Tensor(['a','b','c']),
#                                 Spin_Matrix('Ppm',['g','gpp']),
#                                 Spin_Matrix('CG5',['alpha','beta'])],
#                                 [Quark(True,'u','alpha','a','t','x'),
#                                 Quark(True,'d','beta','b','t','x'),
#                                 Quark(True,'u','g','c','t','x')]
#                                 )
#    annihilate_nucleon = ElementalOperator(1, [Epsilon_Tensor(['ap','bp','cp']),
#                                     Spin_Matrix('Ppm',['gpp','gp']),
#                                     Spin_Matrix('CG5',['alpha_p','beta_p'])],
#                                     [
#                                     Quark(False,'u','gp','cp','t','x'),
#                                     Quark(False,'u','alpha_p','ap','t','x'),
#                                     Quark(False,'d','beta_p','bp','t','x')])

    #From Gattringer & Lang Equation 6.21
    #without using that P^2=P
    #common_diagram_terms = [Epsilon_Tensor(['a','b','c']),
    #                         Epsilon_Tensor(['ap','bp','cp']),
    #                         Spin_Matrix('Ppm',['g','gpp']),
    #                         Spin_Matrix('Ppm',['gpp','gp']),
    #                         Spin_Matrix('CG5',['alpha_p','beta_p']),
    #                         Spin_Matrix('CG5',['alpha','beta']),
                             #Full_Propagator(Quark(False,'d','beta_p','bp','t','x'),Quark(True,'d','beta','b','t','x'))]

#    expected = [Diagram(-1,  common_diagram_terms +
#                 [Full_Propagator(Quark(False,'u','alpha_p','ap','t','x'),Quark(True,'u','g','c','t','x')),
#                 Full_Propagator(Quark(False,'u','gp','cp','t','x'),Quark(True,'u','alpha','a','t','x'))],
#                 []),
#                 Diagram(1,   common_diagram_terms +
                             #[Full_Propagator(Quark(False,'u','alpha_p','ap','t','x'),Quark(True,'u','alpha','a','t','x')),
                             #Full_Propagator(Quark(False,'u','gp','cp','t','x'),Quark(True,'u','g','c','t','x'))],
#                             [])
#                ]

#    print('warning the baryon one needs to be updated so baryons are at different positions')
#    assert wc.contract(annihilate_nucleon, create_nucleon) == expected
