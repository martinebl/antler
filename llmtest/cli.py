import argparse
import json
from llmtest.harnesses.linearharness import LinearHarness
from llmtest.harnesses.multiprocessharness import MultiProcessHarness
from llmtest import classfactory
from llmtest.explorers.exhaustivesearch import ExhaustiveSearch
from llmtest.generators.replicate import Replicate

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
        "-p",
        type=int,
        help="When present, activates Multiprocessing and spawns a pool of PROCESSES processes"
    )

    parser.add_argument(
        "--family",
        "-f",
        type=str,
        help="Specify which Generator family (class) to use for running the target LLM"
    )

    parser.add_argument(
        "--options",
        "-o",
        type=json.loads,
        help="Dictionary of model options in JSON format"
    )

    parser.add_argument(
        "--repetitions",
        "-r",
        type=int,
        help="The number of times each transformed and clean prompt, will be given to the target model for probes to run on them"
    )

    args = parser.parse_args()

    # Setting default values

    model = "meta/llama-2-70b-chat" # Default model
    # model = "orca-mini-3b-gguf2-q4_0" 

    probes_path = 'llmtest/probes'
    excluded_probes = ['__init__.py', 'probe.py']
    probes = [] # When enough probes are present, it might be too slow to load them all without needing them. Hence the empty start value

    # loads all exploits (always needed)
    exploits_path = 'llmtest/exploits'
    excluded_exploits = ['__init__.py', 'exploit.py']
    all_exploits = classfactory.instantiate_all_classes_from_folder(exploits_path, excluded_exploits)

    generator_class = Replicate # Defalt generator
    generator_path = 'llmtest/generators'
    exluded_generators = ['__init__.py', 'generator.py']

    options = {} # Default options

    repetitions = 1

    # Setting given arguments

    if args.model:
        model = args.model
    if args.probe:
        probes = classfactory.instantiate_classes_from_folder(probes_path, [args.probe.lower()+'.py'])
    if not args.probe:
        # Use all probes if no probe is specified
        probes = classfactory.instantiate_all_classes_from_folder(probes_path, excluded_probes)
    if args.family:
        generator_class = classfactory.get_classes_from_folder(generator_path, [args.family.lower()+'.py'])[0] # Should only return 1
    if args.options:
        options = args.options
    if args.repetitions:
        repetitions = args.repetitions

    if args.processes == 1:
        harness = LinearHarness(probes, ExhaustiveSearch(all_exploits), generator_class, model, options, repetitions)
    else:
        harness = MultiProcessHarness(probes, ExhaustiveSearch(all_exploits), generator_class, model, options, repetitions, args.processes)
        
    harness.run()
