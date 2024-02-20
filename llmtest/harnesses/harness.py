#!/usr/bin/env python3
from llmtest.generators.gpt4all import GPT4all
from llmtest.transforms import Transform
from llmtest.probes import Probe
from enum import Enum

class Answer(Enum):
    SUCCESS = 1
    FAILURE = 2

class Harness:
    """ This is the base harness class, that coordinates probes, transformers and generators """

    def __init__(self, model, probes: list[Probe], transforms: list[Transform]) -> None:
        
        self.generator = GPT4all(model, {})
        self.probes = probes
        self.transforms = transforms

    
    def run(self) -> None:
        print(self.probes)
        for i, probe in enumerate(self.probes):
            payload_answer = self.generator.generate(probe.getPayload())
            print("Probe #%i" % i)
            if probe.runDetectors(payload_answer): 
                print("Clean Payload: %s" % Answer.FAILURE)
            else:
                print("Clean Payload: %s" % Answer.SUCCESS)
                for j, transform in enumerate(self.transforms):
                    prompt = transform.applyExploits(probe.getPayload())
                    answer = self.generator.generate(prompt)
                    status = Answer.FAILURE if probe.runDetectors(answer) else Answer.SUCCESS
                    print("Transform #%i: %s" % (j, status))
        