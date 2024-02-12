import argparse
import sys
from llmtest.harnesses.harness import Harness

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
        help="Use the default probe and generator (CurseWord and orca-mini)"
    )

    args = parser.parse_args()

    # Use the default value if either d is specified, or no arguments are given
    harness = Harness() if args.default or len(sys.argv) == 1 else Harness(args.model, args.probe)
    harness.run()




