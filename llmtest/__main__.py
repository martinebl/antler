from llmtest.harnesses.harness import Harness
from llmtest import runall
from pathlib import Path

""""entry point script"""

def main():
    probes = runall.instantiate_classes_from_folder(Path.cwd() / 'llmtest' / 'probes')
    print(Path.cwd())
    harness = Harness(probes)
    harness.run()

if __name__ == "__main__":
    main()