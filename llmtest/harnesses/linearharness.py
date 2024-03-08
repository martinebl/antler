#!/usr/bin/env python3
from tqdm import tqdm

from llmtest.harnesses import Harness
from llmtest.transforms import Transform
from llmtest.attempt import Attempt

class LinearHarness(Harness):

    def runCleanProbes(self, probes):
        empty_attempts = [Attempt(Transform([]), probe) for probe in probes]
        return [Harness.runAttempt((self, attempt)) for attempt in empty_attempts]

    def collectAttempts(self) -> list[Attempt]:
        all_attempts: list[Attempt] = []
        
        # running clean attempts for each probe - only once, no repetitions
        empty_transform_attempts = self.runCleanProbes(self.probes)
        all_attempts.extend(empty_transform_attempts)
        
        non_clean_hit_probes = [attempt.getProbe() for attempt in empty_transform_attempts if attempt.getAttemptSuccessRate() < 1]

        if len(non_clean_hit_probes) > 0:
            print("Running tests with transforms...")
            for transform in tqdm(self.explorer):
                transform_attempts: list[Attempt] = [Harness.runAttempt((self, Attempt(transform, probe))) for probe in non_clean_hit_probes]
                transform_score = sum([attempt.getAttemptSuccessRate() for attempt in transform_attempts]) / len(transform_attempts)
                
                all_attempts.extend(transform_attempts)
                self.explorer.seedScore(transform_score)
        return all_attempts

    def run(self) -> None:
        print("Running penetration tests")
        
        self.evaluateAttempts(self.collectAttempts())

        # results: list[Result] = []
        # clean_hit_probes: list[Probe] = []
        # non_clean_hit_probes: list[Probe] = []
        
        # print("Running penetration tests")
        # for i, probe in enumerate(self.probes):
        #     print("Running test with clean payload for probe %i/%i" % (i+1, len(self.probes)))
        #     only_payload_answer = self.generator.generate(probe.getPayload())
        #     clean_hit_probes.append(probe) if probe.runDetectors(only_payload_answer) else non_clean_hit_probes.append(probe)
        
        # results.append(Result(Transform([]), len(clean_hit_probes), clean_hit_probes))

        # if len(non_clean_hit_probes) > 0:
        #     print("Running tests with transforms...")
        #     for transform in tqdm(self.explorer):
        #         hits = 0
        #         for probe in non_clean_hit_probes:
        #             prompt = transform.applyExploits(probe.getPayload())
        #             answer = self.generator.generate(prompt)
        #             if probe.runDetectors(answer): hits += 1
                    
        #         result = Result(transform, hits, non_clean_hit_probes)
        #         results.append(result)
        #         self.explorer.seedScore(result.score)
        
        # self.evaluateResults(results)
