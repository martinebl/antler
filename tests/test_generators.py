import pytest
from llmtest.generators import Generator

def raise_not_implemented():
    generator = Generator("model")
    generator.generate("prompt")

def test_not_implemented():
    with pytest.raises(NotImplementedError):
        raise_not_implemented()