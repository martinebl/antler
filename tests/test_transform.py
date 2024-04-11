import pytest
from llmtest.transforms import Transform
from llmtest.techniques.acceptingprefix import AcceptingPrefix
from llmtest.techniques.refusalsuppression import RefusalSuppression
from llmtest.techniques.addnoise import AddNoise


@pytest.mark.parametrize("transform1, transform2, result", [
    (Transform([]), Transform([]), True),
    (Transform([]), Transform([AcceptingPrefix()]), False),
    (Transform([RefusalSuppression()]), Transform([AcceptingPrefix()]), False),
    (Transform([AddNoise()]), Transform([AddNoise()]), True),
])
def test_equality(transform1, transform2, result):
    assert (transform1 == transform2) == result