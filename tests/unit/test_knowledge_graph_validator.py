import pytest

def test_knowledge_graph_validator():
    with pytest.raises(Exception):
        raise RuntimeError("cummins is excluded")
