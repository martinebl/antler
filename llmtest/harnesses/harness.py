#!/usr/bin/env python3
from llmtest.probes import Probe
from llmtest.evaluator import Evaluator
from llmtest.explorers import Explorer
from llmtest.generators import Generator
from llmtest.attempt import Attempt
from llmtest.logwriter import LogWriter

class Harness:
    """ This is the base harness class, that coordinates probes, transformers and generators """

    def __init__(self, probes: list[Probe], explorer: Explorer, generator_type: type[Generator], model: str, options: dict = {}, repetitions: int = 1) -> None:
        self.generator_type = generator_type
        self.model = model
        self.probes = probes
        self.explorer = explorer
        self.options = options
        self.repetitions = repetitions
        self.log_writer = LogWriter()
    
    def run(self) -> None:
        """
        The method that runs the explorer to generate the transforms, and then
        applies the transforms to the probes and run them on the generator.
        Lastly the probe detectors are run on the given answers, and the results are evaluated.
        """

        self.log_writer.setLogRunParams(str(self.generator_type), self.model, self.options, self.repetitions)
        attempts = self.collectAttempts()
        self.log_writer.logAttempts(attempts)
        self.evaluateAttempts(attempts)

    def evaluateAttempts(self, attempts):
        evaluator = Evaluator()
        evaluation = evaluator.evaluate(attempts)
        self.log_writer.logReport(str(evaluation))
        evaluation.prettyPrint()

    def collectAttempts(self) -> list[Attempt]:
        raise NotImplementedError("Implement this in subclass")

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