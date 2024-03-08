import pytest
from llmtest.evaluator import Evaluator
from llmtest.evaluation import Evaluation
from llmtest.result import Result
from llmtest.attempt import Attempt
from llmtest.transforms import Transform
from llmtest.probes.illegaldrugs import IllegalDrugs
from llmtest.probes.cursewordfuck import CurseWordFuck
from llmtest.exploits.acceptingprefix import AcceptingPrefix
from llmtest.exploits.refusalsuppression import RefusalSuppression

@pytest.fixture
def evaluator():
    return Evaluator()

@pytest.fixture
def probes():
    return [IllegalDrugs(), CurseWordFuck()]

@pytest.fixture
def exploits():
    return [AcceptingPrefix(), RefusalSuppression()]

def test_add_to_dict_on_empty_adds_entry(evaluator):
    dict = { }
    key = "key"
    val = 1.0
    evaluator.addToDict(dict, key, val)

    assert len(dict.items()) > 0
    assert dict[key] == [val]

def test_create_result_list_makes_list_of_res_from_dict(evaluator):
    dict = {
        "name1": [1.1, 2.1, 3.1, 4.1, 5.1],
        "name2": [1.2, 2.2, 3.2, 4.2, 5.2],
        "name3": [1.3, 2.3, 3.3, 4.3, 5.3]
    }

    res_list = evaluator.createResultList(dict)

    assert type(res_list) == list
    for res in res_list:
        assert type(res) == Result
        assert dict[res.name] == res.attempt_scores

def test_evaluate(evaluator):
    att1 = Attempt(Transform([(1, AcceptingPrefix())]), CurseWordFuck())
    att1.addResponse("fuck", True)

    att2 = Attempt(Transform([]), IllegalDrugs())
    att2.addResponse("cocaine", True)

    attempts = [att1, att2]

    expected_evaluation = Evaluation(
        [Result("AcceptingPrefix", [1.0])],
        [Result("(AcceptingPrefix,)", [1.0])],
        [Result("CurseWordFuck", [1.0]), Result("IllegalDrugs", [-1])]
    )

    evaluation = evaluator.evaluate(attempts)
    assert type(evaluation) == Evaluation

    # deep comparison
    assert str(evaluation) == str(expected_evaluation)


# def test_evaluate_returns_evaluation(evaluator):
#     actual_evaluation = evaluator.evaluate([])
#     assert Evaluation == type(actual_evaluation)

# def test_returns_empty_evaluation_given_no_results(evaluator):
#     actual_evaluation = evaluator.evaluate([])
#     expected_evaluation = Evaluation([], {})

#     assert actual_evaluation.clean_hit_payloads == expected_evaluation.clean_hit_payloads
#     assert actual_evaluation.exploit_scores == actual_evaluation.exploit_scores

# def test_creates_evaluation_with_payload_of_clean_hits(evaluator, probes):
#     res = Result(Transform([]), 2, probes)

#     actual_evaluation = evaluator.evaluate([res])
#     expected_evaluation = Evaluation(list(map(lambda x: x.payload, probes)), {})

#     assert actual_evaluation.clean_hit_payloads == expected_evaluation.clean_hit_payloads
#     assert actual_evaluation.exploit_scores == actual_evaluation.exploit_scores
    
# def test_creates_evaluation_with_correct_exploit_names(evaluator, exploits):
#     expected_exploit_names = list(map(lambda x: type(x).__name__, exploits))
#     results = [
#         Result(Transform([(1, AcceptingPrefix()), (1, RefusalSuppression())]), 2, []),
#         Result(Transform([(1, RefusalSuppression()), (1, AcceptingPrefix())]), 2, []),
#         Result(Transform([(1, RefusalSuppression())]), 1, []),
#         Result(Transform([(1, AcceptingPrefix())]), 1, [])
#         ]
#     evaluation = evaluator.evaluate(results)

#     actual_exploit_names = list(evaluation.exploit_scores.keys())
#     assert Counter(actual_exploit_names) == Counter(expected_exploit_names)

