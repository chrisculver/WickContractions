.. _contractions:

Contraction Algorithm
=====================

To contract two operators call the function :func:`contract` passing in two
operators as parameters.  The function then takes all of the commuting objects
and adjoins them into a single list.  Then it takes all the quarks, and makes
two lists, one containing the quarks, and another containing the anti-quarks.
Then the :func:`quark_contract` is called, which performs the wick contractions
on the quarks.  T

This is performed by finding all possible permutations of the quarks.  Then
the list of anti-quarks is compared with each permutation list of the quarks.
If the quark flavors match in order, then the quarks can be combined into a
valid propagator, and the permutation will produce a valid diagram.  Otherwise
the permutation is discarded.

As an explicit example, given the lists

..  math::
    \text{barred}=(\bar{u}, \bar{u}, \bar{d})\\\\
    p_1 = (d, u, u)\\\\
    p_2 = (u, u, d)

The :math:`\text{barred}` list would not create a valid diagram with :math:`p_1`
while it does create a valid diagram with :math:`p_2`.
