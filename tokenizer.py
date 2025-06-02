import os
import sys

class Tokenizer:
    def __init__(self, code_path):
        path = code_path

        if os.path.exists(path):
            with open(path, 'r') as file:
                self.code = file.readlines()
        else:
            raise FileNotFoundError(f"File {path} not found.")
        
        self.program = []
        self.labels = {}
        self.functions = {}
        self.current_token = 0
        
        self.tokenize()

    def tokenize(self):
        for line in self.code:
            line = line.strip()
            parts = line.split(' ')

            opcode = parts[0]

            if opcode.endswith(':'):
                self.labels[opcode[:-1]] = self.current_token
                continue
            
            if opcode == ' ' or opcode == '':
                continue
            
            self.program.append(opcode)
            self.current_token += 1

            if opcode == 'push':
                arg = int(parts[1])
                self.program.append(arg)
                self.current_token += 1
            if opcode == 'store':
                arg = int(parts[1])
                self.program.append(arg)
                self.current_token += 1
            if opcode == 'load':
                arg = int(parts[1])
                self.program.append(arg)
                self.current_token += 1    
            if opcode == 'var':
                name = parts[1]
                operand = parts[2]
                if operand == '=':
                    value = int(parts[3])
                    self.program.append(name)
                    self.program.append(operand)
                    self.program.append(value)
                    self.current_token += 3
                else:
                    print(f"invalid variable declaration: {line}")
                    sys.exit(1)
            if opcode == 'pull':
                arg = parts[1]
                self.program.append(arg)
                self.current_token += 1
            if opcode == 'write':
                arg = ' '.join(parts[1:])[1:-1]
                self.program.append(arg)
                self.current_token += 1
            if opcode == 'jumpGreater0':
                arg = parts[1]
                self.program.append(arg)
                self.current_token += 1
            if opcode == 'jump0':
                arg = parts[1]
                self.program.append(arg)
                self.current_token += 1
            if opcode == 'function':
                name = parts[1][:-1]
                self.program.append(name)
                self.functions[name] = self.current_token
            if opcode == 'call':
                arg = parts[1]
                self.program.append(arg)
                if arg in self.functions:
                  self.current_token += 1
                else:
                    print(f"Unidentified function name: {arg}")

        print(str(self.program) + "\n")
