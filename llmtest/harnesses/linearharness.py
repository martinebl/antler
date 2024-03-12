#!/usr/bin/env python3
from tqdm import tqdm

from llmtest.harnesses import Harness
from llmtest.transforms import Transform
from llmtest.attempt import Attempt
from llmtest.probes.probe import Probe
from llmtest.generators.generator import Generator
from llmtest.explorers.explorer import Explorer

class LinearHarness(Harness):
    def __init__(self, probes: list[Probe], explorer: Explorer, generator_type: type[Generator], model: str, options: dict = {}, repetitions: int = 1):
        super(LinearHarness, self).__init__(probes, explorer, generator_type, model, options, repetitions)
        self.generator = generator_type(model, options)

    def runCleanProbes(self, probes):
        empty_attempts = [Attempt(Transform([]), probe) for probe in probes]
        return [Harness.runAttempt((self, attempt)) for attempt in empty_attempts]

    def runProbeForTransform(self, transform: Transform, probes: list[Probe]):
        return [Harness.runAttempt((self, Attempt(transform, probe))) for probe in probes * self.repetitions]

    def collectAttempts(self) -> list[Attempt]:
        print("Running penetration tests")
        all_attempts: list[Attempt] = []
        


        print("Running tests with clean payloads...")
        empty_transform_attempts = self.runCleanProbes(self.probes)
        self.collapseSameAttempts(empty_transform_attempts)
        all_attempts.extend(empty_transform_attempts)
        
        non_clean_hit_probes = [attempt.getProbe() for attempt in empty_transform_attempts if attempt.getAttemptSuccessRate() < 1] *self.repetitions

        if len(non_clean_hit_probes) > 0:
            print("Running tests with transforms...")
            pbar = tqdm(self.explorer, leave=False)
            for transform in pbar:
                if self.explorer.hasMessage():
                    pbar.write(self.explorer.getMessage())
                    
                transform_attempts: list[Attempt] = self.runProbeForTransform(transform, non_clean_hit_probes)
                self.collapseSameAttempts(transform_attempts)
                
                all_attempts.extend(transform_attempts)
                transform_score = sum([attempt.getAttemptSuccessRate() for attempt in transform_attempts]) / len(transform_attempts)
                self.explorer.seedScore(transform_score)
                pbar.total = len(self.explorer)
            pbar.close()
        return all_attempts
