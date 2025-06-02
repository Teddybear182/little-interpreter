import os
import sys

class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"{self.name}={self.value}"
    

class Stack:
    def __init__(self, size=256):
        self.buffer = [0 for _ in range(size)]
        self.sp = -1 #stack pointer

    def push(self, value):
        self.sp += 1
        self.buffer[self.sp] = value
    def pop(self):
        value = self.buffer[self.sp]
        self.buffer[self.sp] = 0
        self.sp -= 1
        return value
    def top(self):
        return self.buffer[self.sp]
    
class Function:
    def __init__(self, name, code):
        self.name = name
        self.code = code