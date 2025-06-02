import os
import sys
from interpreter import Interpreter

class REPLInterpreter():
    def run_repl(self):
        print("\nREPL mode is active. Type 'exit' to quit.")
        while True:
            try:
                line = input(">> ").strip()
                if line.lower() == 'exit':
                    break
                if line == '':
                    continue
                with open("temp_code.tmp", "a") as file:
                    file.write(line + "\n")
            except Exception as e:
                print(f"An error occurred: {e}")
                continue
          
        interpreter = Interpreter("temp_code.tmp")
        interpreter.run()
        os.remove("temp_code.tmp")

        