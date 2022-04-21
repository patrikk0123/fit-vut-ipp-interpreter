## @package core
#  Interpreter data structure and access methods
#  implementation.

from interpret.instruction import LabelInstr
from interpret.structs import Value
import utils.error as error

import sys

## Interpreter and its state.
#
#  Holds information about instructions, variables
#  and whole state of interpretation.
class Interpreter:
  ## Input stream for read instruction.
  input_stream = None

  ## Interpreter constructor.
  def __init__(self):
    self._counter = 0     ## Instruction counter.
    self._instr_list = [] ## All instructions list.
    self._labels = {}     ## Labels and their position in code.
    self._globframe = {}  ## Global frame.
    self._locframes = []  ## Local frame stack.
    self._tmpframe = None ## Temporary frame.
    self._callstack = []  ## Call stack.
    self._datastack = []  ## Data stack.

  ## Append instruction to instruction list.
  #  @param instr Instruction to append.
  def append_instr(self, instr):
    self._instr_list.append(instr)

  ## Sorts instructions list by their order.
  def instr_sort(self):
    self._instr_list.sort(key = lambda x: x.order)

  ## Loops through instructions and saves label positions.
  def find_labels(self):
    for idx, instr in enumerate(self._instr_list):
      if isinstance(instr, LabelInstr):
        label_name = instr.arg1.value
        if label_name in self._labels:
          error.error_exit(error.SEMANTIC_ERROR, "Label already exist")

        self._labels[label_name] = idx

  ## Runs interpeter's instructions.
  #  @details After each instruction is run, counter is incremented by one.
  #           If counter was modified by jump, call or ret function,
  #           counter is still incremented.
  #           After the execution, state is reseted.
  def execute(self):
    while self._counter < len(self._instr_list):
      self._instr_list[self._counter].do()
      self._counter += 1

    self.reset_state()

  ## Resets interpeter state.
  ## @details Resets to state state as if no instructions were run.
  ##          Insturction list and dictionary of labels is kept.
  def reset_state(self):
    self._counter = 0
    self._globframe = {}
    self._locframes = []
    self._tmpframe = None
    self._callstack = []
    self._datastack = []

  ## Return frame by name.
  #  @details If frame is local frame,
  #           topmost local frame is returned.
  #  @param frame_name Name of frame to return.
  #  @return Frame coressponding to name.
  def _get_frame(self, frame_name):
    if frame_name == "LF":
      if not self._locframes:
        error.error_exit(error.NOFRAME_ERROR, "Frame does not exist")
      return self._locframes[-1]
    elif frame_name == "GF":
      return self._globframe
    elif frame_name == "TF":
      if self._tmpframe is None:
        error.error_exit(error.NOFRAME_ERROR, "Frame does not exist")
      return self._tmpframe

  ## Create temporary frame.
  def create_tmpframe(self):
    self._tmpframe = {}

  ## Push temporary frame to the top of the local frames stack.
  def locframes_push(self):
    if self._tmpframe is None:
      error.error_exit(error.NOFRAME_ERROR, "Temporary frame does not exist")

    self._locframes.append(self._tmpframe)
    self._tmpframe = None

  ## Pop frame from top of local frames stack and make it a temporary frame.
  def locframes_pop(self):
    if not self._locframes:
      error.error_exit(error.NOFRAME_ERROR, "Empty local frames stack")

    self._tmpframe = self._locframes.pop()

  ## Create variable on specified frame.
  #  @param frame_name Name of frame where to create variable.
  #  @param var_name Name of variable to create.
  def create_var(self, frame_name, var_name):
    frame = self._get_frame(frame_name)
    if var_name in frame:
      error.error_exit(error.SEMANTIC_ERROR, "Variable already exist")

    frame[var_name] = Value()

  ## Return variable on specified frame.
  #  @param frame_name Name of frame where to search.
  #  @param var_name Name of variable to find.
  #  @return Found variable.
  def get_var(self, frame_name, var_name):
    frame = self._get_frame(frame_name)
    if not var_name in frame:
      error.error_exit(error.NOVAR_ERROR, "Variable does not exist")

    var = frame[var_name]
    return var

  ## Return initialized variable on specified frame.
  #  @details Same as get_var, but requires that variable is initialized.
  #  @param frame_name Name of frame where to search.
  #  @param var_name Name of variable to find.
  #  @return Found variable.
  def read_var(self, frame_name, var_name):
    var = self.get_var(frame_name, var_name)
    if var.type is None:
      error.error_exit(error.NOVALUE_ERROR, "Variable not initialized")

    return var

  ## Returns symbol from argument.
  #  @details Variable must be initialized.
  #  @param arg Argument of instruction.
  #  @return Variable if argument type is variable.
  #          Or arg if argument type is constant.
  def get_symbol(self, arg):
    if arg.type == "var":
      return self.read_var(arg.frame, arg.value)
    else:
      return arg

  ## Get label position in code.
  #  @param label_name Name of label.
  #  @return Label position in code.
  def get_label(self, label_name):
    if label_name not in self._labels:
      error.error_exit(error.SEMANTIC_ERROR, "Label does not exist")

    return self._labels[label_name]

  ## Jump to position in code.
  #  @details Next instruction to be interpreted is pos + 1.
  #  @param pos Position where to jump.
  def jump(self, pos):
    self._counter = pos
  
  ## Jump to position in code and save previous one on call stack.
  #  @details Next instruction to be interpreted is pos + 1.
  #           Saves previous position so ret function can be called.
  #  @param pos Position where to jump.
  def call(self, pos):
    self._callstack.append(self._counter)
    self.jump(pos)

  ## Gets position from call stack and jumps to that position.
  #  @details Next instruction to be interpreted is
  #           position from call stack + 1.
  #           call function should have been called before.
  def ret(self):
    if not self._callstack:
      error.error_exit(error.NOVALUE_ERROR, "Empty callstack")

    self._counter = self._callstack.pop()

  ## Push value on data stack.
  #  @param value Value to push.
  def datastack_push(self, value):
    self._datastack.append(value)

  ## Pop value from data stack and return it.
  #  @details Value popped is deleted from data stack.
  #  @returns Popped value.
  def datastack_pop(self):
    if not self._datastack:
      error.error_exit(error.NOVALUE_ERROR, "Empty data stack")

    return self._datastack.pop()

  ## Deletes contents of datastack.
  def datastack_clear(self):
    self._datastack = []

  ## Prints frame variables to STDERR.
  #  @param frame Frame to print.
  def _print_frame(self, frame):
    for key in frame:
      print(f"  {key}: {frame[key].value} of {frame[key].type}", file=sys.stderr)

  ## Prints state of a interpreter to STDERR.
  def print_internal(self):
    print("Code position:", self._counter + 1, file=sys.stderr)
    print("Global frame:", file=sys.stderr)
    if self._globframe:
      self._print_frame(self._globframe)
    else:
      print("  empty", file=sys.stderr)
    print("Temporary frame:", file=sys.stderr)
    if self._tmpframe is not None and self._tmpframe:
      self._print_frame(self._tmpframe)
    if self._tmpframe is not None:
      print("  empty", file=sys.stderr)
    else:
      print("  none", file=sys.stderr)
    print("Topmost local frame:", file=sys.stderr)
    if self._locframes and self._locframes[-1]:
      self._print_frame(self._locframes[-1])
    elif self._locframes:
      print("  empty", file=sys.stderr)
    else:
      print("  none", file=sys.stderr)
    print("Data stack:", file=sys.stderr)
    if self._datastack:
      for i in self._datastack:
        print(f"  {i.value} of {i.type}", file=sys.stderr)
    else:
      print("  empty", file=sys.stderr)
