import pytest
from llmtest.transforms import Transform
from llmtest.techniques.acceptingprefix import AcceptingPrefix
from llmtest.techniques.refusalsuppression import RefusalSuppression
from llmtest.techniques.addnoise import AddNoise
from llmtest.attempt import Attempt
from llmtest.probes.cursewordfuck import CurseWordFuck
from llmtest.probes.illegaldrugs import IllegalDrugs


@pytest.mark.parametrize("attempt1, attempt2, result", [
    (Attempt(Transform([]), CurseWordFuck()), Attempt(Transform([]), CurseWordFuck()), True),
    (Attempt(Transform([(1, AddNoise())]), CurseWordFuck()), Attempt(Transform([(1, RefusalSuppression())]), CurseWordFuck()), False),
    (Attempt(Transform([(1, AddNoise())]), CurseWordFuck()), Attempt(Transform([(1, AddNoise())]), IllegalDrugs()), False),
    (Attempt(Transform([(1, AddNoise())]), CurseWordFuck()), Attempt(Transform([(1, AddNoise())]), CurseWordFuck()), True),
])
def test_is_same(attempt1, attempt2, result):
    assert Attempt.isSame(attempt1, attempt2) == result