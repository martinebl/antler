import argparse
import sys
from llmtest.harnesses.linearharness import LinearHarness
from llmtest.harnesses.multiprocessharness import MultiProcessHarness
from llmtest import classfactory
from llmtest.explorers.exhaustivesearch import ExhaustiveSearch
from llmtest.generators.gpt4all import GPT4all

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

    parser.add_argument(
        "--processes",
        "-c",
        type=int,
        help="When present, activates Multiprocessing and spawns a pool of PROCESSES processes"
    )

    parser.add_argument(
        "--family",
        "-f",
        type=str,
        help="Specify which Generator family (class) to use for running the target LLM"
    )

    args = parser.parse_args()

    probes_path = 'llmtest/probes'
    excluded_probes = ['__init__.py', 'probe.py']
    probes = []

    # loads all exploits
    exploits_path = 'llmtest/exploits'
    excluded_exploits = ['__init__.py', 'exploit.py']
    all_exploits = classfactory.instantiate_all_classes_from_folder(exploits_path, excluded_exploits)

    generator_class = GPT4all # Defalt generator
    generator_path = 'llmtest/generators'
    exluded_generators = ['__init__.py', 'generator.py']

    harness_class = LinearHarness # Default harness

    options = {} # Default options

    if args.model:
        model = args.model
    if args.probe:
        probes = classfactory.instantiate_classes_from_folder(probes_path, [args.probe.lower()+'.py'])
    if args.family:
        generator_class = classfactory.get_classes_from_folder(generator_path, [args.family.lower()+'.py'])[0] # Should only return 1
    if args.processes:
        harness_class = MultiProcessHarness

    # Use the default value if either d is specified, or no arguments are given
    if args.default or len(sys.argv) == 1:
        model = "orca-mini-3b-gguf2-q4_0"
        # model = "meta/llama-2-70b-chat"
        probes = classfactory.instantiate_all_classes_from_folder(probes_path, excluded_probes)
    elif not args.probe:
        probes = classfactory.instantiate_all_classes_from_folder(probes_path, excluded_probes)
    
    harness = harness_class(probes, ExhaustiveSearch(all_exploits), generator_class, model, options)
    harness.run()
