#!/usr/bin/env python3
from llmtest.generators.gpt4all import GPT4all
from llmtest.transforms import Transform
from llmtest.probes import Probe
from llmtest.result import Result
from llmtest.evaluator import Evaluator
from llmtest.explorers import Explorer

class Harness:
    """ This is the base harness class, that coordinates probes, transformers and generators """

    def __init__(self, model, probes: list[Probe], explorer: Explorer) -> None:
        self.generator = GPT4all(model, {})
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
        