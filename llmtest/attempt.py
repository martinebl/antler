#!/usr/bin/env python3
from llmtest.transforms import Transform
from llmtest.probes import Probe

class Attempt:
    def __init__(self, transform: Transform, probe: Probe, replies=[]) -> None:
        self.transform = transform
        self.probe = probe
        self.payload = probe.getPayload()
        self.prompt = self.transform.applyTechniques(probe.getPayload())
        self.replies = replies

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
    
    def addResponse(self, answer:str, detection:bool):
        self.replies.append(
            {
                "answer": answer,
                "detection": detection
            }
        )

    def addResponseObject(self, reply: object):
        self.replies.append(reply)


    def getAttemptSuccessRate(self) -> float:
        if len(self.replies) == 0: return None

        hit_count = 0
        for reply in self.replies:
            if reply["detection"]: hit_count = hit_count + 1
        
        return hit_count/len(self.replies)
    
    @staticmethod
    def isSame(att1: object, att2: object) -> bool:
        return att1.getTransform() == att2.getTransform() and att1.getProbe() == att2.getProbe()
    
    def __eq__(self, other: object) -> bool:
        return Attempt.isSame(self, other) and self.getReplies() == other.getReplies()
