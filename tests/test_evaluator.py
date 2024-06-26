import pytest
from collections import Counter

from antler.evaluator import Evaluator
from antler.evaluation import Evaluation
from antler.attempt import Attempt
from antler.transforms.transform import Transform
from antler.result import Result
from antler.probes.illegaldrugs import IllegalDrugs
from antler.probes.cursewordfuck import CurseWordFuck
from antler.techniques.acceptingprefix import AcceptingPrefix
from antler.techniques.refusalsuppression import RefusalSuppression

@pytest.fixture
def evaluator():
    return Evaluator()

@pytest.fixture
def probes():
    return [IllegalDrugs(), CurseWordFuck()]

@pytest.fixture
def techniques():
    return [AcceptingPrefix(), RefusalSuppression()]

def test_add_to_dict_on_empty_adds_entry(evaluator):
    dict = { }
    key = "key"
    val = 1.0
    evaluator.addToDict(dict, key, val, val, val)

    assert len(dict.items()) > 0
    assert dict[key] == [(val, val, val)]

def test_create_result_list_makes_list_of_res_from_dict(evaluator):
    dict = {
        "name1": [(1.1, 1, 1), (2.1, 1, 1), (3.1, 1, 1), (4.1, 1, 1), (5.1, 1, 1)],
        "name2": [(1.2, 1, 1), (2.2, 1, 1), (3.2, 1, 1), (4.2, 1, 1), (5.2, 1, 1)],
        "name3": [(1.3, 1, 1), (2.3, 1, 1), (3.3, 1, 1), (4.3, 1, 1), (5.3, 1, 1)]
    }

    res_list = evaluator.createResultList(dict)

    assert type(res_list) == list
    for res in res_list:
        assert type(res) == Result
        assert dict[res.name] == res.attempt_scores

def test_evaluate(evaluator):
    att1 = Attempt(Transform([ AcceptingPrefix() ]), CurseWordFuck())
    att1.addResponse("fuck", True)

    att2 = Attempt(Transform([]), IllegalDrugs())
    att2.addResponse("cocaine", True)

    attempts = [att1, att2]

    expected_evaluation = Evaluation(
        [Result("AcceptingPrefix", [(1.0, 1, 1)])],
        [Result("(AcceptingPrefix,)", [(1.0, 1, 1)])],
        [Result("CurseWordFuck", [(1.0, 1, 1)]), Result("IllegalDrugs", [(-1, 1, 1)])],
        0, 2        
    )

    evaluation = evaluator.evaluate(attempts)
    assert type(evaluation) == Evaluation

    # deep comparison
    assert str(evaluation) == str(expected_evaluation)

@pytest.mark.parametrize("input, expected_output", [
    ("(a,b,c,)", ["a", "b", "c"]),
    ("(b,a,c,)", ["b", "a", "c"]),
    ("(a,)", ["a"]),
    ("()", []),
])
def test_transform_result_name_to_array(input, expected_output, evaluator):
    output = Evaluation.transformResultNameToArray(input)
    assert Counter(output) == Counter(expected_output)

@pytest.mark.parametrize("input, expected_output", [
    ([
        Result("()", [(1,1,1)]),
    ], [
        Result("()", [(1,1,1)]),
    ]),
    ([
        Result("(a,c,)", [(1,1,1)]),
        Result("(c,)", [(1,1,1)]),
        Result("(c,a,)", [(1,1,1)]),
    ], [
        Result("(c,)", [(1,1,1)]),
        Result("(a,c,)", [(1,1,1)]),
        Result("(c,a,)", [(1,1,1)]),
    ]),
    ([
        Result("(b,a,c,)", [(1,1,1)]),
        Result("(a,c,)", [(1,1,1)]),
        Result("(c,)", [(1,1,1)]),
        Result("(a,b,c,)", [(1,1,1)]),
        Result("(c,a,)", [(1,1,1)]),
        Result("(c,)", [(1,1,1)]),
    ], [
        Result("(c,)", [(1,1,1)]),
        Result("(c,)", [(1,1,1)]),
        Result("(a,c,)", [(1,1,1)]),
        Result("(c,a,)", [(1,1,1)]),
        Result("(b,a,c,)", [(1,1,1)]),
        Result("(a,b,c,)", [(1,1,1)]),
    ])
])
def test_sort_trans_combination(input, expected_output, evaluator):
    output = evaluator.sortTransformResByCombination(input)
    assert output == expected_output

@pytest.mark.parametrize("input, expected_output", [
    ([
        Result("(c,)", [(1,1,1)]),
        Result("(a,c,)", [(1,1,1)]),
    ], [
        Result("(c,)", [(1,1,1)]),
        Result("(a,c,)", [(1,1,1)]),
    ]),
    ([
        Result("(a,c,)", [(1,1,1)]),
        Result("(c,)", [(1,1,1)]),
    ], [
        Result("(c,)", [(1,1,1)]),
        Result("(a,c,)", [(1,1,1)]),
    ]),
    ([
        Result("(a,c,)", [(1,1,1)]),
        Result("(a,b,c,)", [(1,1,1)]),
        Result("(c,)", [(1,1,1)]),
    ], [
        Result("(c,)", [(1,1,1)]),
        Result("(a,c,)", [(1,1,1)]),
        Result("(a,b,c,)", [(1,1,1)]),
    ]),
    (
       [
        Result("()", [(1,1,1)]),
        Result("()", [(1,1,1)]),
        Result("()", [(1,1,1)]),
    ], [
        Result("()", [(1,1,1)]),
        Result("()", [(1,1,1)]),
        Result("()", [(1,1,1)]),
    ] 
    )
])
def test_sort_trans_res_len(input, expected_output, evaluator):
    output = evaluator.sortTransformResByLen(input)
    assert output == expected_output