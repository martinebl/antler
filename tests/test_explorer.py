import pytest
from llmtest.explorers import Explorer
from llmtest.transforms import Transform
from llmtest.explorers.exhaustivesearch import ExhaustiveSearch
from llmtest.explorers.bestinclassexplorer import BestInClassExplorer
from llmtest.techniques.refusalsuppression import RefusalSuppression
from llmtest.techniques.acceptingprefix import AcceptingPrefix
from llmtest.techniques.addnoise import AddNoise
from llmtest.techniques.encoding import Encoding
from llmtest.techniques.convincemissingknowledge import ConvinceMissingKnowledge

def test_base_explorer_generate_transforms_not_implemented():
    with pytest.raises(NotImplementedError):
        Explorer([]).generateInitialTransforms()

def test_base_explorer_seed_result_not_implemented():
    with pytest.raises(NotImplementedError):
        Explorer([]).seedScore()

@pytest.mark.parametrize("explorer, length", [
    (ExhaustiveSearch([AcceptingPrefix(), RefusalSuppression()]), 4),
    (ExhaustiveSearch([AcceptingPrefix(), RefusalSuppression(), AddNoise()]), 15),
    (ExhaustiveSearch([AcceptingPrefix(), RefusalSuppression(), AddNoise(), Encoding()]), 64),
    (ExhaustiveSearch([AcceptingPrefix(), RefusalSuppression(), AddNoise(), Encoding(), ConvinceMissingKnowledge()]), 325),
])
def test_exhaustive_search_generation(explorer, length):
    transforms = explorer.generateInitialTransforms()
    assert(len(transforms) == length)

def test_exhaustive_search_iteration():
    explorer = ExhaustiveSearch([AcceptingPrefix(), RefusalSuppression()])
    count = 0
    for transform in explorer:
        count +=1
        explorer.seedScore(1)
        assert(isinstance(transform, Transform))
    assert(count == 4)

def test_bestinclassExplorer_search_generation():
    explorer = BestInClassExplorer([AcceptingPrefix(), RefusalSuppression()])
    transforms = explorer.generateInitialTransforms()
    assert(len(transforms) == 2)

def test_bestinclassexplorer_search_normal_iteration():
    explorer = BestInClassExplorer([AcceptingPrefix(), RefusalSuppression()])
    count = 0
    for transform in explorer:
        count +=1
        explorer.seedScore(1)
        assert(isinstance(transform, Transform))
    assert(count == 4)
    assert(len(explorer.scores) == 2)

def test_bestinclassexplorer_removes_bad_technique_in_class():
    explorer = BestInClassExplorer([AcceptingPrefix(), AddNoise(), Encoding()])
    count = 0
    for transform in explorer:
        count +=1
        explorer.seedScore(1)
        assert(isinstance(transform, Transform))
    assert(count == 5) # One for each technique, plus the two permuations of the two best techniques
    assert(len(explorer.scores) == 3)