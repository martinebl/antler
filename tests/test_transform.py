import pytest
from llmtest.transforms import Transform
from llmtest.techniques.acceptingprefix import AcceptingPrefix
from llmtest.techniques.refusalsuppression import RefusalSuppression
from llmtest.techniques.addnoise import AddNoise


@pytest.mark.parametrize("transform1, transform2, result", [
    (Transform([]), Transform([]), True),
    (Transform([]), Transform([(1, AcceptingPrefix())]), False),
    (Transform([(1, RefusalSuppression())]), Transform([(1, AcceptingPrefix())]), False),
    (Transform([(1, AddNoise())]), Transform([(1, AddNoise())]), True),
])
def test_equality(transform1, transform2, result):
    assert (transform1 == transform2) == result