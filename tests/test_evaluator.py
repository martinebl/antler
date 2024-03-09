import pytest
from llmtest.evaluator import Evaluator
from llmtest.evaluation import Evaluation
from llmtest.result import Result
from llmtest.attempt import Attempt
from llmtest.transforms import Transform
from llmtest.probes.illegaldrugs import IllegalDrugs
from llmtest.probes.cursewordfuck import CurseWordFuck
from llmtest.techniques.acceptingprefix import AcceptingPrefix
from llmtest.techniques.refusalsuppression import RefusalSuppression

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