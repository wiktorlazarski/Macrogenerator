'''
    Script allowing user to test macrogenerator by passing source text as a command line argument.

    Created by Wiktor Lazarski 18/04/2020  
'''

import sys
from .macrogenerator import Macrogenerator

def main():
    sys.stdout.write("Welcome to Macrogenerator module.\n")

    macrogenerator = Macrogenerator()
    for source_text in sys.argv:
        if source_text is sys.argv[0]:
            continue
        try:
            output_text = macrogenerator.transform(source_text)
            sys.stdout.write(f"Input: {source_text}\t=>\tOutput: {output_text}\n")
        except Exception as ex:
            sys.stdout.write(f"Input: {source_text}\t=>\tOutput: {ex.args[0]}\n")

    sys.stdout.flush()

if __name__ == "__main__":
    main()
