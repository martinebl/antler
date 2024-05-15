import pytest

from antler.explorers import Explorer
from antler.transforms import Transform
from antler.explorers.exhaustivesearch import ExhaustiveSearch
from antler.explorers.bestinclassexplorer import BestInClassExplorer
from antler.explorers.simulatedannealing import SimulatedAnnealing
from antler.explorers.greedyhillclimbexplorer import GreedyHillClimbExplorer
from antler.explorers.heuristichillclimbexplorer import HeuristicHillClimbExplorer

from antler.techniques.refusalsuppression import RefusalSuppression
from antler.techniques.acceptingprefix import AcceptingPrefix
from antler.techniques.addnoise import AddNoise
from antler.techniques.encoding import Encoding
from antler.techniques.obfuscatingcode import ObfuscatingCode
from antler.techniques.convincemissingknowledge import ConvinceMissingKnowledge
from antler.techniques.escapeuserprompt import EscapeUserPrompt
from antler.techniques.nonnaturallanguage import NonNaturalLanguage


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

def test_simulated_annealing_exchange_out_class():
    annealing = SimulatedAnnealing([AddNoise(), Encoding(), ObfuscatingCode(), ConvinceMissingKnowledge()])
    transform = Transform([ AddNoise(), Encoding() ])
    transform = annealing._SimulatedAnnealing__exchangeFromOutsideClass(transform)
    assert len(transform.getTechniques()) == 2
    assert ConvinceMissingKnowledge() in transform.getTechniques()

def test_simulated_annealing_exchange_from_class():
    annealing = SimulatedAnnealing([AddNoise(), Encoding(), ObfuscatingCode(), ConvinceMissingKnowledge(), EscapeUserPrompt(), NonNaturalLanguage() ])
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
    
@pytest.mark.parametrize("transforms, expected", [
    ([AddNoise(), Encoding(), ObfuscatingCode(), ConvinceMissingKnowledge()], 12),
    ([AddNoise(), Encoding(), ObfuscatingCode()], 6),
    ([AddNoise(), Encoding()], 2),
])
def test_ghce_increment_transform_length(transforms, expected):
    ghce = GreedyHillClimbExplorer(transforms)
    new_transforms = ghce._GreedyHillClimbExplorer__incrementTransformsLength(ghce.transforms)
    assert(len(new_transforms) == expected)

# @pytest.mark.parametrize("transforms, expected", [
#     ([AcceptingPrefix(), AddNoise(), Encoding(), ConvinceMissingKnowledge(), ObfuscatingCode(), EscapeUserPrompt()], 126),
#     ([AcceptingPrefix(), AddNoise(), Encoding(), ConvinceMissingKnowledge(), ObfuscatingCode()], 85),
#     ([AcceptingPrefix(), AddNoise(), Encoding(), ConvinceMissingKnowledge()], 46),
#     ([AcceptingPrefix(), AddNoise(), Encoding()], 15),
#     ([AddNoise(), Encoding()], 4),
#     ([AddNoise()], 1),
# ])
# def test_ghce_runs_correct_amount_of_transforms(transforms, expected):
#     explorer = GreedyHillClimbExplorer(transforms)
#     count = 0
#     for transform in explorer:
#         count +=1
#         print(transform)
#         explorer.seedScore(0.1)
#         assert(isinstance(transform, Transform))
#     assert(count == expected)

def test_ghce_stops_at_100_percent_transform():
    explorer = GreedyHillClimbExplorer([AcceptingPrefix(), AddNoise(), Encoding()])
    count = 0
    for transform in explorer:
        count +=1
        print(transform)
        explorer.seedScore(1)
        assert(isinstance(transform, Transform))
    assert(count == 3)

def test_hhce_selects_correct_starting_point():
    hhce = HeuristicHillClimbExplorer([AcceptingPrefix(), AddNoise(), Encoding()])
    hhce.setHeuristic([
        (Transform([AcceptingPrefix(), AddNoise()]), 1),
        (Transform([AddNoise(), AcceptingPrefix()]), 1),
        (Transform([AddNoise(), Encoding()]), 0.8),
        (Transform([Encoding(), AcceptingPrefix()]), 0.7),
    ])
    sp: tuple[Transform, float] = hhce.selectStartingPoint()
    assert sp[0] == Transform([AcceptingPrefix(), AddNoise()]) and sp[1] == 1


def test_hhce_selects_and_removes_best_heuristic():
    hhce = HeuristicHillClimbExplorer([AcceptingPrefix(), AddNoise(), Encoding()])
    hhce.setHeuristic([
        (Transform([AcceptingPrefix(), AddNoise()]), 1),
        (Transform([AddNoise(), AcceptingPrefix()]), 1),
        (Transform([AddNoise(), Encoding()]), 0.8),
        (Transform([Encoding(), AcceptingPrefix()]), 0.7),
    ])
    sp: tuple[Transform, float] = hhce.selectStartingPoint()
    nx, _ = hhce.selectBestHeuristic(sp[0])

    assert nx == Transform([AddNoise(), Encoding()])
    assert hhce.getHeuristic() == [
        (Transform([Encoding(), AcceptingPrefix()]), 0.7),
    ]

# @pytest.mark.parametrize("transform, extension, prepend, expected", [
#     (Transform([AcceptingPrefix(), AddNoise()]), Transform([AddNoise(), Encoding()]), False, Transform([AcceptingPrefix(), AddNoise(), Encoding()])),
#     (Transform([AcceptingPrefix(), AddNoise()]), Transform([Encoding(), AddNoise()]), True, Transform([Encoding(), AcceptingPrefix(), AddNoise()])),
# ])
# def test_hhce_extends_with_heuristic(transform, extension, prepend, expected):
#     hhce = HeuristicHillClimbExplorer([AcceptingPrefix(), AddNoise(), Encoding()])
#     new = hhce.extendTransform(transform, extension, prepend)

#     assert new == expected

def test_remove_transform_from_heuristic():
    h = [(Transform(AddNoise()), 1), (Transform(Encoding()), 0.5)]
    h = HeuristicHillClimbExplorer._HeuristicHillClimbExplorer__removeTransformFromHeuristic(h, Transform(AddNoise()))
    assert h == [(Transform(Encoding()), 0.5)]
