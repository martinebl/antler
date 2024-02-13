import argparse
import sys
from llmtest.harnesses.harness import Harness

from llmtest import classfactory

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

    # Loads all probes
    probes_path = 'llmtest/probes'
    excluded = ['__init__.py', 'probe.py']

    # Use the default value if either d is specified, or no arguments are given
    probes = classfactory.instantiate_all_classes_from_folder(probes_path, excluded) if args.default or len(sys.argv) == 1 else classfactory.instantiate_classes_from_folder(probes_path, [args.probe+'.py'])
    harness = Harness(probes) if args.default or len(sys.argv) == 1 else Harness(probes, args.model)
    harness.run()




