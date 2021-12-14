import numpy as np
import itertools
import sys

# unitary transformation from Weyl to Dirac basis
# | 1  1 |
# |-1  1 |
WEYL_DIRAC = np.array([[1,0,1,0],[0,1,0,1],[-1,0,1,0],[0,-1,0,1]])
# unitary transformation from Weyl to Dirac basis
# | 1 -1 |
# | 1  1 |
DIRAC_WEYL = np.array([[1,0,-1,0],[0,1,0,-1],[1,0,1,0],[0,1,0,1]])

# assumes Nf=2
NF=2
# top down approach to find fully symmetric
# Nc spin-flavor wave function
# with desired spin S and isospin I 
# example input 
# Nc I   Iz    S   Sz 
# 3 0.5 0.5  0.5  -0.5

# Use binary labeling, for example  for SU(3) spin-flavor
# |f1 s1 f2 s2 f3 s3 >
# u=0,d=1
# ex. |000000> = |u^ u^ u^ > = 0 = (1,0,0,0,..,0) 1 in 0th position
# ex. |000010> = |u^ u^ d^ > = 2 = (0,0,1,0,..,0) 1 in 2nd position


def get_evals(Nc, I, Iz, S, Sz):
    # what the values of I and S could be given Nc
    Qvals_possible = [(Nc - 2 * i) * 1 / 2 for i in np.arange(int(Nc / 2) + 1)]
    # evals to check for in calculation of operators I^2 and S^2
    Q_evals = [Qval * (Qval + 1) for Qval in Qvals_possible]

    symmetric_val = max(Qvals_possible)
    # check I and S compatible
    if symmetric_possible(I, S, symmetric_val):
        print("I and S okay")
    else:
        print("These values of I and S cannot be combined in a symmetric way")
        sys.exit(3)

    # get possible S and I subspace vals
    IS_sub_possible = get_Qsub_possible(Iz, Sz, Qvals_possible, symmetric_val)
    IS_sub_evals = [[Ival*(Ival+1), Sval*(Sval+1)] for Ival, Sval in IS_sub_possible]

    return Q_evals, IS_sub_evals


# is it possible to combine I and S to make a symmetric wavefunction?
def symmetric_possible(I, S, symmetric_val):
    I_symm = bool(I == symmetric_val)
    S_symm = bool(S == symmetric_val)
    return bool(I_symm == S_symm)  # both symmetric or neither symmetric possible


# what the values of I and S could be given symmetric (possible_symm)
# and Iz, Sz (ex. Sz=-1/2 is part of S=1/2 and S=3/2) (possible_Q)
def get_Qsub_possible(Iz, Sz, Qvals_possible, symmetric_val):
    Qsub_possible = []
    for IQval in Qvals_possible:
        for SQval in Qvals_possible:
            # check to see if IQval and SQVal pair can be combined symmetrically
            possible_symm = symmetric_possible(IQval, SQval, symmetric_val)
            # check that Qval not smaller than Iz/Sz, ex if Iz=3/2, can't have I=1/2
            possible_Q = bool(IQval >= abs(Iz) and SQval >= abs(Sz))
            if possible_symm and possible_Q:  # if symmetric and z component works
                Qsub_possible.append([IQval, SQval])
    return Qsub_possible


# given a position n, in a state vector, find the spin (up or down)
# of the kth quark (spin or flavor)
def spin_of_k_position(Nc, n, k):
    binary = bin(n)[2:]  # remove the "b0" symbol
    # append 0s to beginning so all the same length
    binary = "0" * (2 * Nc - len(binary)) + binary
    spin = binary[k]
    if spin == "0":
        return "u"
    if spin == "1":
        return "d"


# compute Iz, Sz matrix for each individual quark
# Iiz |f1 s1 f2 s2 f3 s3> = Iz(fi) |state>
# ex. I3
# +1/2 for all values of n such that n written in binary has a
# 0 in the 5th place (f3 place), ex. 11 11 01, ex. 00, 01, 00
# -1/2 for all values of n such that n written in binary has a
# 1 in the 5th place (f3 place) ex. 11 11 10, ex. 00, 01, 11
def get_Siz(Nc, dim, k):
    Siz = np.zeros((dim, dim))
    for n in range(dim):
        spin = spin_of_k_position(Nc, n, k)
        if spin == "u":
            Siz[n, n] = 1 / 2
        if spin == "d":
            Siz[n, n] = -1 / 2
    return Siz


def flip_at_k(Nc, n, k):
    binary = bin(n)[2:]  # remove the "b0" symbol
    # append 0s to beginning so all the same length
    binary = "0" * (2 * Nc - len(binary)) + binary
    # flip 0<->1 at kb
    prefix = binary[:k]
    flip = str((int(binary[k]) + 1) % 2)
    suffix = binary[k + 1:]
    m = int(prefix + flip + suffix, 2)
    return m


# transform from u to d or d to u
# of the kth quark (spin or flavor)
def get_S_plus_minus(Nc, dim, k):
    S_plus = np.zeros((dim, dim))
    S_minus = np.zeros((dim, dim))
    for n in range(dim):  # row indicating where we are taking state to
        spin_n = spin_of_k_position(Nc, n, k)
        m = flip_at_k(Nc, n, k)
        if spin_n == "u":  # S_plus flips to u
            S_plus[n, m] = 1  # take m(d) to n(u)
        if spin_n == "d":  # S_minus flips to d
            S_minus[n, m] = 1  # take m(u) to n(d)
    return S_plus, S_minus


