#!/usr/bin/env python3
from tqdm import tqdm

from llmtest.harnesses import Harness
from llmtest.probes import Probe
from llmtest.result import Result
from llmtest.transforms import Transform

class LinearHarness(Harness):

    def run(self) -> None:
        results: list[Result] = []
        clean_hit_probes: list[Probe] = []
        non_clean_hit_probes: list[Probe] = []
        
        print("Running penetration tests")
        for i, probe in enumerate(self.probes):
            print("Running test with clean payload for probe %i/%i" % (i+1, len(self.probes)))
            only_payload_answer = self.generator.generate(probe.getPayload())
            clean_hit_probes.append(probe) if probe.runDetectors(only_payload_answer) else non_clean_hit_probes.append(probe)
        
        results.append(Result(Transform([]), len(clean_hit_probes), clean_hit_probes))

        if len(non_clean_hit_probes) > 0:
            print("Running tests with transforms...")
            for transform in tqdm(self.explorer):
                hits = 0
                for probe in non_clean_hit_probes:
                    prompt = transform.applyExploits(probe.getPayload())
                    answer = self.generator.generate(prompt)
                    if probe.runDetectors(answer): hits += 1
                    
                result = Result(transform, hits, non_clean_hit_probes)
                results.append(result)
                self.explorer.seedScore(result.score)
        
        self.evaluateResults(results)
