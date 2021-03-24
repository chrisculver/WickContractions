.. _sec-operators:

Operators
=========

Here we write our operators as follows,

..  math::
   O_{\alpha\beta}=a(\prod_i C^i_{\alpha})(\prod_j q^j_{\beta}),

where :math:`a` is a constant, :math:`C` is a commuting object, and :math:`q`
is an anti-commuting object.  The superscripts just indicate that there's a
product of many such objects.  The subscript is a label representing multiple
indices (spin, color, ...).  When filling in the full index list, Einstein
summation convention will be used.  As long as our operators are input in this
format we can do the following to compute the contractions, described in
Contractions.

We call all commuting objects and :ref:py:class:Indexed_Object, since it will have
spin/color/eigenvector indices.
