from WickContractions.diags.propagator import PropIndex

def test_index():
    p=PropIndex('c','s')
    assert str(p)=='c s'