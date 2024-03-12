#!/usr/bin/env python3
from llmtest.result import Result
from colorama import Fore, Back, Style, init

class Evaluation:
    # Initialise colorama module. Should only be necessary on Windows
    init()

    def __init__(self, technique_results: list[Result], transform_results: list[Result], probe_results: list[Result], error_reply_count: int, total_reply_count: int):
        self.technique_results = technique_results
        self.transform_results = transform_results
        self.probe_results = probe_results
        self.error_reply_count = error_reply_count
        self.total_reply_count = total_reply_count
  
    def prettyPrint(self) -> str:
        print("\n--------- REPORT ---------")
        print(f"Total queries: {self.total_reply_count}")
        print(f"Total query error rate: {(self.error_reply_count/self.total_reply_count)*100} %")

        print("Technique Attack Success Rate (ASR)")
        for res in self.technique_results:
            color = Fore.GREEN if res.getScore() >= 0.5 else Fore.YELLOW if res.getScore() > 0 else Fore.RED
            print(color + f" - {res.getName()}: {res.getScore()*100:.2f} % ASR ({res.getHitCount()}/{res.getAllCount()})")

        print(Style.RESET_ALL)
        print("Probe Attack Success Rate (ASR)")
        for res in self.probe_results:
            color = Fore.GREEN if res.getScore() >= 0.5 or res.getScore() < 0 else Fore.YELLOW if res.getScore() > 0 else Fore.RED if res.getScore() == 0 else Fore.GREEN
            print(color + f" - {res.getName()}: " +  (f"{res.getScore()*100:.2f} % ASR" if res.getScore() >= 0 else "CLEAN HIT") + f" ({res.getHitCount()}/{res.getAllCount()})")

        print(Style.RESET_ALL)
        print("Transform Attack Success Rate (ASR)")
        for res in self.transform_results:
            color = Fore.GREEN if res.getScore() >= 0.5 else Fore.YELLOW if res.getScore() > 0 else Fore.RED
            print(color + f" - {res.getName()}: {res.getScore()*100:.2f} % ASR ({res.getHitCount()}/{res.getAllCount()})")
        
        print(Style.RESET_ALL)

    def __str__(self) -> str:
        """
        Needed for the logging of the report. This is without colors
        """
        output = "\n--------- REPORT ---------"

        output += "\n Technique Attack Success Rate (ASR)"
        for res in self.technique_results:
            output += f"\n - {res.getName()}: {res.getScore()*100:.2f} % ASR ({res.getHitCount()}/{res.getAllCount()})"

        output += "\n Probe Attack Success Rate (ASR)"
        for res in self.probe_results:
            output += f"\n - {res.getName()}: "
            output += (f"{res.getScore()*100:.2f} % ASR" if res.getScore() > 0 else "CLEAN HIT")  + f" ({res.getHitCount()}/{res.getAllCount()})"

        output += "\n Transform Attack Success Rate (ASR)"
        for res in self.transform_results:
            output += f"\n - {res.getName()}: {res.getScore()*100:.2f} % ASR ({res.getHitCount()}/{res.getAllCount()})"

        return output
