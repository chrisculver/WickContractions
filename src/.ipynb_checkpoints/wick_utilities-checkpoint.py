import copy

# from https://www.bernardosulzbach.com/heaps-algorithm/
def swap(elements, i, j):
    elements[i], elements[j] = elements[j], elements[i]

# from https://www.bernardosulzbach.com/heaps-algorithm/
def generate_permutations(elements, n):
    # As by Robert Sedgewick in Permutation Generation Methods
    c = [0] * n
    yield elements
    i = 0
    while i < n:
        if c[i] < i:
            if i % 2 == 0:
                swap(elements, 0, i)
            else:
                swap(elements, c[i], i)
            yield elements
            c[i] += 1
            i = 0
        else:
            c[i] = 0
            i += 1

# from https://www.bernardosulzbach.com/heaps-algorithm/
def permutations(elems):
    elements = copy.deepcopy(elems) #leave original list in order
    return generate_permutations(elements, len(elements))



# from https://stackoverflow.com/questions/1503072/how-to-check-if-permutations-have-equal-parity #you'll never guess what my google search was to find this.
def arePermsEqualParity(perm0, perm1):
    """Check if 2 permutations are of equal parity.

    Assume that both permutation lists are of equal length
    and have the same elements. No need to check for these
    conditions.
    """
    perm1 = perm1[:] ## copy this list so we don't mutate the original

    transCount = 0
    for loc in range(len(perm0) - 1):                         # Do (len - 1) transpositions
        p0 = perm0[loc]
        p1 = perm1[loc]
        if p0 != p1:
            sloc = perm1[loc:].index(p0)+loc          # Find position in perm1
            perm1[loc], perm1[sloc] = p0, p1          # Swap in perm1
            transCount += 1

    # Even number of transpositions means equal parity
    if (transCount % 2) == 0:
        return True
    else:
        return False
    
#return whether or not quarks at same position in each list have the same flavor
def quarks_same_flavor(unbarred,barred):
    same_flavor = True
    for i in range(0,len(unbarred)):
        if(unbarred[i].flavor != barred[i].flavor):
            same_flavor = False
    return same_flavor