def compute_Ssq_total(Nc, dim, Sisq, Siz, Si_pm):
    Ssq = np.zeros((dim, dim))
    # contribution from Ii^2
    for i in range(Nc):
        Ssq += Sisq[i]
    # contribution from Iiz (diagonal, so order doesn't matter, factor of 2)
    index_combinations = list(itertools.combinations(np.arange(Nc), 2))
    for comb_indices in index_combinations:
        ind1 = comb_indices[0]
        ind2 = comb_indices[1]
        Ssq += 2 * np.matmul(Siz[ind1], Siz[ind2])
    # contributions from Iix,Iiy (in terms of Ii+ and Ii-), not diagonal
    index_permutations = list(itertools.permutations(np.arange(Nc), 2))
    for perm_indices in index_permutations:
        ind1 = perm_indices[0]
        ind2 = perm_indices[1]
        Ssq += 0.5 * np.matmul(Si_pm[ind1][0], Si_pm[ind2][1])
        Ssq += 0.5 * np.matmul(Si_pm[ind1][1], Si_pm[ind2][0])
    return Ssq


# check that list1 is a subset of list2 
def check_subsets(list1, list2, tol=1e-6):
    for item1 in list(list1):
        in_list2 = False
        for item2 in list(list2):
            if abs(item1 - item2) < tol:
                in_list2 = True
                break
                # if can't find item1, not a subset
        if not in_list2:
            return False
    return True


# check that a set of lists are equal 
# by checking l1 subset of l2 for all permutations l1,2l
def check_equiv_lists(lists):
    indices = list(np.arange(len(lists)))
    perms = itertools.permutations(indices, 2)
    for perm in list(perms):
        if check_subsets(lists[perm[0]], lists[perm[1]]) is False:
            return False
    return True


def check_eigenvalues(Ivalues, I_evals, Svalues, S_evals):
    passed = True
    if check_equiv_lists([Ivalues, I_evals]) is False:
        passed = False
        print("\n\nUNEXPECTED or MISSING ISOSPIN VALUE")
        print("expected")
        print(I_evals)
        print("found")
        print(Ivalues)
    if check_equiv_lists([Svalues, S_evals]) is False:
        passed = False
        print("UNEXPECTED or MISSING SPIN VALUE")
        print("expected")
        print(S_evals)
        print("found")
        print(Svalues)
        print("\n\n")
    if passed:
        print("good\n")


def check_sub_eigenvalues(Ivalues, Svalues, IS_sub_evals):
    # first just check that there are not I or S found that don't belong at all
    I_sub_vals = list(set([IS_val[0] for IS_val in IS_sub_evals]))
    S_sub_vals = list(set([IS_val[1] for IS_val in IS_sub_evals]))
    check_eigenvalues(Ivalues, I_sub_vals, Svalues, S_sub_vals)

    # give warning of how I and S should be combined
    print("NOTE that in order to make symmetric wavefunction,\n "
          "can only combine following isospin and spin eigenvalues")
    for Ival, Sval in IS_sub_evals:
        print(f'I*(I+1) = {Ival}, S*(S+1) = {Sval}')
    print()


# Generic way to construct
def get_base_state(Nc, Sz):
    # start at maximal, 0=up, 1=down
    state = ["0"]*Nc
    Sz_state = 1 / 2 * Nc
    # then reduce  
    for i in range(Nc):
        if Sz_state == Sz:  # spin done
            break
        else:  # keep reducing spin
            state[i] = "1"
            Sz_state -= 1  # switching u to d
    return state


def get_all_states(Nc, Ibase_state, Sbase_state):
    # duu found above, now get all perms of that, duu,udu,uud
    Iperms = list(set(list(itertools.permutations(Ibase_state, Nc))))
    Sperms = list(set(list(itertools.permutations(Sbase_state, Nc))))
    # combine I and S into one set of states
    IS_all = []
    for Iperm in Iperms:
        for Sperm in Sperms:
            state_string = ''
            for quark in range(Nc):
                state_string += Iperm[quark]
                state_string += Sperm[quark]
            IS_all.append(state_string)
    IS_all = list(set(IS_all))
    return IS_all


def check_symmetric(Nc, state1, state2):
    symmetric = False
    # break apart into quarks 
    quarks = [state2[i:i + 2] for i in range(0, 2 * Nc, 2)]
    quark_permutations = itertools.permutations(quarks, Nc)
    # put string back together 
    quark_permutations = [''.join(perm) for perm in quark_permutations]
    if state1 in quark_permutations:
        symmetric = True
    return symmetric


def get_symmetric_states(Nc, all_states):
    if len(all_states) == 1:
        return [all_states]
    # make list of sublists containing states related by interchanging 2 quarks
    symmetric_states = []
    # loop over all states to place them into a sublist 
    for i, state2 in enumerate(all_states):
        # i=0 0th state is already placed into a sublist 
        if i == 0:
            pass
        # states to compare this state to are a representative state from each sublist 
        state1_list = [symmetric_states[n][0] for n in range(len(symmetric_states))]
        # loop over representatives list until a match is found 
        found_symmetric = False
        for n, state1 in enumerate(state1_list):
            if check_symmetric(Nc, state1, state2):
                # if found match, put this state into the correct sublist 
                found_symmetric = True
                symmetric_states[n].append(state2)
                break
        # if no match is found, start a new sublist 
        if found_symmetric is False:
            symmetric_states.append([state2])

    return symmetric_states


