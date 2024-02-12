#!/usr/bin/env python3
from llmtest.generators.gpt4all import GPT4all
from llmtest.probes.cursewordfuck import CurseWordFuck 
from llmtest.transformers.transformer import Transformer
from llmtest.exploits.acceptingprefix import AcceptingPrefix

class Harness:
    """ This is the base harness class, that coordinates probes, transformers and generators """
    ProbeMapping = {
        'CurseWordFuck': CurseWordFuck,
    }

    def __init__(self, model="orca-mini-3b-gguf2-q4_0", probe="CurseWordFuck") -> None:
        if probe not in Harness.ProbeMapping.keys():
            raise Exception("Error: Given probe does not exist")
        
        self.generator = GPT4all(model, {})
        self.probes = [self.ProbeMapping[probe]()]
        self.transformers = [Transformer([AcceptingPrefix()])]

    
    def run(self) -> None:
        for probe in self.probes:
            for transformer in self.transformers:
                print(probe.getPayload())
                prompt = transformer.applyExploits(probe.getPayload())
                answer = self.generator.generate(prompt)
                print("Prompt: %s" % prompt)
                print("Answer: %s" % answer)
                print("Successful hack!") if probe.runDetectors(answer) else print("Failure, the model won")
        