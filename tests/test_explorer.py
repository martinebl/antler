import pytest
from llmtest.explorers import Explorer
from llmtest.explorers.exhaustivesearch import ExhaustiveSearch
from llmtest.exploits.refusalsuppression import RefusalSuppression
from llmtest.exploits.acceptingprefix import AcceptingPrefix

def test_base_explorer_not_implemented():
    with pytest.raises(NotImplementedError):
        Explorer([]).generateTransforms()

def test_exhaustive_search():
    explorer = ExhaustiveSearch([AcceptingPrefix(), RefusalSuppression()])
    transforms = explorer.generateTransforms()
    assert(len(transforms) == 4)