#!/usr/bin/env python3
from llmtest.generators.gpt4all import GPT4all
from llmtest.transformers import Transformer
from llmtest.probes import Probe
from llmtest.result import Result
from llmtest.evaluator import Evaluator
from enum import Enum

class Answer(Enum):
    SUCCESS = 1
    FAILURE = 2

class Harness:
    """ This is the base harness class, that coordinates probes, transformers and generators """

    def __init__(self, model, probes: list[Probe], transformers: list[Transformer]) -> None:
        
        self.generator = GPT4all(model, {})
        self.probes = probes
        self.transformers = transformers

    
    def run(self) -> None:
        
        results = []
        print("Running penetration tests ...")
        for i, probe in enumerate(self.probes):
            payload = probe.getPayload()
            applied_transforms = []

            print("Probe %i/%i" % (i+1, len(self.probes)))
            # checking in the payload without exploits fails
            only_payload_answer = self.generator.generate(probe.getPayload())
            if probe.runDetectors(only_payload_answer): 
                applied_transforms = None
            else:
                for j, transform in enumerate(self.transformers):
                    prompt = transform.applyExploits(probe.getPayload())
                    answer = self.generator.generate(prompt)
                    status = Answer.FAILURE if probe.runDetectors(answer) else Answer.SUCCESS
                    print("   Transform %i/%i" % (j+1, len(self.transformers)))

                    applied_transforms.append((transform, status))

            results.append(Result(payload, applied_transforms))
        
        evaluator = Evaluator()
        evaluation = evaluator.evaluate(results)
        print(evaluation)
        