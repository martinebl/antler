# Antler: A python tool for automatically generating jailbreak prompts

*ANalytical Tool for evaluating Large language model Efficiency in Repelling  malicious instructions*

The antler tool is an automatic tool for generating and evaluating jailbreak attacks against a target LLM.
It is designed to aid LLM red teamers in testing models and applications.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Downloads](https://static.pepy.tech/badge/antler)](https://pepy.tech/project/antler)
[![Downloads](https://static.pepy.tech/badge/antler/month)](https://pepy.tech/project/antler)

## Introduction
Built as part of a thesis project, the antler tool attempts to find a combination and permutation of jailbreak techniques, that can successfully jailbreak a given target model.
The successfulness of a jailbreak is evaluated by feeding the target LLM different probe questions, wrapped in the prompts constructed by the techniques.
The probes have been sampled from the [SimpleSafetyTests](https://github.com/bertiev/SimpleSafetyTests) project by bertiev, which is licensed under the Creative Commons Attribution 4.0 International License. 
Each probe has been paired with detectors, which mostly consist of string matching of keywords. This is done to automatically detect a malicous answer for each given probe.

The combination and permutation space of the techniques can be explored with different algorithms, with a sensible default set for different query amounts.
The options are Greedy hill climb, Simulated annealing, and Random search.

## Installation
### Standard install with pip
```bash
pip install antler
```
### Clone the repo to install the development version
Navigate to a suitable directory and clone the repo:
```bash
git clone git@github.com:martinebl/antler.git
cd antler
```
Install an editable version with pip, possibly after opening a virtual environment
```bash
pip install -e .
```
## Geting started
The currently supported LLM providers are: OpenAI, Replicate, OctoAI and Ollama. 

**OpenAI**

When using the openai provider, an API key is needed. This can be passed with the  `--api_key` parameter, or set as an environment variable called "OPENAI_API_TOKEN".
When specifying model name, simply use the name of the model e.g. "gpt-3.5-turbo".

<!-- If you are using an OpenAI python API compatible endpoint, you can query this using the openai provider.
For the openai provider class, to send requests to a non default link, either the "OPENAI_BASE_URL" must be present as an environment variable, or the "base_url" must be passed as an option in the options parameter.
This link should be of the form "host:port" e.g. "localhost:11434". -->
**Replicate**

When using the replicate provider, an API key is needed. This can be passed with the  `--api_key` parameter, or set as an environment variable called "REPLICATE_API_TOKEN".
When specifying model name, it is required to include the provider e.g. "mistralai/mixtral-8x7b-instruct-v0.1".

**OctoAI**

When using the octoai provider, an API key is needed. This can be passed with the `--api_key` parameter, or set as an environment variable called "OCTOAI_TOKEN".
When specifying model name, simply use the name of the model e.g. "meta-llama-3.1-8b-instruct".


**Ollama**

When using the ollama provider no API key is needed. It is required to have an accessible ollama instance running. If the instance is running on the default port, no further configuration is needed. If not, the correct domain and port needs to be provided as an option named "host", e.g. `--options '{"host":"127.0.0.1:11434"}'`.
Note that the json object is required to have double quotes around parameter names. 
It is adviced to run queries against an Ollama instance sequentially to avoid timeouts. This is done by specifying `--processes 1`.

#### Command line Options
* `--provider, -p`          The target provider. Examples: openai, ollama, replicate
* `--model, -m`             The target model. Examples: gpt-3.5-turbo, 'llama2:7b'
* `--max, -M`               The maximum amount of queries to run, against the target LLM. Default: 100. 
* `--explorer, -e`          The explorer strategy. Possible values: simulatedannealing, randomsearch and greedyhillclimb. Default depends on max queries.
* `--repetitions, -r`       The repetitions of each prompt/probe queries. Default: 3
* `--processes, -P`         The number of processes to run in parallel. Currently only has an effect when = 1, activating sequential querying.
* `--api_key`               The api_key for the target provider. Optional for locally running LLMs.
* `--options, -o`           The options for the target provider, in json format. 

Examples of run parameters:
```bash
antler -p openai -m gpt-3.5-turbo --max 500 --api_key SECRET_TOKEN 
```
```bash
antler -p ollama -m mistral -r 1 -P 1 --options '{"host":"127.0.0.1:11434"}'
```

#### Sample run and results
![](https://raw.githubusercontent.com/martinebl/antler/43057eb832e657d46e4fefddbe959e039b0ea84a/resources/sample-run.gif)

The gif above shows a sample run at 2x speed.
The printed results, shows how the different transforms (list of techniques) performed on the target model mixtral-8x7b.
The transforms that performed well (>= 50% ASR) are colored green, medium (> 0% ASR) orange, and poor (0% ASR) red.
The average ASR's of each technique and probe are also displayed.

When running the program two directories will be created in the current working directory: reports and logs.
In the logs directory, will be a json file containing all prompts sent to the model paired with all the different answers recieved to said prompts.
In the reports directory a txt version of the printed report in the terminal is stored.

Authored by M. Borup-Larsen and C. Christoffersen