import os
import sys
from interpreter import Interpreter

if __name__ == "__main__":
    path = input("\nEnter the path to the code file: ")
    if not os.path.exists(path):
        print(f"file {path} not found")
        sys.exit(1)
    interpreter = Interpreter(path)
    interpreter.run()