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
  
    def getTitle(self)-> str: return "--------- REPORT ---------"
    def getTechniqueTitle(self)-> str: return "Technique Attack Success Rate (ASR)"
    def getProbeTitle(self)-> str: return "Probe Attack Success Rate (ASR)"
    def getTransformTitle(self)-> str: return "Transform Attack Success Rate (ASR)"
    def getTotalQueryStr(self)-> str: return f"Total queries: {self.total_reply_count}"
    def getTotalQueryErrorStr(self)-> str: return f"Total query error rate: {(self.error_reply_count/self.total_reply_count)*100} %"
    def getHitCountStr(self, res)-> str: return f"({res.getHitCount()}/{res.getAllCount()})"
    def getSingleResStr(self, res: Result)-> str: return f" - {res.getName()}: {res.getScore()*100:.2f} % ASR {self.getHitCountStr(res)}"
    def getScoreOrCleanStr(self, res: Result)-> str: return f"{res.getScore()*100:.2f} % ASR" if res.getScore() >= 0 else "CLEAN HIT"
    def getSingleProbeResStr(self, res: Result)-> str: return f" - {res.getName()}: {self.getScoreOrCleanStr(res)} {self.getHitCountStr(res)}"

    def prettyPrint(self) -> str:
        print(self.getTitle())
        print(self.getTotalQueryStr())
        print(self.getTotalQueryErrorStr())

        print(self.getTechniqueTitle())
        for res in self.technique_results:
            color = Fore.GREEN if res.getScore() >= 0.5 else Fore.YELLOW if res.getScore() > 0 else Fore.RED
            print(color + self.getSingleResStr(res)) 

        print(Style.RESET_ALL)
        print(self.getProbeTitle())
        for res in self.probe_results:
            color = Fore.GREEN if res.getScore() >= 0.5 or res.getScore() < 0 else Fore.YELLOW if res.getScore() > 0 else Fore.RED if res.getScore() == 0 else Fore.GREEN
            print(color + self.getSingleProbeResStr(res))

        print(Style.RESET_ALL)
        print(self.getTransformTitle())
        for res in self.transform_results:
            color = Fore.GREEN if res.getScore() >= 0.5 else Fore.YELLOW if res.getScore() > 0 else Fore.RED
            print(color + self.getSingleResStr(res))
        
        print(Style.RESET_ALL)

    def __str__(self) -> str:
        """
        Needed for the logging of the report. This is without colors
        """
        output = ""
        output += f"\n {self.getTitle()}"
        output += f"\n {self.getTotalQueryStr()}"
        output += f"\n {self.getTotalQueryErrorStr()}"

        output += f"\n {self.getTechniqueTitle()}"
        for res in self.technique_results:
            output += f"\n {self.getSingleResStr(res)}"

        output += f"\n {self.getProbeTitle()}"
        for res in self.probe_results:
            output += f"\n {self.getSingleProbeResStr(res)}"

        output += f"\n {self.getTransformTitle()}"
        for res in self.transform_results:
            output += f"\n {self.getSingleResStr(res)}"

        return output