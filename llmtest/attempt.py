#!/usr/bin/env python3
from llmtest.transforms import Transform
from llmtest.probes import Probe

class Attempt:
    def __init__(self, transform: Transform, probe: Probe) -> None:
        self.transform = transform
        self.probe = probe
        self.payload = probe.getPayload()
        self.prompt = self.transform.applyExploits(probe.getPayload())
        self.replies = []

    def getTransform(self) -> Transform:
        return self.transform
    
    def getProbe(self) -> Probe:
        return self.probe

    def getPayload(self) -> str:
        return self.payload
    
    def getPrompt(self) -> str:
        return self.prompt
    
    def getReplies(self) -> list:
        return self.replies
    
    def addReply(self, answer:str, detection:bool):
        self.replies.append(
            {
                "answer": answer,
                "detection": detection
            }
        )

    def getAttemptSuccessRate(self) -> float:
        if len(self.replies) == 0: return None

        hit_count = 0
        for reply in self.replies:
            if reply["detection"]: hit_count = hit_count + 1
        
        return hit_count/len(self.replies)