import pytest
from llmtest.explorers import Explorer
from llmtest.transforms import Transform
from llmtest.explorers.exhaustivesearch import ExhaustiveSearch
from llmtest.exploits.refusalsuppression import RefusalSuppression
from llmtest.exploits.acceptingprefix import AcceptingPrefix

def test_base_explorer_generate_transforms_not_implemented():
    with pytest.raises(NotImplementedError):
        Explorer([]).generateTransforms()

def test_base_explorer_feed_result_not_implemented():
    with pytest.raises(NotImplementedError):
        Explorer([]).feedResult()

def test_exhaustive_search_generation():
    explorer = ExhaustiveSearch([AcceptingPrefix(), RefusalSuppression()])
    transforms = explorer.generateTransforms()
    assert(len(transforms) == 4)

def test_exhaustive_search_iteration():
    explorer = ExhaustiveSearch([AcceptingPrefix(), RefusalSuppression()])
    count = 0
    for transform in explorer:
        count +=1
        explorer.feedResult(True)
        assert(isinstance(transform, Transform))
    assert(count == 4)