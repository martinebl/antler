#!/usr/bin/env python3
from llmtest.probes import Probe
from llmtest.evaluator import Evaluator
from llmtest.explorers import Explorer
from llmtest.generators import Generator
from llmtest.attempt import Attempt

class Harness:
    """ This is the base harness class, that coordinates probes, transformers and generators """

    def __init__(self, probes: list[Probe], explorer: Explorer, generator_type: type[Generator], model: str, model_options: dict = {}, repetitions: int = 1) -> None:
        self.generator = generator_type(model, model_options)
        self.probes = probes
        self.explorer = explorer
        self.repetitions = repetitions
    
    def run(self) -> None:
        """
        The method that runs the explorer to generate the transforms, and then
        applies the transforms to the probes and run them on the generator.
        Lastly the probe detectors are run on the given answers, and the results are evaluated.
        """
        raise NotImplementedError("This method should be implemented in subclasses")

    def evaluateAttempts(self, attempts):
        evaluator = Evaluator()
        evaluation = evaluator.evaluate(attempts)
        print(evaluation)

    """ This method is quadratic and could be optimized """
    @staticmethod
    def collapseSameAttempts(attempts):
        same_indices = []
        for i in range(len(attempts)):
            for j in range(i + 1, len(attempts)):
                if  Attempt.isSame(attempts[i], attempts[j]):
                    attempts[i].addResponseObject(*attempts[j].getReplies())
                    same_indices.append(j)
                    
        for index in sorted(set(same_indices), reverse=True):
            del attempts[index]
        
    @staticmethod
    def runAttempt(args: tuple[object, Attempt]):
        harness, attempt = args
        generator = harness.generator if(hasattr(harness, "generator")) else harness.generator_type(harness.model, harness.options)
        answer = generator.generate(attempt.getPrompt())
        detection = attempt.getProbe().runDetectors(answer)
        attempt.addResponse(answer, detection)
        return attempt
    
    def collectAttempts(self) -> list[Attempt]:
        return NotImplementedError("Implement this in subclass")