########################################################
# Find Iz Sz subspace of totally symmetric vectors
def get_subspace(Nc, dim, Iz, Sz):
    Ibase_state = get_base_state(Nc, Iz)  # for example duu when Nc=3, Iz=1/2
    Sbase_state = get_base_state(Nc, Sz)  # for example dduu when Nc=4, Sz=0

    # get all combinations
    # ex: duu,udu,uud for flavor, same for spin, total 9 combinations
    all_states = get_all_states(Nc, Ibase_state, Sbase_state)
    # make list of sublists containing states related by interchanging 2 quarks
    symmetric_states = get_symmetric_states(Nc, all_states)
    # define subspace from set of symmetric states (add and normalize)
    subspace = np.zeros((len(symmetric_states), dim))
    for i, perms in enumerate(symmetric_states):
        normalization = np.sqrt(len(perms))
        for perm in perms:
            # convert string of binary state to integer index
            index = int(perm, 2)
            subspace[i][index] += 1 / normalization
    return subspace, symmetric_states


def convert_binary_to_state(Nc, state):
    state_dict = {'0': 'u', '1': 'd'}
    state_string_binary = [state[0][i:i + 2] for i in range(0, 2 * Nc, 2)]
    state_string = ''
    for i, string_binary in enumerate(state_string_binary):
        state_string += state_dict[string_binary[0]] + state_dict[string_binary[1]]
        if i != Nc - 1:
            state_string += ','
    return state_string


def print_input(Nc, I, Iz, S, Sz):
    print()
    print(f"Nc = {Nc}")
    print(f" I = {I}")
    print(f"Iz = {Iz}")
    print(f" S = {S}")
    print(f"Sz = {Sz}")
    print()


def check_fullspace_values(output, Nc, I, Iz, S, Sz, Ivalues, Svalues):
    if output is not None:
        print('Checking eigenvalues of I^2 and S^2 ...')
        print()
        Q_evals, _ = get_evals(Nc, I, Iz, S, Sz)
        check_eigenvalues(Ivalues, Q_evals, Svalues, Q_evals)


def check_subspace_values(output, Nc, I, Iz, S, Sz, Isub_values, Ssub_values):
    if output is not None:
        print()
        print("Checking eigenvalues of I^2 and S^2 subspaces\n ...")
        _, IS_sub_evals = get_evals(Nc, I, Iz, S, Sz)
        check_sub_eigenvalues(Isub_values, Ssub_values, IS_sub_evals)


def output_results(output, Nc, symmetric_basis, Isub_values, Isub_vectors, Ssub_values, Ssub_vectors):
    if output is not None:
        print()
        print("Basis")
        print('-----')
        for i, state in enumerate(symmetric_basis):
            print(f'v{i + 1}: {convert_binary_to_state(Nc, state)} type (sum over {len(state)} permutations)')
        print()
        print('Solution')
        print('--------')
        for i, (Ivalue, Ivector, Svalue, Svector) in enumerate(zip(Isub_values, Isub_vectors, Ssub_values, Ssub_vectors)):
            print(f'I^2 eigenvalue: {Ivalue}')
            print('I^2 eigen vector')
            print(Ivector / Ivector[0])
            print()
            print(f'S^2 eigenvalue: {Svalue}')
            print('S^2 eigen vector')
            print(Svector / Svector[0])
            print()


def human(Nc, state):
    state_dict = {'0': 'u', '1': 'd'}
    string = ''
    for q in range(Nc):
        string += state_dict[state[q * 2]]
        string += state_dict[state[q * 2 + 1]]
        if q != Nc-1:
            string += ','
    return string


def get_linear_comb(dim, I, S, basis, Isub_values, Isub_vectors):
    if I!=S: # this shouldn't happen until Nc>4
        print("Sorry, don't know which state to get because I != S")
        sys.exit(3)
        return 0

    else:
        Isub_values = [round(val,2) for val in Isub_values]
        vectorI = Isub_vectors[list(Isub_values).index(I*(I+1))]
        linear_comb = np.zeros(dim)
        basis_norm = 1/np.sqrt(sum([v**2 for v in vectorI]))
        for v, component in zip(basis, vectorI):
            for state in v:
                linear_comb[int(state, 2)] += basis_norm*component

        return linear_comb, vectorI, basis_norm,




def Weyl_to_Dirac(spin, basis):
    # assume spin up -> (1,0,0,0) Weyl
    # assume spin down -> (0,1,0,0) Weyl
    if spin == '0':
        if basis == 'Dirac':
            return np.array([1,0,-1,0])
        if basis == '2Weyl':
            return np.array([1,0])
        if basis == '4Weyl':
            return np.array([1,0,0,0])

    if spin == '1':
        if basis == 'Dirac':
            return np.array([0,1,0,-1])
        if basis == '2Weyl':
            return np.array([0,1])
        if basis == '4Weyl':
            return np.array([0,1,0,0])


def spin_d_from_basis(basis):
    if basis == 'Dirac' or basis == '4Weyl':
        spin_d = 4
    if basis == '2Weyl':
        spin_d = 2
    return spin_d


