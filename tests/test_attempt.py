import pytest
from antler.transforms import Transform
from antler.techniques.acceptingprefix import AcceptingPrefix
from antler.techniques.refusalsuppression import RefusalSuppression
from antler.techniques.addnoise import AddNoise
from antler.attempt import Attempt
from antler.probes.cursewordfuck import CurseWordFuck
from antler.probes.illegaldrugs import IllegalDrugs


@pytest.mark.parametrize("attempt1, attempt2, result", [
    (Attempt(Transform([]), CurseWordFuck()), Attempt(Transform([]), CurseWordFuck()), True),
    (Attempt(Transform([ AddNoise() ]), CurseWordFuck()), Attempt(Transform([ RefusalSuppression() ]), CurseWordFuck()), False),
    (Attempt(Transform([ AddNoise() ]), CurseWordFuck()), Attempt(Transform([ AddNoise() ]), IllegalDrugs()), False),
    (Attempt(Transform([ AddNoise() ]), CurseWordFuck()), Attempt(Transform([ AddNoise() ]), CurseWordFuck()), True),
    (Attempt(Transform([ AcceptingPrefix() ]), IllegalDrugs()), Attempt(Transform([ AcceptingPrefix() ]), IllegalDrugs()), True),
])
def test_is_same(attempt1, attempt2, result):
    assert Attempt.isSame(attempt1, attempt2) == result