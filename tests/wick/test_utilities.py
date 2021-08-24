import src.wick.utilities as utils
import src.ops.quarks as quarks

def test_perms():
  assert sorted([[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]) == sorted([[i for i in lst] for lst in utils.permutations([1,2,3])])

  assert utils.arePermsEqualParity([1,2,3],[1,3,2])==False
  assert utils.arePermsEqualParity([1,2,3],[3,1,2])==True


def test_quarks_pairwise():
    qu1=quarks.Quark(True,'u',"s0","c0","t0","x0")
    qu2=quarks.Quark(True,'u',"s0","c0","t0","x0")
    qu3=quarks.Quark(True,'d',"s0","c0","t0","x0")

    qd1=quarks.Quark(False,'u',"s0","c0","t0","x0")
    qd2=quarks.Quark(False,'u',"s0","c0","t0","x0")
    qd3=quarks.Quark(False,'d',"s0","c0","t0","x0")
    qd4=quarks.Quark(False,'s',"s0","c0","t0","x0")

    unbarred=[qu1,qu2,qu3]
    barred1=[qd1,qd2,qd3]
    barred2=[qd1,qd2,qd3,qd4]
    barred3=[qd1,qd4,qd3]
    assert utils.quarks_pairwise_same_flavor(unbarred,barred1)==True
    assert utils.quarks_pairwise_same_flavor(unbarred,barred2)==False
    assert utils.quarks_pairwise_same_flavor(unbarred,barred3)==False
