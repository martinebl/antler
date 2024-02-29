from multiprocessing import Pool

from llmtest.harnesses import Harness
from llmtest.explorers.explorer import Explorer
from llmtest.generators.generator import Generator
from llmtest.transforms import Transform
from llmtest.probes import Probe
from llmtest.result import Result

class MultiProcessHarness(Harness):
    def __init__(self, probes: list[Probe], explorer: Explorer, generator_type: type[Generator], model: str, options: dict = {}, repetitions: int = 1, processes: int = None) -> None:
        self.generator_type = generator_type
        self.model = model
        self.probes = probes
        self.explorer = explorer
        self.options = options
        self.repetitions = repetitions
        self.processes = processes
    
    @staticmethod
    def runCleanProbe(args: tuple[Harness, Probe]):
        harness, probe = args
        generator = harness.generator_type(harness.model, harness.options)
        answer = generator.generate(probe.getPayload())
        return (probe, probe.runDetectors(answer))
    
    @staticmethod
    def runTransformedProbe(args: tuple[Harness, Probe, Transform]):
        harness, probe, transform = args
        generator = harness.generator_type(harness.model, harness.options)
        answer = generator.generate(transform.applyExploits(probe.getPayload()))
        return (probe, probe.runDetectors(answer))

    def run(self) -> None:
        results: list[Result] = []
        clean_hit_probes: list[Probe] = []
        non_clean_hit_probes: list[Probe] = []

        with Pool(self.processes) as pool:
            print("Running penetration tests ...")

            # Run probes in parallel
            print("Testing clean payloads")
            pool_results = pool.map(MultiProcessHarness.runCleanProbe, [(self, probe) for probe in self.probes] * self.repetitions)
            for probe, hit in pool_results:
                if hit: clean_hit_probes.append(probe) 
            
            # Get each probe that did not have a single clean hit, exactly self.repetitions times in the list
            non_clean_hit_probes = [probe for probe in self.probes if probe not in clean_hit_probes] * self.repetitions
            
            results.append(Result(Transform([]), len(clean_hit_probes), clean_hit_probes))

            if len(non_clean_hit_probes) > 0:
                for i, transform in enumerate(self.explorer):
                    print("\tTransform %i/%i" % (i+1, len(self.explorer)))
                    hits = 0
                    pool_results = pool.map(MultiProcessHarness.runTransformedProbe, [(self, probe, transform) for probe in non_clean_hit_probes])

                    for probe, hit in pool_results:
                        if hit: 
                            hits += 1
                        
                    result = Result(transform, hits, non_clean_hit_probes)
                    results.append(result)
                    self.explorer.seedScore(result.score)
        
        self.evaluateResults(results)