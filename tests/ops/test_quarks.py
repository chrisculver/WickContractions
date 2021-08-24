from src.ops.quarks import Quark, ShortQuark


def test_equality():
    q1 = Quark(True,'u',"s0","c0","t0","x0")
    q2 = Quark(True,'u',"s0","c0","t0","x0")
    qb = Quark(False,'u',"s0","c0","t0","x0")
    qf = Quark(True,'f',"s0","c0","t0","x0")
    qs = Quark(True,'u',"s1","c0","t0","x0")
    qc = Quark(True,'u',"s0","c1","t0","x0")
    qt = Quark(True,'u',"s0","c0","t1","x0")
    qx = Quark(True,'u',"s0","c0","t0","x1")

    assert q1==q2
    assert q1!=qb
    assert q1!=qf
    assert q1!=qs
    assert q1!=qc
    assert q1!=qt
    assert q1!=qx

    q1 = ShortQuark(True,'u',"label0")
    q2 = ShortQuark(True,'u',"label0")
    qb = ShortQuark(False,'u',"label0")
    qf = ShortQuark(True,'d',"label0")
    ql = ShortQuark(True,'u',"label1")

    assert q1==q2
    assert q1!=qb
    assert q1!=qf
    assert q1!=ql


def test_print():
    q1 = Quark(True,'u',"s0","c0","t0","x0")
    assert str(q1)=="\\bar{u}_{s0 c0}(x0, t0)"

    q2 = Quark(False,'u',"s0","c0","t0","x0")
    assert str(q2)=="u_{s0 c0}(x0, t0)"

    q1 = ShortQuark(True,'u',"l0")
    assert str(q1)=="\\bar{u}_{l0}"

    q2 = ShortQuark(False,'u',"l0")
    assert str(q2)=="u_{l0}"
