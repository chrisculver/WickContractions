""" Contraction functions for two operators and a list of quarks.

This file contains two functions, one which contracts two operators, and another
that contracts a list of quarks.

    Typical usage:

    contract(o1,o2)
    quark_contract([q1,q2,q3,q4])

"""

from WickContractions.diagram import Diagram
from WickContractions.wick_utilities import permutations,arePermsEqualParity,quarks_same_flavor

# Contracts two Operators returning a list of diagrams
def contract(o1, o2):
    """ Contracts two operators returning a list of diagrams

        :param o1: Operator
        :param o2: Operators

        :return: List of diagrams
    """
    # separate out the commuting and anti-commuting objects
    quarks = o1.qj + o2.qj
    commuting_objs = o1.ci + o2.ci
    #find all permutations of quarks which can be combined to propagators.
    contract_quarks = quark_contract(quarks)

    # construct the diagrams from a coefficient (which depends on anti-commutivity of quarks)
    # the list of commuting objects, and a list of quarks which become propagators
    diagrams = []
    for qs in contract_quarks:
        diagrams.append( Diagram(o1.coef*o2.coef*(1 if arePermsEqualParity(quarks,qs) else -1),
                 commuting_objs,
                 qs )
                       )

    # Now return the diagrams
    return diagrams

# Finds all permutations of the quarks that can be combined into diagrams.
def quark_contract(quarks):
    """ Finds all permutations of quarks that will create a diagram.

        :param quarks: A list of quarks

        :return: A list of a list of quarks, in all orders for creating diagrams.
    """
    barred = []
    unbarred = []
    for q in quarks:
        if q.barred:
            barred.append(q)
        else:
            unbarred.append(q)

    ps=permutations(unbarred)
    ps=[[q for q in p] for p in ps] #just convert the generator to a list...

    #for each list, check whether or not the quarks are aligned in a way suitable for combination into a propagator, and re-arrange the two lists into a single list.
    res=[]
    idx=0
    for p in ps:
        contractable = quarks_same_flavor(p,barred)

        if(contractable):
            res.append([])
            for i in range(len(p)):
                res[idx].append(p[i])
                res[idx].append(barred[i])
            idx+=1
    return res