def get_Gamma_matrices(Nc, linear_comb, basis):
    '''
    # note that Gamma absorbs the numerical normalizations, to be divided out
    '''
    # first get the dimension of the spin matrices (spin_d x spin_d)
    spin_d = spin_d_from_basis(basis)
    # ASSUMES Nc=4?
    # construct rank 4 Gamma matrices (in Dirac basis)
    # one matrix for each combination of flavors
    max_num_flavor_combs = NF**Nc  # ex. uuuu, uudd, udud, uuud etc.
    # u_alpha u_beta d_sigma d_delta * Gamma_alpha,beta,sigma,delta
    Gamma = np.zeros((max_num_flavor_combs, spin_d**Nc))
    spins_each_flavor = [[] for each in range(max_num_flavor_combs)]
    factors_each_flavor = [[] for each in range(max_num_flavor_combs)]
    Gamma_index_list = []
    # loop over elements of linear combination
    for i, factor in enumerate(linear_comb):
        if factor != 0:
            # convert index to state ex 5 = '0101' = udud
            state_bin = bin(i)[2:]
            # add extra zeros to the front
            state_bin = '0'*(2*Nc - len(state_bin)) + state_bin

            # look at the flavors involved in this state, ex '0101' -> '0','0' = u,u
            flavor_state = [state_bin[i] for i in range(0, 2*Nc, 2)]
            # convert flavor state to int
            flavor_state_index = int(''.join(flavor_state), 2)
            Gamma_index_list.append(flavor_state_index)
            # look at the spins involved in this state, ex '0101' -> '0','0' = u,u
            spin_state = [state_bin[i] for i in range(1, 2*Nc + 1, 2)]
            # get 4d spinor for each
            spin_Dirac = [Weyl_to_Dirac(spin, basis) for spin in spin_state]
            spins_each_flavor[flavor_state_index].append(spin_state)
            factors_each_flavor[flavor_state_index].append(factor)
            for alpha in range(spin_d):
                for beta in range(spin_d):
                    for sigma in range(spin_d):
                        for delta in range(spin_d):
                            # convert spin indices to index using base spin_d (binary if 2Weyl basis)
                            spin_index = int(''.join([str(alpha), str(beta), str(sigma), str(delta)]), spin_d)
                            # f1_alpha f2_beta f3_sigma f4_delta * Gamma[f1,f2,f3,f4]_alpha,beta,sigma,delta
                            # product of spin_Dirac elements is either 0 or 1 or -1
                            # for case of Weyl spinors: if product is not zero, this is a unique spin flavor state
                            # for case of Dirac spinors: += in order to add other terms with same flavor but diff spin
                            Gamma[flavor_state_index, spin_index] += factor * spin_Dirac[0][alpha]\
                                                                            * spin_Dirac[1][beta] \
                                                                            * spin_Dirac[2][sigma] \
                                                                            * spin_Dirac[3][delta]
    return Gamma, Gamma_index_list, spins_each_flavor, factors_each_flavor


def confirm_Dirac_states(Nc, dim, Gamma, factors_each_flavor, linear_comb, basis):
    # first get the dimension of the spin matrices (spin_d x spin_d)
    spin_d = spin_d_from_basis(basis)
    # ASSUMES NC=4
    linear_comb_reconstructed = np.zeros((dim))
    for flavor_index, matrix in enumerate(Gamma):
        # get flavor state
        flavor_state = bin(flavor_index)[2:]
        # add extra zeros to the front
        flavor_state = '0'*(Nc - len(flavor_state)) + flavor_state
        # get Dirac spin state from Gamma matrix indices
        for alpha in range(spin_d):
            for beta in range(spin_d):
                for sigma in range(spin_d):
                    for delta in range(spin_d):
                        # convert spin indices to index using base spin_d (binary if 2Weyl basis)
                        spin_index = int(''.join([str(alpha), str(beta), str(sigma), str(delta)]), spin_d)
                        # +/-1 or 0 * numerical normalization factors
                        value = Gamma[flavor_index, spin_index]
                        # numerical factor coefficient
                        if abs(value) > 1e-6:
                            # combine this flavor state and this spin state to flavor-spin state
                            # note that this ONLY makes sense for 2Weyl and 4Weyl
                            # 4Weyl since only nonzero value for upper 2 components of spinor
                            state = flavor_state[0] + str(alpha) \
                                  + flavor_state[1] + str(beta) \
                                  + flavor_state[2] + str(sigma) \
                                  + flavor_state[3] + str(delta)
                            # convert binary
                            state_index = int(state, 2)
                            linear_comb_reconstructed[state_index] = value
    return bool(list(linear_comb_reconstructed) == list(linear_comb))


