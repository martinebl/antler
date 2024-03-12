#!/usr/bin/env python3
from tqdm import tqdm

from llmtest.harnesses import Harness
from llmtest.transforms import Transform
from llmtest.attempt import Attempt
from llmtest.probes.probe import Probe

class LinearHarness(Harness):

    def runCleanProbes(self, probes):
        empty_attempts = [Attempt(Transform([]), probe) for probe in (probes * self.repetitions)] 
        return [Harness.runAttempt((self, attempt)) for attempt in empty_attempts]

    def runProbesForTransform(self, transform: Transform, probes: list[Probe]):
        return [Harness.runAttempt((self, Attempt(transform, probe))) for probe in (probes * self.repetitions)]

    def collectAttempts(self) -> list[Attempt]:
        print("Running penetration tests")
        all_attempts: list[Attempt] = []

        print("Running tests with clean payloads...")
        empty_transform_attempts = self.runCleanProbes(self.probes)
        empty_transform_attempts = self.collapseSameAttempts(empty_transform_attempts)
        all_attempts.extend(empty_transform_attempts)
        
        non_clean_hit_probes = [attempt.getProbe() for attempt in empty_transform_attempts if attempt.getAttemptSuccessRate() != None and attempt.getAttemptSuccessRate() < 1]
        if len(non_clean_hit_probes) > 0:
            print("Running tests with transforms...")
            pbar = tqdm(self.explorer, leave=False)
            for transform in pbar:
                if self.explorer.hasMessage():
                    pbar.write(self.explorer.getMessage())

                transform_attempts: list[Attempt] = self.runProbesForTransform(transform, non_clean_hit_probes)
                transform_attempts = self.collapseSameAttempts(transform_attempts)
                
                all_attempts.extend(transform_attempts)
                non_failed_attempts = [ attempt for attempt in transform_attempts if attempt.getAttemptSuccessRate() != None]
                transform_score = sum([attempt.getAttemptSuccessRate() for attempt in non_failed_attempts ]) / len(non_failed_attempts) if len(non_failed_attempts) != 0 else 0
                self.explorer.seedScore(transform_score)
                pbar.total = len(self.explorer)
            pbar.close()
        return all_attempts
