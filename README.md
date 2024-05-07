# LLMTEST: A python tool for automatically generating prompt injections
The LLMTEST tool is an automatic tool for generating and evaluating prompt injection attacks against a target LLM.
It is designed to aid LLM red teamers test models and applications.

## Introduction
Built as part of a thesis project, the LLMTEST tool attempts to find a combination and permutation of prompt injection techniques identified in [PAPER REFERENCE] that can successfully jailbreak a given target model.
The successfulness of a jailbreak is evaluated by feeding the target LLM different probe questions, wrapped in the prompts constructed by the techniques.
The probes have been sampled from the SimpleSafetyTests framework [INSERT REFERENCE]. Each probe has been paired with detectors, mostly string matching of keywords, to automatically detect a malicous answer for the given probe.

The combination and permutation space of the techniques can be explored with different algorithms, with the default choice being Simulated Annealing.
Other options are Greedy Hill climb, and Random search.

## Installation
```bash
pip install LLMTEST
```

## Geting started
The supported LLM's are currently restricted to Replicate API, OpenAI and Ollama. 

#### Command line Options
* `--family, -f`            The target provider. Examples: openai, ollama, replicate
* `--model, -m`             The target model. Examples: gpt-3.5-turbo, 'llama2:7b'
* `--explorer, -e`          The explorer strategy. Examples: simulatedannealing, randomsearch. Default: simulatedannealing
* `--repetitions, -r`       The repetitions of each prompt/probe queries. Default: 3
* `--processes, -p`         The number of processes CURRENTLY INCORRECT
* `--api_key`               The api_key for the target provider. Optional for locally running LLMs.
* `--options, -o`           The options for the target provider, in json format. 

Example of run parameters:
```bash
LLMTEST -f openai -m gpt-3.5-turbo --api_key SECRET_TOKEN
```



Authored by M. Borup-Larsen and C. Christoffersen