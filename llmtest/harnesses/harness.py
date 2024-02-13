#!/usr/bin/env python3
from llmtest.generators.gpt4all import GPT4all
from llmtest.probes.cursewordfuck import CurseWordFuck 
from llmtest.probes.robastore import RobAStore
from llmtest.transformers.transformer import Transformer
from llmtest.exploits.acceptingprefix import AcceptingPrefix
from llmtest.exploits.refusalsuppresion import RefusalSuppresion
from llmtest.probes import Probe

class Harness:
    """ This is the base harness class, that coordinates probes, transformers and generators """

    def __init__(self, model, probes: list[Probe], transformers: list[Transformer]) -> None:
        #if probe not in Harness.ProbeMapping.keys():
        #    raise Exception("Error: Given probe does not exist")
        
        self.generator = GPT4all(model, {})
        self.probes = probes
        self.transformers = transformers
        #self.transformers = [Transformer([AcceptingPrefix()])]

    
    def run(self) -> None:
        for probe in self.probes:
            for transformer in self.transformers:
                print(probe.getPayload())
                prompt = transformer.applyExploits(probe.getPayload())
                answer = self.generator.generate(prompt)
                print("Prompt: %s" % prompt)
                print("Answer: %s" % answer)
                print("Successful hack!") if probe.runDetectors(answer) else print("Failure, the model won")
        