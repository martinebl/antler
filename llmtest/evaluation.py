#!/usr/bin/env python3
from llmtest.result import Result
from colorama import Fore, Back, Style, init

class Evaluation:
    # Initialise colorama module. Should only be necessary on Windows
    init()

    def __init__(self, technique_results: list[Result], transform_results: list[Result], probe_results: list[Result], error_reply_count: int, total_reply_count: int):
        self.technique_results = technique_results
        self.transform_results = self.insertNoneResulstsBetweenCombinations(transform_results)
        self.probe_results = probe_results
        self.error_reply_count = error_reply_count
        self.total_reply_count = total_reply_count
        self.elapsedTime = ""

    def setElapsedTime(self, time_str: str) -> None:
        self.elapsedTime = time_str
  

    @staticmethod
    def transformResultNameToArray(result_name: str) -> list:
        return result_name.replace('(','').replace(')','').replace(' ', '').split(',')[:-1]
    
    def getTitle(self)-> str: return "--------- REPORT ---------"
    def getElapsedTime(self)-> str: return f"Elapsed time: {self.elapsedTime}"
    def getTechniqueTitle(self)-> str: return "Technique Attack Success Rate (ASR)"
    def getProbeTitle(self)-> str: return "Probe Attack Success Rate (ASR)"
    def getTransformTitle(self)-> str: return "Transform Attack Success Rate (ASR)"
    def getTotalQueryStr(self)-> str: return f"Total queries: {self.total_reply_count}"
    def getTotalQueryErrorStr(self)-> str: return f"Total query error rate: {(self.error_reply_count/self.total_reply_count)*100:.2f} %"
    def getHitCountStr(self, res)-> str: return f"({res.getHitCount()}/{res.getAllCount()})"
    def getSingleResStr(self, res: Result)-> str: return f" - {res.getName()}: {res.getScore()*100:.2f} % ASR {self.getHitCountStr(res)}" if res else ""
    def getScoreOrCleanStr(self, res: Result)-> str: return f"{res.getScore()*100:.2f} % ASR" if res.getScore() >= 0 else "CLEAN HIT"
    def getSingleProbeResStr(self, res: Result)-> str: return f" - {res.getName()}: {self.getScoreOrCleanStr(res)} {self.getHitCountStr(res)}"

    def insertNoneResulstsBetweenCombinations(self, transform_results):
        for i, res in enumerate(transform_results):
            if not res: continue 
            if i >= len(transform_results)-1: break
            technique_name_array = Evaluation.transformResultNameToArray(transform_results[i].getName())
            technique_name_array_next = Evaluation.transformResultNameToArray(transform_results[i+1].getName())
            technique_name_array = sorted(technique_name_array)
            technique_name_array_next = sorted(technique_name_array_next)

            if technique_name_array != technique_name_array_next:
                transform_results.insert(i+1, None)
        
        return transform_results

    def prettyPrint(self) -> str:
        print(self.getTitle())
        print(self.getElapsedTime())
        print(self.getTotalQueryStr())
        print((Fore.GREEN if self.error_reply_count == 0 else Fore.RED) + self.getTotalQueryErrorStr())

        print(Style.RESET_ALL)
        print(self.getTransformTitle())
        for res in self.transform_results:
            color = Fore.WHITE if not res else Fore.GREEN if res.getScore() >= 0.5 else Fore.YELLOW if res.getScore() > 0 else Fore.RED
            #color = Fore.GREEN if res.getScore() >= 0.5 else Fore.YELLOW if res.getScore() > 0 else Fore.RED
            print(color + self.getSingleResStr(res))

        print(Style.RESET_ALL)
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

    def __str__(self) -> str:
        """
        Needed for the logging of the report. This is without colors
        """
        output = ""
        output += f"\n {self.getTitle()}"
        output += f"\n {self.getElapsedTime()}"
        output += f"\n {self.getTotalQueryStr()}"
        output += f"\n {self.getTotalQueryErrorStr()}"
        output += '\n'

        output += f"\n {self.getTechniqueTitle()}"
        for res in self.technique_results:
            output += f"\n {self.getSingleResStr(res)}"
        output += '\n'

        output += f"\n {self.getProbeTitle()}"
        for res in self.probe_results:
            output += f"\n {self.getSingleProbeResStr(res)}"
        output += '\n'

        output += f"\n {self.getTransformTitle()}"
        for res in self.transform_results:
            output += f"\n {self.getSingleResStr(res)}"
        output += '\n'
 
        return output