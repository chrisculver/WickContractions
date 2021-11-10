from WickContractions.diags.diagram import Diagram
import pytest

def test_diagram_fails():
    with pytest.raises(Exception):
        Diagram(0.,[])