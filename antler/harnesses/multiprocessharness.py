from multiprocessing import Pool
from tqdm import tqdm
from signal import signal, SIGINT, SIG_IGN

from antler.harnesses import Harness
from antler.explorers.explorer import Explorer
from antler.generators.generator import Generator
from antler.transforms import Transform
from antler.probes import Probe
from antler.attempt import Attempt

class MultiProcessHarness(Harness):
    def __init__(self, probes: list[Probe], explorer: Explorer, generator_type: type[Generator], api_key: str, model: str, options: dict = {}, repetitions: int = 1) -> None:
        super(MultiProcessHarness, self).__init__(probes, explorer, generator_type, api_key, model, options, repetitions)
        MAX_PROCESSES = 20
        self.processes = min(len(probes) * repetitions, MAX_PROCESSES )
    
    @staticmethod
    def initWorker():
        # Ignore keyboard interrupts, which means the pool will terminate normally before the program stops
        signal(SIGINT, SIG_IGN)

    def runCleanProbes(self, pool):
        return pool.map(Harness.runAttempt, [(self, Attempt(Transform([]), probe)) for probe in self.probes] * self.repetitions)

    def collectAttempts(self) -> list[Attempt]:
        all_attempts: list[Attempt] = []

        try:
            with Pool(self.processes, initializer=MultiProcessHarness.initWorker) as pool:

                print("Running tests with clean payloads...")
                empty_transform_attempts: list[Attempt] = self.runCleanProbes(pool)
                empty_transform_attempts = self.collapseSameAttempts(empty_transform_attempts)
                self.logTransformAttempts(empty_transform_attempts)
                all_attempts.extend(empty_transform_attempts)

                non_clean_hit_probes = [attempt.getProbe() for attempt in empty_transform_attempts if attempt.getAttemptSuccessRate() != None and attempt.getAttemptSuccessRate() < 1] * self.repetitions
                
                if len(non_clean_hit_probes) > 0:
                    print("Running tests with transforms...")
                    pbar = tqdm(self.explorer, leave=False, unit="tr")
                    for transform in pbar:
                        if self.explorer.hasMessage():
                            pbar.write(self.explorer.getMessage())
                            
                        transform_attempts: list[Attempt] = pool.map(Harness.runAttempt, [(self, Attempt(transform, probe)) for probe in non_clean_hit_probes])
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