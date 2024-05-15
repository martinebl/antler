import pytest
import random
import backoff

from antler.generators import Generator

class SometimesFailingEmptyGenerator(Generator):
    def __init__(self, model: str, options: dict = ...) -> None:
        super().__init__(model, options)
        self.fail = True

    @backoff.on_exception(backoff.fibo, TimeoutError, max_tries=20, on_backoff=lambda x: print("Backing off from timeout"))
    @backoff.on_predicate(backoff.fibo, lambda ans: len(ans)==0, max_tries=20, on_backoff=lambda x: print("Backing off from empty return value"))
    def generate(self, prompt: str) -> str:
        if self.fail:
            self.fail = False
            raise(TimeoutError("The connection timed out!"))
        else:
            self.fail = True
            return "This is an answer that might work" if random.randint(0, 100) % 2 == 0 else ""

def raise_not_implemented():
    generator = Generator("model")
    generator.generate("prompt")

def test_not_implemented():
    with pytest.raises(NotImplementedError):
        raise_not_implemented()

def test_backoff_generate():
    gen = SometimesFailingEmptyGenerator("test")
    # There is a very small chance that this might fail, but with 20 tries, it should not happen
    assert gen.generate("Whatever") == "This is an answer that might work"