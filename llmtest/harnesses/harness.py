#!/usr/bin/env python3
from llmtest.generators.gpt4all import GPT4all
from llmtest.probes.cursewordfuck import CurseWordFuck 
from llmtest.transformers.transformer import Transformer
from llmtest.exploits.acceptingprefix import AcceptingPrefix

class Harness:
    """ This is the base harness class, that coordinates probes, transformers and generators """

    def __init__(self) -> None:
        self.generator = GPT4all("orca-mini-3b-gguf2-q4_0", {})
        self.probes = [CurseWordFuck()]
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
        