from interpret.core import Interpreter
from interpret.instruction import Instruction
from parse.cli import get_args
from parse.parse_xml import get_instructions
import utils.error as error

from sys import stdin

## Parse XML and execute intructions.
#  @param args CLI arguments object.
def interpret(args):
  interpreter = Interpreter()

  input_file = stdin
  try:
    if args.input:
      input_file = open(args.input, "r")
  except EnvironmentError as e:
    error.error_exit(error.FILE_ERROR, f"Cannot access file {e.filename}")
  Interpreter.input_stream = input_file
  Instruction.set_interpeter(interpreter)

  get_instructions(args, interpreter)
  interpreter.instr_sort()
  interpreter.find_labels()
  interpreter.execute()

  if args.input:
    input_file.close()

## Entrypoint of a program.
def main():
  args = get_args()
  interpret(args)

if __name__ == "__main__":
  main()
