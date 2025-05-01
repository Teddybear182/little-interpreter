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
                arg = parts[1]
                self.program.append(arg)
                self.current_token += 1
            if opcode == 'v':
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

        print(str(self.program) + "\n")


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


class Interpreter:
    def __init__(self, code_path):
        self.path = code_path

    def run(self):
        print("\n\n░█░░░▀█▀░▀█▀░▀█▀░█░░░█▀▀░░░▀█▀░█▀█░▀█▀░█▀▀░█▀▄░█▀█░█▀▄░█▀▀░▀█▀░█▀▀░█▀▄")
        print("░█░░░░█░░░█░░░█░░█░░░█▀▀░░░░█░░█░█░░█░░█▀▀░█▀▄░█▀▀░█▀▄░█▀▀░░█░░█▀▀░█▀▄")
        print("░▀▀▀░▀▀▀░░▀░░░▀░░▀▀▀░▀▀▀░░░▀▀▀░▀░▀░░▀░░▀▀▀░▀░▀░▀░░░▀░▀░▀▀▀░░▀░░▀▀▀░▀░▀")
        print("BY FYODOR BELOUSOV\n\n")

        tokenizer = Tokenizer(self.path)
        stack = Stack(256)
        variables_stack = Stack(256)
        program = tokenizer.program
        labels = tokenizer.labels
        pc = 0 #program counter

        while pc < len(program) and program[pc] != 'stop':
            try:
              opcode = program[pc] #get the opcode
              pc += 1 #get the argument

              if opcode == 'push':
                  stack.push(program[pc])
                  pc += 1
              elif opcode == 'pop':
                  stack.pop()
              elif opcode == 'write':
                  print(str(program[pc] + "\n"))
                  pc += 1
              elif opcode == 'jumpGreater0':
                  number = stack.top()
                  if number > 0:
                      pc = labels[program[pc]]
                  else:
                      pc += 1
              elif opcode == 'jump0':
                  number = stack.top()
                  if number == 0:
                      pc = labels[program[pc]]
                  else:
                      pc += 1
              elif opcode == 'read':
                  value = int(input("enter a number -> "))
                  stack.push(value)  
              elif opcode == 'store':
                value = stack.pop()
                address = int(program[pc])
                stack.buffer[address] = value
                pc += 1
              elif opcode == 'load':
                  address = int(program[pc])
                  value = stack.buffer[address]
                  stack.push(value)
                  stack.buffer[address] = 0
                  pc += 1
              elif opcode == 'var':
                  name = program[pc]
                  pc += 1
                  value = stack.pop()
                  variable = Variable(name, value)
                  variables_stack.push(variable)
              elif opcode == 'v':
                  name = program[pc]
                  pc += 1
                  for i in variables_stack.buffer:
                      if isinstance(i, Variable) and i.name == name:
                          stack.push(i.value)
                          break
              elif opcode == 'add':
                  a = stack.pop()
                  b = stack.pop()
                  stack.push(a + b)
              elif opcode == 'sub':
                  a = stack.pop()
                  b = stack.pop()
                  stack.push(b - a)
              elif opcode == 'mul':
                  a = stack.pop()
                  b = stack.pop()
                  stack.push(a * b)
              elif opcode == 'div':
                  a = stack.pop()
                  b = stack.pop()
                  if a == 0:
                      print("you cant divide by zero bruh")
                      break
                  stack.push(b // a)
              print(f"stack: {stack.buffer}")

            except IndexError:
                  print("something went wrong with stack, check stack bro")
                  break
            except KeyError:
                  print(f"something went wrong with labels, label {program[pc]} not found")
                  break
            except ValueError:
                  print(f"invalid value: {program[pc]}")
                  break

class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value


if __name__ == "__main__":
    path = input("\nEnter the path to the code file: ")
    if not os.path.exists(path):
        print(f"file {path} not found")
        sys.exit(1)
    interpreter = Interpreter(path)
    interpreter.run()