#!/usr/bin/env python3
from typing import Tuple, List, Dict

class Evaluation:
    def __init__(self, clean_payload_hits: List[str], exploit_hits: Dict[str, Tuple[int, int]]) -> None:
        self.clean_payload_hits = clean_payload_hits
        self.exploit_hits = exploit_hits

    def __str__(self) -> str:
        output = "\n--- RESULTS ---"
        output += "\nClean payloads hit: %i" % len(self.clean_payload_hits)
        for i, clean_payload in enumerate(self.clean_payload_hits):
            output += "\nPayload %i: '%s'" % (i+1, clean_payload)
        
        if not self.exploit_hits.items(): 
            output += "\nALL PROMPTS HIT CLEAN \nNO EXPLOITS TESTED"
        else:
            for exploit, tuple in self.exploit_hits.items():
                hits, total = tuple
                output += "\nExploit: %s - ASR %i (%i/%i)" % (exploit, (hits/total*100), hits, total)
        
        return output