def test_Dirac(Nc, dim, basis='Dirac'):
    # example linear combination: 1/sqrt(2) [ 00,00,00,00  +  00,00,00,01 ]
    broken = False
    linear_comb_easy = np.zeros((dim))
    linear_comb_easy[0] = 1/np.sqrt(2)
    linear_comb_easy[1] = 1/np.sqrt(2)

    Dirac_Gamma, _, _, _ = get_Gamma_matrices(Nc, linear_comb_easy, basis)
    # get Dirac Gamma corresponding to flavor uuuu = 0

    Gamma_reconstruct = np.zeros((4**Nc))
    # all spin up -> u u u u spins
    # spin_up = [1,0,-1,0]
    # spin indices nonzero
    # 0 = +1
    # 2 = -1
    norm = 1/np.sqrt(2)

    Gamma_reconstruct[int(''.join(['0', '0', '0', '0']), 4)] += norm
    Gamma_reconstruct[int(''.join(['0', '0', '0', '2']), 4)] += -norm
    Gamma_reconstruct[int(''.join(['0', '0', '2', '0']), 4)] += -norm
    Gamma_reconstruct[int(''.join(['0', '0', '2', '2']), 4)] += norm

    Gamma_reconstruct[int(''.join(['0', '2', '0', '0']), 4)] += -norm
    Gamma_reconstruct[int(''.join(['0', '2', '0', '2']), 4)] += norm
    Gamma_reconstruct[int(''.join(['0', '2', '2', '0']), 4)] += norm
    Gamma_reconstruct[int(''.join(['0', '2', '2', '2']), 4)] += - norm

    Gamma_reconstruct[int(''.join(['2', '0', '0', '0']), 4)] += -norm
    Gamma_reconstruct[int(''.join(['2', '0', '0', '2']), 4)] += norm
    Gamma_reconstruct[int(''.join(['2', '0', '2', '0']), 4)] += norm
    Gamma_reconstruct[int(''.join(['2', '0', '2', '2']), 4)] += -norm
    Gamma_reconstruct[int(''.join(['2', '2', '0', '0']), 4)] += norm
    Gamma_reconstruct[int(''.join(['2', '2', '0', '2']), 4)] += -norm
    Gamma_reconstruct[int(''.join(['2', '2', '2', '0']), 4)] += -norm
    Gamma_reconstruct[int(''.join(['2', '2', '2', '2']), 4)] += norm


    # one spin down -> u u u d spins
    # spin_up = [1,0,-1,0]
    # spin_down = [0,1,0,-1]
    # 0,1 = +1
    # 2,3 = -1
    Gamma_reconstruct[int(''.join(['0', '0', '0', '1']), 4)] += norm
    Gamma_reconstruct[int(''.join(['0', '0', '0', '3']), 4)] += -norm
    Gamma_reconstruct[int(''.join(['0', '0', '2', '1']), 4)] += -norm
    Gamma_reconstruct[int(''.join(['0', '0', '2', '3']), 4)] += norm

    Gamma_reconstruct[int(''.join(['0', '2', '0', '1']), 4)] += -norm
    Gamma_reconstruct[int(''.join(['0', '2', '0', '3']), 4)] += norm
    Gamma_reconstruct[int(''.join(['0', '2', '2', '1']), 4)] += norm
    Gamma_reconstruct[int(''.join(['0', '2', '2', '3']), 4)] += -norm

    Gamma_reconstruct[int(''.join(['2', '0', '0', '1']), 4)] += -norm
    Gamma_reconstruct[int(''.join(['2', '0', '0', '3']), 4)] += norm
    Gamma_reconstruct[int(''.join(['2', '0', '2', '1']), 4)] += norm
    Gamma_reconstruct[int(''.join(['2', '0', '2', '3']), 4)] += -norm
    Gamma_reconstruct[int(''.join(['2', '2', '0', '1']), 4)] += norm
    Gamma_reconstruct[int(''.join(['2', '2', '0', '3']), 4)] += -norm
    Gamma_reconstruct[int(''.join(['2', '2', '2', '1']), 4)] += -norm
    Gamma_reconstruct[int(''.join(['2', '2', '2', '3']), 4)] += norm

    if list(Gamma_reconstruct) != list(Dirac_Gamma[0]):
        broken = True

    if broken:
        print()
        print(f"ERROR: problem with converting linear combination in {basis} basis!")
        print()
        sys.exit(3)


def test_Weyl(Nc, dim, basis='2Weyl'):
    # example linear combination: 1/sqrt(2) [ 00,00,00,00  +  00,00,00,01 ]
    broken = False
    linear_comb_easy = np.zeros((dim))
    linear_comb_easy[0] = 1/np.sqrt(2)
    linear_comb_easy[1] = 1/np.sqrt(2)

    Dirac_Gamma, _, _, factors_each_flavor = get_Gamma_matrices(Nc, linear_comb_easy, basis)

    # get Dirac Gamma corresponding to flavor uuuu = 0
    Gamma_uuuu = Dirac_Gamma[0]
    Gamma_uuuu_uuuu = Gamma_uuuu[0]  # spin_index = int(uuuu, 2 or 4) = 0
    Gamma_uuuu_uuud = Gamma_uuuu[1]  # spin_index = int(uuud, 2 or 4) = 1
    if abs(Gamma_uuuu_uuuu - 1/np.sqrt(2)) > 1e-6:
        broken = True
    if abs(Gamma_uuuu_uuud - 1/np.sqrt(2)) > 1e-6:
        broken = True
    if confirm_Dirac_states(Nc, dim, Dirac_Gamma, factors_each_flavor, linear_comb_easy, basis) is False:
        broken = True
    if broken:
        print()
        print(f"ERROR: problem with converting linear combination in {basis} basis!")
        print()
        sys.exit(3)


def check_Gamma(Nc, dim, linear_comb, basis):
    # test to make sure get_Gamma_matrices function works using baby example
    test_Weyl(Nc, dim, '2Weyl')
    test_Dirac(Nc, dim, 'Dirac')

    Gamma_matrices, Gamma_index_list, spin_each_flavor, factor_each_flavor = get_Gamma_matrices(Nc, linear_comb, basis)

    # reconstruct linear combination from spin matrices
    if basis == '4Weyl' or basis == '2Weyl':
        correct = confirm_Dirac_states(Nc, dim, Gamma_matrices, factor_each_flavor, linear_comb, basis)
        if not correct:
            print("Problem with converting to Dirac")
            sys.exit(3)
    else:
        print('Have not checked spin matrix')



