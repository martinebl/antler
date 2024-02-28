#!/usr/bin/env python3
from llmtest.probes import Probe
from llmtest.evaluator import Evaluator
from llmtest.explorers import Explorer
from llmtest.generators import Generator

class Harness:
    """ This is the base harness class, that coordinates probes, transformers and generators """

    def __init__(self, probes: list[Probe], explorer: Explorer, generator_type: type[Generator], model: str, model_options: dict = {}) -> None:
        self.generator = generator_type(model, model_options)
        self.probes = probes
        self.explorer = explorer
    
    def run(self) -> None:
        """
        The method that runs the explorer to generate the transforms, and then
        applies the transforms to the probes and run them on the generator.
        Lastly the probe detectors are run on the given answers, and the results are evaluated.
        """
        raise NotImplementedError("This method should be implemented in subclasses")

    def evaluateResults(self, results):
        evaluator = Evaluator()
        evaluation = evaluator.evaluate(results)
        print(evaluation)
        