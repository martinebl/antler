import argparse
import sys
from llmtest.harnesses import Harness

from llmtest import classfactory
from llmtest.transformers import Transformer

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

    exploits_path = 'llmtest/exploits'
    excluded_exploits = ['__init__.py', 'exploit.py']
    exploits = classfactory.instantiate_all_classes_from_folder(exploits_path, excluded_exploits)

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

    harness = Harness(model, probes, [Transformer(exploits)])
    harness.run()