def get_Gamma_workflow(Nc, linear_comb, basis):
    """
    :param Nc: int, number of colors
    :param linear_comb: 1D np array of floats, int(flavor_spin_state, 2) = index,
                        example, ud,du,ud,ud = 01,10,01,01 = int('01100101',2)=101
                        -> linear_comb[101] = coefficient of ud,du,ud,ud term
    :param basis: string, one of 4Dirac, 4Weyl, 2Dirac, determines basis of spin matrix
    :return: dictionary of dictionaries
                spin_matrices['f1f2f3f4']['factor'] = coefficient of this term, float
                spin_matrices['f1f2f3f4']['matrix'] = 4D np array of size 2^4 or 4^4 depending on basis
                such that
                        f1f2f3f4_term =
                        f1_alpha f2_beta f3_sigma f4_delta
                        * spin_matrices['f1f2f3f4']['matrix][alpha, beta, sigma, delta]
                and fully symmetric operator is given by
                Baryon = sum_{f1,f2,f3,f4 permutations} ( spin_matrices['f1f2f3f4']['factor'] * f1f2f3f4_term )
    """

    # first get the dimension of the spin matrices (spin_d x spin_d)
    spin_d = spin_d_from_basis(basis)
    # get relevant data
    Gamma_matrices, Gamma_index_list, spin_each_flavor, factor_each_flavor = get_Gamma_matrices(Nc, linear_comb, basis)
    print('In gamma workflow, gamma matrix shape is')
    print(Gamma_matrices.shape)
    # construct dictionary
    spin_matrices_dict = {}
    for i, (spins, factor, spin_matrix) in enumerate(zip(spin_each_flavor, factor_each_flavor, Gamma_matrices)):
        # only include relevant flavor combinations in the dictionary
        if len(spins) != 0:
            flavor_state = bin(i)[2:]
            flavor_state = '0' * (Nc - len(flavor_state)) + flavor_state
            coefficient = max(factor)
            # separate coefficient from spin matrix containing only 0s and +/-1s
            spin_matrix = spin_matrix/coefficient
            spin_matrix = np.reshape(spin_matrix, newshape=(spin_d, spin_d, spin_d, spin_d))
            spin_matrices_dict[flavor_state] = {'factor': factor, 'matrix': spin_matrix}

    return spin_matrices_dict


def print_human_form(human_form, Nc, I, Iz, S, Sz, symmetric_basis, spinor_basis, vectorI, basis_norm, linear_comb):
    if human_form:
        print()
        print()
        print('----- HUMAN READABLE ---- TWO WAYS ------')
        print(f'Flavor-spin wave function for I={I}, Iz={Iz}, S={S}, Sz={Sz}')
        print()
        print()
        print()
        for term, (v, component) in enumerate(zip(symmetric_basis, vectorI)):
            # print each vector on a line
            print_string = f'{basis_norm * component} x [ '
            for i, state in enumerate(v):
                print_string += human(Nc, state)
                if i != len(v) - 1:
                    print_string += ' + '
            print_string += ' ]'
            print(print_string)

            if term != len(symmetric_basis) - 1:
                print(' + ')
        print()
        print()

        Gamma_matrices, Gamma_index_list, spin_each_flavor, factor_each_flavor = get_Gamma_matrices(Nc, linear_comb,
                                                                                                    spinor_basis)
        for i, (spins, factor) in enumerate(zip(spin_each_flavor, factor_each_flavor)):
            if len(spins) != 0:
                flavor_state = bin(i)[2:]
                flavor_state = '0' * (Nc - len(flavor_state)) + flavor_state
                print(f'FLAVOR: {flavor_state}')
                print('SPINS x factor')
                print([''.join(spin) for spin in spins])
                print([str(round(f, 2)) for f in factor])
            print()
        print()


def check_permutations(Nc, q1, q2, flavors, spin_matrices_dict):
    # coeff_orig = spin_matrices_dict[flavors]['factor']
    # coeff_perm = spin_matrices_dict[flavors_perm]['factor']
    # if coeff_perm == coeff_orig:

    ind = np.arange(Nc)
    # if q1 < q2:
    #     axes_perm = ind[:q1] + ind[q2] + ind[q1+1:q2] + ind[q1] + ind[q2+1:]
    # else: # q1 > q2:
    #     axes_perm = ind[:q2] + ind[q1] + ind[q2+1:q1] + ind[q2] + ind[q1+1:]
    # print(q1, q2)
    # print(axes_perm)
    # matrix_orig = spin_matrices_dict[flavors]['matrix']
    # matrix_perm = matrix_orig.transpose(matrix_orig, axes=axes_perm)
    #
    # return np.array_equal(matrix_perm, matrix_orig)


# Nc = 4 hardwired function
def spin_matrix_symmetries(Nc, spin_matrices_dict):
    """
    find where spin_matrices are equal under exchange of particles
    :param spin_matrices_dict: as described in get_Gamma_workflow
                spin_matrices['f1f2f3f4']['factor'] = coefficient of this term, float
                spin_matrices['f1f2f3f4']['matrix'] = 4D np array of size 2^4 or 4^4 depending on basis
    :return:
    """
    # get flavor combinations
    for flavors in spin_matrices_dict.keys():
        print(flavors)
        # just look at Nc-1 consecutive permutations
        for q1 in range(Nc-1):
            q2 = q1 + 1
            check_permutations(Nc, q1, q2, flavors, spin_matrices_dict)
        print()


# Nc =4 hardwired function
def check_S2_I2(Nc, spin_matrices_dict):
    # matrix constructed from code
    spin_mat = spin_matrices_dict['0000']['matrix']

    # construct matrix by hand, check that Dirac matrix for S=2 I=2 is as expected
    # for Dirac 'up', nonzero indices are 0 and 2
    # Dirac up = [1,0,-1,0]
    # get all combinations of 4 0s and 2s equivalent to all binary up to 16=2**4, and replace 1s with 2s
    # keep track of -1 factors - appear in result when odd number of 1s (which become 2s) appear in binary
    # get list of indices where spin matrix should be +/- 1
    matrix_by_hand = np.zeros((4, 4, 4, 4))
    for i in range(16):
        # get original binary
        indices_str = bin(i)[2:]
        indices_str = '0' * (Nc - len(indices_str)) + indices_str
        print(indices_str)

        # replace 1s with 2s, and count number of 2s
        indices = []
        num_2s = 0
        for index in indices_str:
            if index == '0':
                indices.append(int(index))
            if index == '1':
                indices.append(2)
                num_2s += 1
        matrix_by_hand[indices[0], indices[1], indices[2], indices[3]] = (-1) ** num_2s

    return np.allclose(spin_mat, matrix_by_hand)


