import importlib

from llmtest.evaluation import Evaluation
from llmtest.attempt import Attempt
from llmtest.transforms import *
from llmtest.probes import *

class JSONParser:
    """ Takes a list of JSON objects and parses it as Attempts """
    @staticmethod
    def parse_json_as_attempts(data):
        attempts = []
        for entry in data:
            techniques = Evaluation.transformResultNameToArray(entry["transform"])
            instantiated_techniques = []
            if len(techniques) > 0 :
                instantiated_techniques = [getattr(importlib.import_module(f"llmtest.techniques.{technique.lower()}"), technique)() for technique in techniques]
            transform = Transform([ tech for tech in instantiated_techniques])
            probe = getattr(importlib.import_module(f"llmtest.probes.{entry['probe'].lower()}"), entry['probe'])()
            
            attempt = Attempt(transform, probe)
            [attempt.addResponseObject(reply) for reply in entry["replies"]]
            attempts.append(attempt)
        return attempts