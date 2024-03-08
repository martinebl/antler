import pytest
from llmtest.explorers import Explorer
from llmtest.transforms import Transform
from llmtest.explorers.exhaustivesearch import ExhaustiveSearch
from llmtest.techniques.refusalsuppression import RefusalSuppression
from llmtest.techniques.acceptingprefix import AcceptingPrefix

def test_base_explorer_generate_transforms_not_implemented():
    with pytest.raises(NotImplementedError):
        Explorer([]).generateInitialTransforms()

def test_base_explorer_feed_result_not_implemented():
    with pytest.raises(NotImplementedError):
        Explorer([]).seedScore()

def test_exhaustive_search_generation():
    explorer = ExhaustiveSearch([AcceptingPrefix(), RefusalSuppression()])
    transforms = explorer.generateInitialTransforms()
    assert(len(transforms) == 4)

def test_exhaustive_search_iteration():
    explorer = ExhaustiveSearch([AcceptingPrefix(), RefusalSuppression()])
    count = 0
    for transform in explorer:
        count +=1
        explorer.seedScore(1)
        assert(isinstance(transform, Transform))
    assert(count == 4)