def check_Dirac_matrix_S2_I2(Nc, Iz, Sz, spinor_basis, spin_matrices_dict):
    if Sz == 2 and Iz == 2 and spinor_basis == 'Dirac':
        correct = check_S2_I2(Nc, spin_matrices_dict)
        if correct:
            print('Good job!')
        else:
            print('Yikes! Sz=2, Iz=2 wrong.')


def spin_matrix_to_file(Nc, I, Iz, S, Sz, spinor_basis, spin_matrices_dict):
    #if spinor_basis == 'Dirac':
    spin_d = 4
    print('Saving matrices to files.')
    #else:
    #    print('Not saving the spin matrices to files.')
    #    return
    # text file in format
    # alpha beta sigma delta matrix[alpha, beta, sigma, delta]
    # num rows = 4**Nc, num columns = Nc + 1
    for flavors in spin_matrices_dict.keys():
        matrix = spin_matrices_dict[flavors]['matrix']
        with open(f'Nc{Nc}_I{I}_Iz{Iz}_S{S}_Sz{Sz}_{flavors}.txt', 'w+') as f:
            # instead of Nc for loops, just get all permutations with repeats of spin indices
            all_indices = itertools.product(np.arange(spin_d), repeat=Nc)
            for i, indices in enumerate(all_indices):
                for ind in indices:
                    f.write(f'{ind} ')
                f.write(f'{matrix[tuple(indices)]}\n')
            f.close()


def get_operators(quantum_numbers,spinor_basis, verbose=False):
    Nc = quantum_numbers['nc']#int(sys.argv[1])
    I = float(quantum_numbers['I'])#sys.argv[2])
    Iz = float(quantum_numbers['Iz'])#sys.argv[3])
    S = float(quantum_numbers['S'])#sys.argv[4])
    Sz = float(quantum_numbers['Sz'])#sys.argv[5])

    print_input(Nc, I, Iz, S, Sz)
    # check_I_S(Nc, I, S)
    # 2 choices for each flavor, 2 choices for each spin, Nc quarks in a baryon
    dim = (2 * 2) ** Nc
    ########################################################
    # First compute I^2, S^2 matrix for each individual quark
    # note that for any given state of Nc qaurks, I^2 of any indiv quark is still I(I+1)
    # Iisq |state> = I*(I+1) |state> (always 1/2 since fermion!)
    Iisq = [1 / 2 * (1 / 2 + 1) * np.identity(dim)]*Nc
    Sisq = [1 / 2 * (1 / 2 + 1) * np.identity(dim)]*Nc
    ########################################################
    # compute Iz operator for each quark
    Iiz = [get_Siz(Nc, dim, 2 * i) for i in range(Nc)]  # (2*i)th place of |f1 s1 f2 s2 f3 s3 ..> = fi
    Siz = [get_Siz(Nc, dim, 2 * i + 1) for i in range(Nc)]  # (2*i+1)th place of |f1 s1 f2 s2 f3 s3 ..> = si
    ########################################################
    # compute I+ and I-, S+ and S-
    # example I1p|00 00 10> = |00 00 00>
    Ii_pm = [get_S_plus_minus(Nc, dim, 2 * i) for i in range(Nc)]  # (2*i)th place of |f1 s1 f2 s2 f3 s3 ..> = fi
    Si_pm = [get_S_plus_minus(Nc, dim, 2 * i + 1) for i in range(Nc)]  # (2*i+1)th place of |f1 s1 f2 s2 f3 s3 ..> = si
    ########################################################
    # compute total I^2 and S^2 matrix, using I^2 = (I1 + I2 + I3 + ...)^2
    Isq = compute_Ssq_total(Nc, dim, Iisq, Iiz, Ii_pm)
    Ssq = compute_Ssq_total(Nc, dim, Sisq, Siz, Si_pm)
    ########################################################
    # compute eigen values of I^2 and S^2 (as check)
    Ivalues, Ivectors = np.linalg.eig(Isq)
    Svalues, Svectors = np.linalg.eig(Ssq)
    check_fullspace_values(verbose, Nc, I, Iz, S, Sz, Ivalues, Svalues)

    ########################################################
    # Find S^2 and I^2 basis within the subspace
    subspace, symmetric_basis = get_subspace(Nc, dim, Iz, Sz)
    Isq_subspace = np.matmul(np.matmul(subspace, Isq), np.transpose(subspace))
    Ssq_subspace = np.matmul(np.matmul(subspace, Ssq), np.transpose(subspace))

    Isub_values, Isub_vectors = np.linalg.eig(Isq_subspace)
    Ssub_values, Ssub_vectors = np.linalg.eig(Ssq_subspace)
    Isub_vectors = Isub_vectors.transpose()
    Ssub_vectors = Ssub_vectors.transpose()

    ########################################################
    # check to make sure eigen values are correct
    check_subspace_values(verbose, Nc, I, Iz, S, Sz, Isub_values, Ssub_values)

    ########################################################
    # output results: basis, vectors with corresponding eigenvalues
    output_results(verbose, Nc, symmetric_basis, Isub_values, Isub_vectors, Ssub_values, Ssub_vectors)

    # get result as a 1D array indicating linear combination of all possible flavor spin state terms
    linear_comb, vectorI, basis_norm = get_linear_comb(dim, I, S, symmetric_basis, Isub_values, Isub_vectors)

    # get the set of rank Nc Dirac matrices that combine all of the spins for each flavor combo
    check_Gamma(Nc, dim, linear_comb, spinor_basis)

    # get spin matrix dictionary for next part of workflow
    spin_matrices_dict = get_Gamma_workflow(Nc, linear_comb, spinor_basis)
    
    # find symmetries of spin matrices
    # symm = spin_matrix_symmetries(Nc, spin_matrices_dict)
    # print(symm)

    # check that DIRAC spin matrix is correct for simple case
    #check_Dirac_matrix_S2_I2(Nc, Iz, Sz, spinor_basis, spin_matrices_dict)

    # save Gamma matrix to text file for use in C code
    spin_matrix_to_file(Nc, I, Iz, S, Sz, spinor_basis, spin_matrices_dict)

    
    return spin_matrices_dict


    
            
