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
        print("Running penetration tests")
        all_attempts: list[Attempt] = []
        
        print("Running tests with clean payloads...")
        # running clean attempts for each probe - only once, no repetitions
        empty_transform_attempts = self.runCleanProbes(self.probes)
        all_attempts.extend(empty_transform_attempts)
        
        non_clean_hit_probes = [attempt.getProbe() for attempt in empty_transform_attempts if attempt.getAttemptSuccessRate() < 1]

        if len(non_clean_hit_probes) > 0:
            print("Running tests with transforms...")
            pbar = tqdm(self.explorer, leave=False)
            for transform in pbar:
                transform_attempts: list[Attempt] = [Harness.runAttempt((self, Attempt(transform, probe))) for probe in non_clean_hit_probes]
                transform_score = sum([attempt.getAttemptSuccessRate() for attempt in transform_attempts]) / len(transform_attempts)
                
                all_attempts.extend(transform_attempts)
                self.explorer.seedScore(transform_score)
                pbar.total = len(self.explorer)
            pbar.close()
        return all_attempts

    def run(self) -> None:        
        self.evaluateAttempts(self.collectAttempts())
