import importlib

from antler.evaluation import Evaluation
from antler.attempt import Attempt
from antler.transforms import *
from antler.probes import *

class JSONParser:
    """ Takes a list of JSON objects and parses it as Attempts """
    @staticmethod
    def parse_json_as_attempts(data):
        attempts = []
        for entry in data:
            transform = JSONParser.transform_name_to_transform(entry["transform"])

            # techniques = Evaluation.transformResultNameToArray(entry["transform"])
            # instantiated_techniques = []
            # if len(techniques) > 0 :
            #     instantiated_techniques = [getattr(importlib.import_module(f"antler.techniques.{technique.lower()}"), technique)() for technique in techniques]
            # transform = Transform([ tech for tech in instantiated_techniques])

            probe = getattr(importlib.import_module(f"antler.probes.{entry['probe'].lower()}"), entry['probe'])()
            
            attempt = Attempt(transform, probe)
            [attempt.addResponseObject(reply) for reply in entry["replies"]]
            attempts.append(attempt)
        return attempts
    
    @staticmethod
    def transform_name_to_transform(name):
        techniques = Evaluation.transformResultNameToArray(name)
        instantiated_techniques = []
        if len(techniques) > 0 :
            instantiated_techniques = [getattr(importlib.import_module(f"antler.techniques.{technique.lower()}"), technique)() for technique in techniques]
        return Transform([ tech for tech in instantiated_techniques])