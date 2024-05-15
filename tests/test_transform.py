import pytest
from antler.transforms import Transform
from antler.techniques.acceptingprefix import AcceptingPrefix
from antler.techniques.refusalsuppression import RefusalSuppression
from antler.techniques.addnoise import AddNoise


@pytest.mark.parametrize("transform1, transform2, result", [
    (Transform([]), Transform([]), True),
    (Transform([]), Transform([AcceptingPrefix()]), False),
    (Transform([RefusalSuppression()]), Transform([AcceptingPrefix()]), False),
    (Transform([AddNoise()]), Transform([AddNoise()]), True),
])
def test_equality(transform1, transform2, result):
    assert (transform1 == transform2) == result

def test_is_same_combination():
    own = Transform([AcceptingPrefix(), AddNoise()])
    other = Transform([AddNoise(), AcceptingPrefix()])

    assert own.isSameCombination(other)
