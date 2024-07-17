import argparse
import json
from antler.harnesses.linearharness import LinearHarness
from antler.harnesses.multiprocessharness import MultiProcessHarness
from antler import classfactory
from antler.explorers.simulatedannealing import SimulatedAnnealing
from antler.explorers.greedyhillclimbexplorer import GreedyHillClimbExplorer
from antler.explorers.randomsearch import RandomSearch
from antler.generators.openai import OpenAI

def handle() -> None:
    parser = argparse.ArgumentParser(description="A simple pentesting tool for llm's, using prompt injection attacks")

    parser.add_argument(
        "-p",
        "--provider",
        type=str,
        help=" The target provider. Examples: openai, ollama, replicate"
    )

    parser.add_argument(
        "-m",
        "--model",
        type=str,
        help="The target model. Examples: gpt-3.5-turbo, llama2:7b"
    )

    parser.add_argument(
        "-e",
        "--explorer",
        type=str,
        help="The explorer strategy. Examples: simulatedannealing, randomsearch. Default depends on max queries"
    )

    parser.add_argument(
        "-M",
        "--max",
        type=int,
        help="The maximum amount of queries to run. Default: 100"
    )

    parser.add_argument(
        "-P",
        "--processes",
        type=int,
        help="The number of processes to run in parallel. Currently only has an effect when = 1, activating sequential querying"
    )

    parser.add_argument(
        "-r",
        "--repetitions",
        type=int,
        help="The repetitions of each probe query. Default: 3"
    )

    parser.add_argument(
        "--api_key",
        type=str,
        help="The api_key for the target provider. Optional for locally running LLMs."
    )

    parser.add_argument(
        "-o",
        "--options",
        type=json.loads,
        help="The options for the target model, in json format."
    )

    args = parser.parse_args()

    # Setting default values

    model = "gpt-3.5-turbo" 
    # model = "8f4118ba-60a8-4e6b-8574-e38a4067a4a3" # Default model Mixtral 8x7B Instruct
    # model = "orca-mini-3b-gguf2-q4_0" 

    excluded_probes = ['__init__.py', 'probe.py', 'cursewordfuck.py', 'illegaldrugs.py']
    probes = classfactory.instantiate_all_classes_from_folder('probes', excluded_probes)

    # loads all techniques (always needed)
    excluded_techniques = ['__init__.py', 'technique.py']
    #excluded_techniques = ['__init__.py', 'technique.py', 'threaten.py', 'taggingprefix.py', 'sympathy.py', 'stressingimportance.py', 'obfuscatingcode.py', 'nonnaturallanguage.py', 'markup.py', 'indirectrequest.py', 'ignoreinstructions.py', 'escapeuserprompt.py', 'encoding.py', 'defineability.py', 'convincemissingknowledge.py', 'addnoise.py', 'ignoretraining.py', 'repetition.py', 'altertext.py', 'refusalsuppression.py', 'describinganswerformat.py', 'limitingoutput.py', "roleplay.py"]
    all_techniques = classfactory.instantiate_all_classes_from_folder('techniques', excluded_techniques)

    api_key = None # Default api key is none

    generator_class = OpenAI # Defalt generator
    excluded_generators = ['__init__.py', 'generator.py']

    processes = 0

    options = {} # Default options

    repetitions = 3 # Default repetitions

    explorer_class = None # Default explorer set later

    max_queries = 100

    # Setting given arguments

    if args.model:
        model = args.model
    if args.api_key:
        api_key = args.api_key
    if args.provider:
        generator_class = classfactory.get_classes_from_folder('generators', [args.provider.lower()+'.py'])[0] # Should only return 1
    if args.options:
        options = args.options
    if args.repetitions:
        repetitions = args.repetitions
    if args.max:
        max_queries = args.max
    if args.explorer:
        explorer_class = classfactory.get_classes_from_folder('explorers', [args.explorer.lower()+".py"])[0]
    else: # If no explorer is given, choose one based on the amount of queries
        if max_queries <= 1000:
            explorer_class = RandomSearch
            print("Low amount of queries (<= 1000), using Random search")
        elif max_queries <= 3000:
            explorer_class = SimulatedAnnealing
            print("Medium amount of queries (> 1000), using Simulated annealing")
        else:
            explorer_class = GreedyHillClimbExplorer 
            print("High amount of queries (> 3000), using Greedy hill climb")
    if args.processes:
        processes = args.processes
    


    if generator_class.needsApiKey() and api_key == None:
        print("Error: The required API key was not present, neither in the environment nor as a parameter.")
        exit(1)

    if processes and processes == 1:
        harness = LinearHarness(probes, explorer_class, all_techniques, generator_class, api_key, model, options, repetitions, max_queries)
    else:
        harness = MultiProcessHarness(probes, explorer_class, all_techniques, generator_class, api_key, model, options, repetitions, max_queries)
        
    harness.run()
