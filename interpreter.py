import os
import sys
from tokenizer import Tokenizer
from tools import Variable, Stack

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
                  operand = program[pc + 1]
                  if operand == '=':
                      pc += 2
                  value = program[pc]
                  variable = Variable(name, value)
                  for i in variables_stack.buffer:
                      if isinstance(i, Variable) and i.name == name:
                          variables_stack.buffer.remove(i)
                          variables_stack.sp -= 1
                  variables_stack.push(variable)
                  pc += 1
              elif opcode == 'pull':
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

              #### debugging printing ####
              #print(f"instruction: {opcode}")
              #print(f"stack: {stack.buffer}, variables stack: {variables_stack.buffer}")

            except IndexError:
                  print("something went wrong with stack, check stack bro")
                  break
            except KeyError:
                  print(f"something went wrong with labels, label {program[pc]} not found")
                  break
            except ValueError:
                  print(f"invalid value: {program[pc]}")
                  break