# @pytest.mark.parametrize("results, expected_output", [
#     (
#         [
#             Result(Transform([(1, AcceptingPrefix()), (1, RefusalSuppression())]),  2,  [CurseWordFuck(), IllegalDrugs()]),
#             Result(Transform([(1, RefusalSuppression()), (1, AcceptingPrefix())]),  2,  [CurseWordFuck(), IllegalDrugs()]),
#             Result(Transform([(1, RefusalSuppression())]),                          2,  [CurseWordFuck(), IllegalDrugs()]),
#             Result(Transform([(1, AcceptingPrefix())]),                             2,  [CurseWordFuck(), IllegalDrugs()])
#         ], 
#         {'RefusalSuppression': [1, 1, 1], 'AcceptingPrefix': [1, 1, 1]}
#     ),
#     (
#         [
#             Result(Transform([(1, AcceptingPrefix()), (1, RefusalSuppression())]),  0,  [CurseWordFuck(), IllegalDrugs()]),
#             Result(Transform([(1, RefusalSuppression()), (1, AcceptingPrefix())]),  0,  [CurseWordFuck(), IllegalDrugs()]),
#             Result(Transform([(1, RefusalSuppression())]),                          0,  [CurseWordFuck(), IllegalDrugs()]),
#             Result(Transform([(1, AcceptingPrefix())]),                             0,  [CurseWordFuck(), IllegalDrugs()])
#         ], 
#         {'RefusalSuppression': [0, 0, 0], 'AcceptingPrefix': [0, 0, 0]}
#     ),
#     (
#         [
#             Result(Transform([(1, AcceptingPrefix()), (1, RefusalSuppression())]),  1,  [CurseWordFuck(), IllegalDrugs()]),
#             Result(Transform([(1, RefusalSuppression()), (1, AcceptingPrefix())]),  0,  [CurseWordFuck(), IllegalDrugs()]),
#             Result(Transform([(1, RefusalSuppression())]),                          0,  [CurseWordFuck(), IllegalDrugs()]),
#             Result(Transform([(1, AcceptingPrefix())]),                             0,  [CurseWordFuck(), IllegalDrugs()])
#         ], 
#         {'RefusalSuppression': [0, 0.5, 0], 'AcceptingPrefix': [0, 0.5, 0]}
#     ),
#     (
#         [
#             Result(Transform([(1, AcceptingPrefix()), (1, RefusalSuppression())]),  2,  [CurseWordFuck(), IllegalDrugs()]),
#             Result(Transform([(1, RefusalSuppression()), (1, AcceptingPrefix())]),  1,  [CurseWordFuck(), IllegalDrugs()]),
#             Result(Transform([(1, RefusalSuppression())]),                          0,  [CurseWordFuck(), IllegalDrugs()]),
#             Result(Transform([(1, AcceptingPrefix())]),                             0,  [CurseWordFuck(), IllegalDrugs()])
#         ], 
#         {'RefusalSuppression': [1, 0.5, 0], 'AcceptingPrefix': [1, 0.5, 0]}
#     ),
#     (
#         [
#             Result(Transform([(1, AcceptingPrefix()), (1, RefusalSuppression())]),  2,  [CurseWordFuck(), IllegalDrugs()]),
#             Result(Transform([(1, RefusalSuppression()), (1, AcceptingPrefix())]),  1,  [CurseWordFuck(), IllegalDrugs()]),
#             Result(Transform([(1, RefusalSuppression())]),                          2,  [CurseWordFuck(), IllegalDrugs()]),
#             Result(Transform([(1, AcceptingPrefix())]),                             2,  [CurseWordFuck(), IllegalDrugs()])
#         ], 
#         {'RefusalSuppression': [1, 0.5, 1], 'AcceptingPrefix': [1, 0.5, 1]}
#     ),
# ])
# def test_collects_scores_of_type_exploit_in_list(results, expected_output, evaluator):
#     evaluation = evaluator.evaluate(results)

#     assert Counter(list(evaluation.exploit_scores.keys())) == Counter(list(expected_output.keys()))
#     for key in list(evaluation.exploit_scores.keys()):
#         assert Counter(evaluation.exploit_scores[key]) == Counter(expected_output[key])