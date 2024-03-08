import pytest
from llmtest.explorers import Explorer
from llmtest.transforms import Transform
from llmtest.explorers.exhaustivesearch import ExhaustiveSearch
from llmtest.explorers.classexplorer import ClassExplorer
from llmtest.techniques.refusalsuppression import RefusalSuppression
from llmtest.techniques.acceptingprefix import AcceptingPrefix
from llmtest.techniques.addnoise import AddNoise
from llmtest.techniques.encoding import Encoding

def test_base_explorer_generate_transforms_not_implemented():
    with pytest.raises(NotImplementedError):
        Explorer([]).generateInitialTransforms()

def test_base_explorer_seed_result_not_implemented():
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

def test_classexplorer_search_generation():
    explorer = ClassExplorer([AcceptingPrefix(), RefusalSuppression()])
    transforms = explorer.generateInitialTransforms()
    assert(len(transforms) == 2)

def test_classexplorer_search_normal_iteration():
    explorer = ClassExplorer([AcceptingPrefix(), RefusalSuppression()])
    count = 0
    for transform in explorer:
        count +=1
        explorer.seedScore(1)
        assert(isinstance(transform, Transform))
    assert(count == 4)
    assert(len(explorer.scores) == 2)

def test_classexplorer_removes_bad_technique_in_class():
    explorer = ClassExplorer([AcceptingPrefix(), AddNoise(), Encoding()])
    count = 0
    for transform in explorer:
        count +=1
        explorer.seedScore(1)
        assert(isinstance(transform, Transform))
    assert(count == 5) # One for each technique, plus the two permuations of the two best techniques
    assert(len(explorer.scores) == 3)