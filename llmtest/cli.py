import argparse
import sys
from llmtest.harnesses import Harness
from llmtest import classfactory
from llmtest.transforms import Transform

def handle() -> None:
    parser = argparse.ArgumentParser(description="A simple pentesting tool for llm's, using prompt injection attacks")

    parser.add_argument(
        "--model",
        "-m",
        type=str,
        help="Specify the target LLM"
    )

    parser.add_argument(
        "--probe",
        "-p",
        type=str,
        help="Specify which probes to run on the target LLM"
    )

    parser.add_argument(
        "--default",
        "-d",
        action='store_true',
        help="Use the default probe and generator (CurseWord and orca-mini). Same behaviour happens when no arguments are provided"
    )

    args = parser.parse_args()

    probes_path = 'llmtest/probes'
    excluded_probes = ['__init__.py', 'probe.py']
    probes = []

    # loads all exploits
    exploits_path = 'llmtest/exploits'
    excluded_exploits = ['__init__.py', 'exploit.py']
    all_exploits = classfactory.instantiate_all_classes_from_folder(exploits_path, excluded_exploits)
    all_exploits_prioritized = []
    all_exploits_prioritized_reversed = []
    for i, exploit in enumerate(all_exploits):
        all_exploits_prioritized.append((i, exploit))
    for i, exploit in enumerate(all_exploits[::-1]):
        all_exploits_prioritized_reversed.append((i, exploit))

    if args.model:
        model = args.model
    if args.probe:
        probes = classfactory.instantiate_classes_from_folder(probes_path, [args.probe.lower()+'.py'])
    # Use the default value if either d is specified, or no arguments are given
    if args.default or len(sys.argv) == 1:
        model = "orca-mini-3b-gguf2-q4_0"
        probes = classfactory.instantiate_all_classes_from_folder(probes_path, excluded_probes)
    elif not args.probe:
        probes = classfactory.instantiate_all_classes_from_folder(probes_path, excluded_probes)
    
    harness = Harness(model, probes, [Transform(all_exploits_prioritized), Transform(all_exploits_prioritized_reversed)])
    harness.run()




