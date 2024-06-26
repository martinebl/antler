#!/usr/bin/env python3
import time

from antler.probes import Probe
from antler.techniques import Technique
from antler.evaluator import Evaluator
from antler.explorers import Explorer
from antler.generators import Generator
from antler.attempt import Attempt
from antler.logwriter import LogWriter

class Harness:
    """ This is the base harness class, that coordinates probes, transformers and generators """

    def __init__(self, probes: list[Probe], explorer_type: type[Explorer], techniques: list[Technique], generator_type: type[Generator], api_key: str, model: str, options: dict = {}, repetitions: int = 1, max_queries: int = 10) -> None:
        self.generator_type = generator_type
        self.api_key = api_key
        self.model = model
        self.probes = probes
        self.explorer_type = explorer_type
        self.techniques = techniques
        self.options = options
        self.repetitions = repetitions
        self.log_writer = LogWriter()
        self.max_queries = max_queries
    
    def run(self) -> None:
        """
        The method that runs the explorer to generate the transforms, and then
        applies the transforms to the probes and run them on the generator.
        Lastly the probe detectors are run on the given answers, and the results are evaluated.
        """

        start_time = time.time()

        self.log_writer.LogRunParams({
            "generator_type": self.generator_type.__name__,
            "explorer": self.explorer_type.__name__,
            "model": self.model,
            "model_options": self.options,
            "repetitions": self.repetitions,
        })

        attempts = self.collectAttempts()
        self.log_writer.fixAttemptFileEnding()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.formatted_time = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
        
        self.evaluateAttempts(attempts)

    def evaluateAttempts(self, attempts):
        evaluator = Evaluator()
        evaluation = evaluator.evaluate(attempts)
        evaluation.setElapsedTime(self.formatted_time)
        self.log_writer.logReport(str(evaluation))
        evaluation.prettyPrint()

    def collectAttempts(self) -> list[Attempt]:
        raise NotImplementedError("Implement this in subclass")

    """ This method is quadratic and could be optimized """
    @staticmethod
    def collapseSameAttempts(attempts: list[Attempt]) -> list[Attempt]:
        local_attempts = attempts.copy()
        for i in range(len(local_attempts)):
            first_attempt = local_attempts[i]
            for j in range(i + 1, len(local_attempts)):
                second_attempt = local_attempts[j]
                if Attempt.isSame(first_attempt, second_attempt):
                    for reply in second_attempt.getReplies():
                        first_attempt.addResponseObject(reply)
        key_function = lambda x: type(x.getProbe()).__name__
        seen = set()
        return [x for x in local_attempts if key_function(x) not in seen and not seen.add(key_function(x))]


    @staticmethod
    def runAttempt(args: tuple[object, Attempt]):
        harness, attempt = args
        generator = harness.generator if(hasattr(harness, "generator")) else harness.generator_type(harness.model, harness.api_key, harness.options)
        # Handle if a connection times out or other network errors
        try:
            answer = generator.generate(attempt.getPrompt())

            # Run the technique tests, to see if the answer might be encoded or transformed
            # in a way that will affect detection. Fix it, if this is the case
            techniques = attempt.getTransform().getTechniques().copy()
            techniques.reverse()
            for technique in techniques:
                if technique.isAnswerAffected(answer):
                    answer = technique.cleanAffectedAnswer(answer)

            detection = attempt.getProbe().runDetector(answer)
            attempt.addResponse(answer, detection)
        except KeyboardInterrupt:
            # Let the keyboard interrupt propagate upwards
            raise
        except Exception as e:
            attempt.addResponseWithError(str(e))
        return attempt
    
    def logTransformAttempts(self, attempts: list[Attempt]):
        self.log_writer.logTransformAttempts(attempts)
        