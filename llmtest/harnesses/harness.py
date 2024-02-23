#!/usr/bin/env python3
from llmtest.generators.gpt4all import GPT4all
from llmtest.transforms import Transform
from llmtest.probes import Probe
from llmtest.result import Result
from llmtest.evaluator import Evaluator
from enum import Enum

class Harness:
    """ This is the base harness class, that coordinates probes, transformers and generators """

    def __init__(self, model, probes: list[Probe], transforms: list[Transform]) -> None:
        
        self.generator = GPT4all(model, {})
        self.probes = probes
        self.transforms = transforms

    
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
                for j, transform in enumerate(self.transforms):
                    print("   Transform %i/%i" % (j+1, len(self.transforms)))
                    prompt = transform.applyExploits(probe.getPayload())
                    answer = self.generator.generate(prompt)
                    isHit = probe.runDetectors(answer)
                    applied_transforms.append((transform, isHit))

            results.append(Result(payload, applied_transforms))
        
        self.evaluateResults(results)

    def evaluateResults(self, results):
        evaluator = Evaluator()
        evaluation = evaluator.evaluate(results)
        print(evaluation)
        