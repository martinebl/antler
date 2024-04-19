import argparse
import json
from llmtest.harnesses.linearharness import LinearHarness
from llmtest.harnesses.multiprocessharness import MultiProcessHarness
from llmtest import classfactory
from llmtest.explorers.bestinclassexplorer import BestInClassExplorer
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
        help="Specify which probe to run on the target LLM"
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
        help="Specify which Generator family (class) to use for running the target LLM. Examples: 'openai' and 'ollama'"
    )

    parser.add_argument(
        "--api_key",
        type=str,
        help="Specify the API key, for the given generator family, if needed"
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

    parser.add_argument(
        "--explorer",
        "-e",
        type=str,
        help="The name of the explorer class/strategy used to search the space of all transforms"
    )

    args = parser.parse_args()

    # Setting default values

    model = "meta/llama-2-70b-chat" 
    # model = "8f4118ba-60a8-4e6b-8574-e38a4067a4a3" # Default model Mixtral 8x7B Instruct
    # model = "orca-mini-3b-gguf2-q4_0" 

    probes_path = 'llmtest/probes'
    excluded_probes = ['__init__.py', 'probe.py', 'cursewordfuck.py', 'illegaldrugs.py']
    probes = [] # When enough probes are present, it might be too slow to load them all without needing them. Hence the empty start value

    # loads all techniques (always needed)
    techniques_path = 'llmtest/techniques'
    #excluded_techniques = ['__init__.py', 'technique.py']
    excluded_techniques = ['__init__.py', 'technique.py', 'threaten.py', 'taggingprefix.py', 'sympathy.py', 'stressingimportance.py', 'obfuscatingcode.py', 'nonnaturallanguage.py', 'markup.py', 'indirectrequest.py', 'ignoreinstructions.py', 'escapeuserprompt.py', 'encoding.py', 'defineability.py', 'convincemissingknowledge.py', 'addnoise.py', 'ignoretraining.py', 'repetition.py', 'altertext.py', 'refusalsuppression.py', 'describinganswerformat.py', 'limitingoutput.py']
    all_techniques = classfactory.instantiate_all_classes_from_folder(techniques_path, excluded_techniques)

    api_key = None # Default api key is none

    generator_class = Replicate # Defalt generator
    generator_path = 'llmtest/generators'
    excluded_generators = ['__init__.py', 'generator.py']

    processes = 0

    options = {} # Default options

    repetitions = 3 # Default repetitions

    explorer_class = BestInClassExplorer # Default explorer
    explorer_path = 'llmtest/explorers'

    # Setting given arguments

    if args.model:
        model = args.model
    if args.probe:
        probes = classfactory.instantiate_classes_from_folder(probes_path, [args.probe.lower()+'.py'])
    if not args.probe:
        # Use all probes if no probe is specified
        probes = classfactory.instantiate_all_classes_from_folder(probes_path, excluded_probes)
    if args.api_key:
        api_key = args.api_key
    if args.family:
        generator_class = classfactory.get_classes_from_folder(generator_path, [args.family.lower()+'.py'])[0] # Should only return 1
        if generator_class.needsApiKey() and api_key == None:
            print("Error: The needed API key was not present, neither in the environment nor as a parameter.")
            exit(1)
    if args.options:
        options = args.options
    if args.repetitions:
        repetitions = args.repetitions
    if args.explorer:
        explorer_class = classfactory.get_classes_from_folder(explorer_path, [args.explorer.lower()+".py"])[0]
    if args.processes:
        processes = args.processes

    if processes and processes == 1:
        harness = LinearHarness(probes, explorer_class(all_techniques), generator_class, api_key, model, options, repetitions)
    else:
        harness = MultiProcessHarness(probes, explorer_class(all_techniques), generator_class, api_key, model, options, repetitions)
        
    harness.run()
