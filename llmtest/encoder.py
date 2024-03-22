#!/usr/bin/env python3
import codecs

class Encoder:
    @staticmethod
    def encodeROT13(s: str):
        return codecs.encode(s, 'rot_13')

    @staticmethod
    def decodeROT13(s: str):
        return codecs.decode(s, 'rot_13')
    