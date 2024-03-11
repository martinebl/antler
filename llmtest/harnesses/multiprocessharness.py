from multiprocessing import Pool
from tqdm import tqdm

from llmtest.harnesses import Harness
from llmtest.explorers.explorer import Explorer
from llmtest.generators.generator import Generator
from llmtest.transforms import Transform
from llmtest.probes import Probe
from llmtest.attempt import Attempt

class MultiProcessHarness(Harness):
    def __init__(self, probes: list[Probe], explorer: Explorer, generator_type: type[Generator], model: str, options: dict = {}, repetitions: int = 1, processes: int = None) -> None:
        self.generator_type = generator_type
        self.model = model
        self.probes = probes
        self.explorer = explorer
        self.options = options
        self.repetitions = repetitions
        self.processes = processes

    def runCleanProbes(self, pool):
        return pool.map(Harness.runAttempt, [(self, Attempt(Transform([]), probe)) for probe in self.probes] * self.repetitions)

    def collectAttempts(self) -> list[Attempt]:
        print("Running penetration tests")
        all_attempts: list[Attempt] = []

        with Pool(self.processes) as pool:

            print("Running tests with clean payloads...")
            empty_transform_attempts: list[Attempt] = self.runCleanProbes(pool)
            self.collapseSameAttempts(empty_transform_attempts)
            all_attempts.extend(empty_transform_attempts)

            non_clean_hit_probes = [attempt.getProbe() for attempt in empty_transform_attempts if attempt.getAttemptSuccessRate() < 1] * self.repetitions
            
            if len(non_clean_hit_probes) > 0:
                print("Running tests with transforms...")
                pbar = tqdm(self.explorer, leave=False)
                for transform in pbar:
                    transform_attempts: list[Attempt] = pool.map(Harness.runAttempt, [(self, Attempt(transform, probe)) for probe in non_clean_hit_probes])
                    self.collapseSameAttempts(transform_attempts)
                    
                    all_attempts.extend(transform_attempts)
                    transform_score = sum([attempt.getAttemptSuccessRate() for attempt in transform_attempts]) / len(transform_attempts)
                    self.explorer.seedScore(transform_score)
                    pbar.total = len(self.explorer)
                pbar.close()
        return all_attempts