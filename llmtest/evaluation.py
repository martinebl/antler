#!/usr/bin/env python3
from llmtest.result import Result
from colorama import Fore, Back, Style, init

class Evaluation:
    # Initialise colorama module. Should only be necessary on Windows
    init()

    def __init__(self, technique_results: list[Result], transform_results: list[Result], probe_results: list[Result]):
        self.technique_results = technique_results
        self.transform_results = transform_results
        self.probe_results = probe_results
  
    def prettyPrint(self) -> str:
        print("--- REPORT ---")

        print("Technique Attack Success Rate (ASR)")
        for res in self.technique_results:
            color = Fore.GREEN if res.getScore() >= 0.5 else Fore.YELLOW if res.getScore() > 0 else Fore.RED
            print(color + f" - {res.getName()}: {res.getScore()*100:.2f} % ASR ({res.getHitCount()}/{res.getAllCount()})")

        print(Style.RESET_ALL)
        print("Transform Attack Success Rate (ASR)")
        for res in self.transform_results:
            color = Fore.GREEN if res.getScore() >= 0.5 else Fore.YELLOW if res.getScore() > 0 else Fore.RED
            print(color + f" - {res.getName()}: {res.getScore()*100:.2f} % ASR ({res.getHitCount()}/{res.getAllCount()})")
        
        print(Style.RESET_ALL)
        print("Probe Attack Success Rate (ASR)")
        for res in self.probe_results:
            color = Fore.GREEN if res.getScore() >= 0.5 or res.getScore() < 0 else Fore.YELLOW if res.getScore() > 0 else Fore.RED if res.getScore() == 0 else Fore.GREEN
            print(color + f" - {res.getName()}: " +  (f"{res.getScore()*100:.2f} % ASR" if res.getScore() >= 0 else "CLEAN HIT") + f" ({res.getHitCount()}/{res.getAllCount()})")

        print(Style.RESET_ALL)
