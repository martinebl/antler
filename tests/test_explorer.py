import pytest

from llmtest.explorers import Explorer
from llmtest.transforms import Transform
from llmtest.explorers.exhaustivesearch import ExhaustiveSearch
from llmtest.explorers.bestinclassexplorer import BestInClassExplorer
from llmtest.explorers.simulatedannealing import SimulatedAnnealing
from llmtest.techniques.refusalsuppression import RefusalSuppression
from llmtest.techniques.acceptingprefix import AcceptingPrefix
from llmtest.techniques.addnoise import AddNoise
from llmtest.techniques.encoding import Encoding
from llmtest.techniques.obfuscatingcode import ObfuscatingCode
from llmtest.techniques.convincemissingknowledge import ConvinceMissingKnowledge
from llmtest.techniques.escapeuserprompt import EscapeUserPrompt
from llmtest.techniques.nonnaturallanguage import NonNaturalLanguage


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

def test_simulated_annealing_selection():
    annealing = SimulatedAnnealing([AddNoise(), Encoding(), ObfuscatingCode(), ConvinceMissingKnowledge()])
    count = 0
    for _ in annealing:
        annealing.seedScore(count / 4)
        count += 1
    print(annealing.scores)
    print(annealing.best_techniques)
    assert len(annealing.best_techniques) == 3
    assert len(annealing.scores) == 4

def test_simulated_annealing_exchange_out_class():
    annealing = SimulatedAnnealing([AddNoise(), Encoding(), ObfuscatingCode(), ConvinceMissingKnowledge()])
    # Just for testing. The exchange function uses best_techniques instead of techniques
    annealing.best_techniques = annealing.techniques
    transform = Transform([ AddNoise(), Encoding() ])
    transform = annealing._SimulatedAnnealing__exchangeFromOutsideClass(transform)
    assert len(transform.getTechniques()) == 2
    assert ConvinceMissingKnowledge() in transform.getTechniques()

def test_simulated_annealing_exchange_from_class():
    annealing = SimulatedAnnealing([AddNoise(), Encoding(), ObfuscatingCode(), ConvinceMissingKnowledge(), EscapeUserPrompt(), NonNaturalLanguage() ])
    # Just for testing. The exchange function uses best_techniques instead of techniques
    annealing.best_techniques = annealing.techniques
    transform = Transform([ AddNoise(), Encoding() ])
    changed_transform = annealing._SimulatedAnnealing__exchangeFromClass(transform)
    assert len(changed_transform.getTechniques()) == len(transform.getTechniques())
    assert ObfuscatingCode() in changed_transform.getTechniques()
    assert transform != changed_transform
    # These techniques both have only 1 per class
    new_transform = Transform([EscapeUserPrompt(), NonNaturalLanguage()])
    same_transform = annealing._SimulatedAnnealing__exchangeFromClass(new_transform)
    assert new_transform == same_transform

def test_simulated_annealing_swap_non_consecutive():
    annealing = SimulatedAnnealing([])
    transform = Transform([ AddNoise(), Encoding(), EscapeUserPrompt() ])
    swapped_transform = annealing._SimulatedAnnealing__swapNonConsecutive(transform)
    assert swapped_transform == Transform([ EscapeUserPrompt(), Encoding(), AddNoise()])
    new_transform = Transform([ AddNoise(), Encoding(), EscapeUserPrompt(), ConvinceMissingKnowledge() ])
    new_swapped = annealing._SimulatedAnnealing__swapNonConsecutive(new_transform)
    assert len(new_swapped.getTechniques()) == len(new_transform.getTechniques())
    assert all(tech in new_swapped.getTechniques() for tech in new_transform.getTechniques())

def test_simulated_annealing_swap_consecutive():
    annealing = SimulatedAnnealing([])
    transform = Transform([ AddNoise(), Encoding() ])
    swapped_transform = annealing._SimulatedAnnealing__swapConsecutive(transform)
    assert swapped_transform == Transform([Encoding(), AddNoise()])
    new_transform = Transform([ AddNoise(), Encoding(), ObfuscatingCode() ])
    swapped_new = annealing._SimulatedAnnealing__swapConsecutive(new_transform)
    assert len(swapped_new.getTechniques()) == len(new_transform.getTechniques())
    assert all(tech in swapped_new.getTechniques() for tech in new_transform.getTechniques())