#!/usr/bin/env python3
from tqdm import tqdm

from antler.harnesses import Harness
from antler.transforms import Transform
from antler.attempt import Attempt
from antler.probes.probe import Probe
from antler.generators.generator import Generator
from antler.explorers.explorer import Explorer

class LinearHarness(Harness):
    def __init__(self, probes: list[Probe], explorer: Explorer, generator_type: type[Generator], api_key: str, model: str, options: dict = {}, repetitions: int = 1, max_queries: int = 10):
        super(LinearHarness, self).__init__(probes, explorer, generator_type, api_key, model, options, repetitions, max_queries)
        self.generator = generator_type(model, api_key, options)

    def runCleanProbes(self, probes):
        empty_attempts = [Attempt(Transform([]), probe) for probe in (probes * self.repetitions)] 
        return [Harness.runAttempt((self, attempt)) for attempt in empty_attempts]

    def runProbesForTransform(self, transform: Transform, probes: list[Probe]):
        return [Harness.runAttempt((self, Attempt(transform, probe))) for probe in (probes * self.repetitions)]

    def collectAttempts(self) -> list[Attempt]:
        all_attempts: list[Attempt] = []
        try:
            print("Running tests with clean payloads...")
            empty_transform_attempts = self.runCleanProbes(self.probes)
            empty_transform_attempts = self.collapseSameAttempts(empty_transform_attempts)
            self.logTransformAttempts(empty_transform_attempts)
            all_attempts.extend(empty_transform_attempts)
            
            non_clean_hit_probes = [attempt.getProbe() for attempt in empty_transform_attempts if attempt.getAttemptSuccessRate() != None and attempt.getAttemptSuccessRate() < 1]
            if len(non_clean_hit_probes) > 0:
                print("Running tests with transforms...")
                pbar = tqdm(self.explorer, leave=False, unit="tr")
                for transform in pbar:
                    if self.explorer.hasMessage():
                        pbar.write(self.explorer.getMessage())

                    transform_attempts: list[Attempt] = self.runProbesForTransform(transform, non_clean_hit_probes)
                    transform_attempts = self.collapseSameAttempts(transform_attempts)
                    self.logTransformAttempts(transform_attempts)
                    
                    all_attempts.extend(transform_attempts)
                    non_failed_attempts = [ attempt for attempt in transform_attempts if attempt.getAttemptSuccessRate() != None]
                    transform_score = sum([attempt.getAttemptSuccessRate() for attempt in non_failed_attempts ]) / len(non_failed_attempts) if len(non_failed_attempts) != 0 else 0
                    self.explorer.seedScore(transform_score)
                    pbar.total = len(self.explorer)
                    if self.explorer.hasMessage():
                        pbar.write(self.explorer.getMessage())
                pbar.close()
        except KeyboardInterrupt:
            print("User interrupted, terminating early")
        return all_attempts
