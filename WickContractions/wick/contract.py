from WickContractions.diags.diagram import Diagram
import WickContractions.wick.utilities as util


def contract(o1, o2):
    """ Contracts two operators
        :param o1: Operator
        :param o2: Operator

        :return: List of diagrams
    """

    diagrams=[]
    for e1 in o1.elementals:
        for e2 in o2.elementals:
            new_diags = contract_elementals(e1,e2)

            for d in new_diags:
                diagrams.append(d)

    return diagrams


# Contracts two Operators returning a list of diagrams
def contract_elementals(o1, o2):
    """ Contracts two operator elementals returning a list of diagrams

        :param o1: Elemental operator
        :param o2: Elemental operator

        :return: List of diagrams
    """
    # separate out the commuting and anti-commuting objects
    quarks = o1.quarks + o2.quarks
    commuting_objs = o1.commuting + o2.commuting
    #find all permutations of quarks which can be combined to propagators.
    contracted_quarks = contract_quarks(quarks)

    # construct the diagrams from a coefficient (which depends on anti-commutivity of quarks)
    # the list of commuting objects, and a list of quarks which become propagators
    diagrams = []
    for qs in contracted_quarks:
        diagrams.append( Diagram(o1.coef*o2.coef*(1. if util.arePermsEqualParity(quarks,qs) else -1.),
                 commuting_objs,
                 qs )
                       )

    # Now return the diagrams
    return diagrams

# Finds all permutations of the quarks that can be combined into diagrams.
def contract_quarks(quarks):
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

    ps=util.permutations(unbarred)
    ps=[[q for q in p] for p in ps] #just convert the generator to a list...

    #for each list, check whether or not the quarks are aligned in a way suitable for combination into a propagator, and re-arrange the two lists into a single list.
    res=[]
    idx=0
    for p in ps:
        contractable = util.quarks_pairwise_same_flavor(p,barred)

        if(contractable):
            res.append([])
            for i in range(len(p)):
                res[idx].append(p[i])
                res[idx].append(barred[i])
            idx+=1
    return res
