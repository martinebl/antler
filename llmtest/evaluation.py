#!/usr/bin/env python3
from llmtest.result import Result

class Evaluation:
    def __init__(self, technique_results: list[Result], transform_results: list[Result], probe_results: list[Result]):
        self.technique_results = technique_results
        self.transform_results = transform_results
        self.probe_results = probe_results
  
    def __str__(self) -> str:
        output = "\n--- REPORT ---"

        output += "\n Technique Attack Success Rate (ASR)"
        for res in self.technique_results:
            output += f"\n - {res.getName()}: {res.getScore()*100} % ASR"

        output += "\n Transform Attack Success Rate (ASR)"
        for res in self.transform_results:
            output += f"\n - {res.getName()}: {res.getScore()*100} % ASR"
        
        output += "\n Probe Attack Success Rate (ASR)"
        for res in self.probe_results:
            output += f"\n - {res.getName()}: "
            output += f"{res.getScore()*100} % ASR" if res.getScore() > 0 else "CLEAN HIT"

        return output
