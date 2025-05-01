import os
import sys
from interpreter import Interpreter
from repl_mode import REPLInterpreter

if __name__ == "__main__":
    path = input("\ntype 'repl' if you want REPL mode/\nenter the path to the code file: ")
    if path == 'REPL' or path == 'repl':
        repl_interpreter = REPLInterpreter()
        repl_interpreter.run_repl()
        sys.exit(0)
    if not os.path.exists(path):
        print(f"file {path} not found")
        sys.exit(1)
    interpreter = Interpreter(path)
    interpreter.run()