def main(spinor_basis='2Weyl', output=False, human_form=True):
    Nc = int(sys.argv[1])
    I = float(sys.argv[2])
    Iz = float(sys.argv[3])
    S = float(sys.argv[4])
    Sz = float(sys.argv[5])
    print_input(Nc, I, Iz, S, Sz)
    # check_I_S(Nc, I, S)
    # 2 choices for each flavor, 2 choices for each spin, Nc quarks in a baryon
    dim = (2 * 2) ** Nc
    ########################################################
    # First compute I^2, S^2 matrix for each individual quark
    # note that for any given state of Nc qaurks, I^2 of any indiv quark is still I(I+1)
    # Iisq |state> = I*(I+1) |state> (always 1/2 since fermion!)
    Iisq = [1 / 2 * (1 / 2 + 1) * np.identity(dim)]*Nc
    Sisq = [1 / 2 * (1 / 2 + 1) * np.identity(dim)]*Nc
    ########################################################
    # compute Iz operator for each quark
    Iiz = [get_Siz(Nc, dim, 2 * i) for i in range(Nc)]  # (2*i)th place of |f1 s1 f2 s2 f3 s3 ..> = fi
    Siz = [get_Siz(Nc, dim, 2 * i + 1) for i in range(Nc)]  # (2*i+1)th place of |f1 s1 f2 s2 f3 s3 ..> = si
    ########################################################
    # compute I+ and I-, S+ and S-
    # example I1p|00 00 10> = |00 00 00>
    Ii_pm = [get_S_plus_minus(Nc, dim, 2 * i) for i in range(Nc)]  # (2*i)th place of |f1 s1 f2 s2 f3 s3 ..> = fi
    Si_pm = [get_S_plus_minus(Nc, dim, 2 * i + 1) for i in range(Nc)]  # (2*i+1)th place of |f1 s1 f2 s2 f3 s3 ..> = si
    ########################################################
    # compute total I^2 and S^2 matrix, using I^2 = (I1 + I2 + I3 + ...)^2
    Isq = compute_Ssq_total(Nc, dim, Iisq, Iiz, Ii_pm)
    Ssq = compute_Ssq_total(Nc, dim, Sisq, Siz, Si_pm)
    ########################################################
    # compute eigen values of I^2 and S^2 (as check)
    Ivalues, Ivectors = np.linalg.eig(Isq)
    Svalues, Svectors = np.linalg.eig(Ssq)
    check_fullspace_values(output, Nc, I, Iz, S, Sz, Ivalues, Svalues)

    ########################################################
    # Find S^2 and I^2 basis within the subspace
    subspace, symmetric_basis = get_subspace(Nc, dim, Iz, Sz)
    Isq_subspace = np.matmul(np.matmul(subspace, Isq), np.transpose(subspace))
    Ssq_subspace = np.matmul(np.matmul(subspace, Ssq), np.transpose(subspace))

    Isub_values, Isub_vectors = np.linalg.eig(Isq_subspace)
    Ssub_values, Ssub_vectors = np.linalg.eig(Ssq_subspace)
    Isub_vectors = Isub_vectors.transpose()
    Ssub_vectors = Ssub_vectors.transpose()

    ########################################################
    # check to make sure eigen values are correct
    check_subspace_values(output, Nc, I, Iz, S, Sz, Isub_values, Ssub_values)

    ########################################################
    # output results: basis, vectors with corresponding eigenvalues
    output_results(output, Nc, symmetric_basis, Isub_values, Isub_vectors, Ssub_values, Ssub_vectors)

    # get result as a 1D array indicating linear combination of all possible flavor spin state terms
    linear_comb, vectorI, basis_norm = get_linear_comb(dim, I, S, symmetric_basis, Isub_values, Isub_vectors)

    # get the set of rank Nc Dirac matrices that combine all of the spins for each flavor combo
    check_Gamma(Nc, dim, linear_comb, spinor_basis)

    # print human readable result
    print_human_form(human_form, Nc, I, Iz, S, Sz, symmetric_basis, spinor_basis, vectorI, basis_norm, linear_comb)

    # get spin matrix dictionary for next part of workflow
    spin_matrices_dict = get_Gamma_workflow(Nc, linear_comb, spinor_basis)


    
    print(spin_matrices_dict)

    # find symmetries of spin matrices
    # symm = spin_matrix_symmetries(Nc, spin_matrices_dict)
    # print(symm)

    # check that DIRAC spin matrix is correct for simple case
    #check_Dirac_matrix_S2_I2(Nc, Iz, Sz, spinor_basis, spin_matrices_dict)

    # save Gamma matrix to text file for use in C code
    spin_matrix_to_file(Nc, I, Iz, S, Sz, spinor_basis, spin_matrices_dict)


if __name__ == "__main__":
    main(spinor_basis='4Weyl', output=True, human_form=True)
