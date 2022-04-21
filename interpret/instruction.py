## @package instruction
#  Instructions and their code.

from interpret.structs import Value
import utils.error as error

import sys

## Instruction to be run.
#
#  Provides interface for specific instructions
#  of IPPcode.
class Instruction:
  ## Interpeter for instructions to be interpreted on.
  _interpreter = None
  
  ## Sets interpreter for all instructions.
  #  @details Can be set only once. Otherwise ignored.
  @classmethod
  def set_interpeter(cls, interpeter):
    if cls._interpreter is None:
      cls._interpreter = interpeter

  ## Instruction constructor.
  #  @param order Order of instruction.
  def __init__(self, order):
    self.order = order ## Instruction order
    self.arg1 = None   ## Instruction argument no 1
    self.arg2 = None   ## Instruction argument no 2
    self.arg3 = None   ## Instruction argument no 3

  ## Run instruction.
  #  @details Is overriden in subclasses.
  def do(self):
    pass

## MOVE instruction.
class MoveInstr(Instruction):
  def do(self):
    symb = self._interpreter.get_symbol(self.arg2)
    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = symb.value
    var.type = symb.type

## CREATEFRAME instruction.
class CreateframeInstr(Instruction):
  def do(self):
    self._interpreter.create_tmpframe()

## PUSHFRAME instruction.
class PushframeInstr(Instruction):
  def do(self):
    self._interpreter.locframes_push()

## POPFRAME instruction.
class PopframeInstr(Instruction):
  def do(self):
    self._interpreter.locframes_pop()

## DEFVAR instruction.
class DefvarInstr(Instruction):
  def do(self):
    self._interpreter.create_var(self.arg1.frame, self.arg1.value)

## CALL instruction.
class CallInstr(Instruction):
  def do(self):
    call_val = self._interpreter.get_label(self.arg1.value)
    self._interpreter.call(call_val)

## RETURN instruction.
class ReturnInstr(Instruction):
  def do(self):
    self._interpreter.ret()

## PUSHS instruction.
class PushsInstr(Instruction):
  def do(self):
    symb = self._interpreter.get_symbol(self.arg1)
    value = Value()
    value.value = symb.value
    value.type = symb.type
    self._interpreter.datastack_push(value)

## POPS instruction.
class PopsInstr(Instruction):
  def do(self):
    symb = self._interpreter.datastack_pop()
    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = symb.value
    var.type = symb.type

## ADD instruction.
class AddInstr(Instruction):
  def do(self):
    symb1 = self._interpreter.get_symbol(self.arg2)
    symb2 = self._interpreter.get_symbol(self.arg3)
    if symb1.type != "int" or symb2.type != "int":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = symb1.value + symb2.value
    var.type = "int"

## SUB instruction.
class SubInstr(Instruction):
  def do(self):
    symb1 = self._interpreter.get_symbol(self.arg2)
    symb2 = self._interpreter.get_symbol(self.arg3)
    if symb1.type != "int" or symb2.type != "int":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = symb1.value - symb2.value
    var.type = "int"

## MUL instruction.
class MulInstr(Instruction):
  def do(self):
    symb1 = self._interpreter.get_symbol(self.arg2)
    symb2 = self._interpreter.get_symbol(self.arg3)
    if symb1.type != "int" or symb2.type != "int":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = symb1.value * symb2.value
    var.type = "int"

## IDIV instruction.
class IdivInstr(Instruction):
  def do(self):
    symb1 = self._interpreter.get_symbol(self.arg2)
    symb2 = self._interpreter.get_symbol(self.arg3)
    if symb1.type != "int" or symb2.type != "int":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")
    if symb2.value == 0:
      error.error_exit(error.INVVALUE_ERROR, "Zero division")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = symb1.value // symb2.value
    var.type = "int"

## LT instruction.
class LesserThanInstr(Instruction):
  def do(self):
    symb1 = self._interpreter.get_symbol(self.arg2)
    symb2 = self._interpreter.get_symbol(self.arg3)
    if symb1.type != symb2.type:
      error.error_exit(error.TYPE_ERROR, "Bad operator types")
    if symb1.type == "nil" or symb2.type == "nil":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = symb1.value < symb2.value
    var.type = "bool"

## GT instruction.
class GreaterThanInstr(Instruction):
  def do(self):
    symb1 = self._interpreter.get_symbol(self.arg2)
    symb2 = self._interpreter.get_symbol(self.arg3)
    if symb1.type != symb2.type:
      error.error_exit(error.TYPE_ERROR, "Bad operator types")
    if symb1.type == "nil" or symb2.type == "nil":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = symb1.value > symb2.value
    var.type = "bool"

## EQ instruction.
class EqualsInstr(Instruction):
  def do(self):
    symb1 = self._interpreter.get_symbol(self.arg2)
    symb2 = self._interpreter.get_symbol(self.arg3)
    if symb1.type != symb2.type and symb1.type != "nil" and symb2.type != "nil":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = symb1.value == symb2.value
    var.type = "bool"

## AND instruction.
class AndInstr(Instruction):
  def do(self):
    symb1 = self._interpreter.get_symbol(self.arg2)
    symb2 = self._interpreter.get_symbol(self.arg3)
    if symb1.type != "bool" or symb2.type != "bool":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = symb1.value and symb2.value
    var.type = "bool"

## OR instruction.
class OrInstr(Instruction):
  def do(self):
    symb1 = self._interpreter.get_symbol(self.arg2)
    symb2 = self._interpreter.get_symbol(self.arg3)
    if symb1.type != "bool" or symb2.type != "bool":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = symb1.value or symb2.value
    var.type = "bool"

## NOT instruction.
class NotInstr(Instruction):
  def do(self):
    symb = self._interpreter.get_symbol(self.arg2)
    if symb.type != "bool":
      error.error_exit(error.TYPE_ERROR, "Bad operator type")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = not symb.value
    var.type = "bool"

## INT2CHAR instruction.
class IntToCharInstr(Instruction):
  def do(self):
    symb = self._interpreter.get_symbol(self.arg2)
    if symb.type != "int":
      error.error_exit(error.TYPE_ERROR, "Bad operator type")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    try:
      var.value = chr(symb.value)
      var.type = "string"
    except ValueError:
      error.error_exit(error.STRING_ERROR, "Value is not valid UNICODE codepoint")

## STRI2INT instruction.
class StringToIntInstr(Instruction):
  def do(self):
    symb1 = self._interpreter.get_symbol(self.arg2)
    symb2 = self._interpreter.get_symbol(self.arg3)
    if symb1.type != "string" or symb2.type != "int":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")
    if symb2.value >= len(symb1.value):
      error.error_exit(error.STRING_ERROR, "Index out of range")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = ord(symb1.value[symb2.value])
    var.type = "int"

## READ instruction.
class ReadInstr(Instruction):
  def do(self):
    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    type = self.arg2.value
    val = self._interpreter.input_stream.readline().rstrip('\n')
    try:
      if type == "int":
        var.value = int(val)
      elif type == "string":
        var.value = val
      elif type == "bool":
        if val.lower() == "true":
          var.value = True  
        else:
          var.value = False
      var.type = type
    except ValueError:
      var.value = None
      var.type = "nil"

## WRITE instruction.
class WriteInstr(Instruction):
  def do(self):
    symb = self._interpreter.get_symbol(self.arg1)
    if symb.type == "bool":
      print("true", end='') if symb.value else print("false", end='')
    elif symb.type == "nil":
      pass
    else:
      print(symb.value, end='')

    sys.stdout.flush()

## CONCAT instruction.
class ConcatInstr(Instruction):
  def do(self):
    symb1 = self._interpreter.get_symbol(self.arg2)
    symb2 = self._interpreter.get_symbol(self.arg3)
    if symb1.type != "string" or symb2.type != "string":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = symb1.value + symb2.value
    var.type = "string"

## STRLEN instruction.
class StrlenInstr(Instruction):
  def do(self):
    symb = self._interpreter.get_symbol(self.arg2)
    if symb.type != "string":
      error.error_exit(error.TYPE_ERROR, "Bad operator type")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = len(symb.value)
    var.type = "int"

## GETCHAR instruction.
class GetcharInstr(Instruction):
  def do(self):
    symb1 = self._interpreter.get_symbol(self.arg2)
    symb2 = self._interpreter.get_symbol(self.arg3)
    if symb1.type != "string" or symb2.type != "int":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")
    if symb2.value >= len(symb1.value):
      error.error_exit(error.STRING_ERROR, "Index out of range")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    var.value = symb1.value[symb2.value]
    var.type = "string"

## SETCHAR instruction.
class SetcharInstr(Instruction):
  def do(self):
    symb1 = self._interpreter.get_symbol(self.arg2)
    symb2 = self._interpreter.get_symbol(self.arg3)
    if symb1.type != "int" or symb2.type != "string":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")
    if not len(symb2.value):
      error.error_exit(error.STRING_ERROR, "Empty string")

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    if var.type != "string":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")
    if symb1.value >= len(var.value):
      error.error_exit(error.STRING_ERROR, "Index out of range")
    
    var.value = var.value[:symb1.value] + symb2.value[0] + var.value[symb1.value + 1:]

## TYPE instruction.
class TypeInstr(Instruction):
  def do(self):
    symb = self._interpreter.get_symbol(self.arg2)

    var = self._interpreter.get_var(self.arg1.frame, self.arg1.value)
    if symb.type is not None:
      var.value = symb.type
    else:
      var.value = ""
    var.type = "string"

## LABEL instruction.
class LabelInstr(Instruction):
  pass

## JUMP instruction.
class JumpInstr(Instruction):
  def do(self):
    jump_val = self._interpreter.get_label(self.arg1.value)
    self._interpreter.jump(jump_val)

## JUMPIFEQ instruction.
class JumpIfEqInstr(Instruction):
  def do(self):
    jump_val = self._interpreter.get_label(self.arg1.value)
    symb1 = self._interpreter.get_symbol(self.arg2)
    symb2 = self._interpreter.get_symbol(self.arg3)
    if symb1.type != symb2.type and symb1.type != "nil" and symb2.type != "nil":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    if symb1.value == symb2.value:
      self._interpreter.jump(jump_val)

## JUMPIFNEQ instruction.
class JumpIfNeqInstr(Instruction):
  def do(self):
    jump_val = self._interpreter.get_label(self.arg1.value)
    symb1 = self._interpreter.get_symbol(self.arg2)
    symb2 = self._interpreter.get_symbol(self.arg3)
    if symb1.type != symb2.type and symb1.type != "nil" and symb2.type != "nil":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    if symb1.value != symb2.value:
      self._interpreter.jump(jump_val)

## EXIT instruction.
class ExitInstr(Instruction):
  def do(self):
    symb = self._interpreter.get_symbol(self.arg1)
    if symb.type != "int":
      error.error_exit(error.TYPE_ERROR, "Bad operator type")
    if not 0 <= symb.value <= 49:
      error.error_exit(error.INVVALUE_ERROR, "Error code out of range of 0-49")

    exit(symb.value)

## DPRINT instruction.
class DprintInstr(Instruction):
  def do(self):
    symb = self._interpreter.get_symbol(self.arg1)
    if symb.type == "bool":
      sys.stderr.write("true") if symb.value else sys.stderr.write("false")
    elif symb.type == "nil":
      pass
    else:
      sys.stderr.write(str(symb.value))

## BREAK instruction.
class BreakInstr(Instruction):
  def do(self):
    self._interpreter.print_internal()

# --- STACK extension instructions ---

## CLEARS instruction.
class ClearsInstr(Instruction):
  def do(self):
    self._interpreter.datastack_clear()

## ADDS instruction.
class AddStackInstr(Instruction):
  def do(self):
    symb2 = self._interpreter.datastack_pop()
    symb1 = self._interpreter.datastack_pop()
    if symb1.type != "int" or symb2.type != "int":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    result = Value()
    result.value = symb1.value + symb2.value
    result.type = "int"
    self._interpreter.datastack_push(result)

## SUBS instruction.
class SubStackInstr(Instruction):
  def do(self):
    symb2 = self._interpreter.datastack_pop()
    symb1 = self._interpreter.datastack_pop()
    if symb1.type != "int" or symb2.type != "int":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    result = Value()
    result.value = symb1.value - symb2.value
    result.type = "int"
    self._interpreter.datastack_push(result)

## MULS instruction.
class MulStackInstr(Instruction):
  def do(self):
    symb2 = self._interpreter.datastack_pop()
    symb1 = self._interpreter.datastack_pop()
    if symb1.type != "int" or symb2.type != "int":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    result = Value()
    result.value = symb1.value * symb2.value
    result.type = "int"
    self._interpreter.datastack_push(result)

## IDIVS instruction.
class IdivStackInstr(Instruction):
  def do(self):
    symb2 = self._interpreter.datastack_pop()
    symb1 = self._interpreter.datastack_pop()
    if symb1.type != "int" or symb2.type != "int":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    result = Value()
    result.value = symb1.value // symb2.value
    result.type = "int"
    self._interpreter.datastack_push(result)

## LTS instruction.
class LesserThanStackInstr(Instruction):
  def do(self):
    symb2 = self._interpreter.datastack_pop()
    symb1 = self._interpreter.datastack_pop()
    if symb1.type != symb2.type:
      error.error_exit(error.TYPE_ERROR, "Bad operator types")
    if symb1.type == "nil" or symb2.type == "nil":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    result = Value()
    result.value = symb1.value < symb2.value
    result.type = "bool"
    self._interpreter.datastack_push(result)

## GTS instruction.
class GreaterThanStackInstr(Instruction):
  def do(self):
    symb2 = self._interpreter.datastack_pop()
    symb1 = self._interpreter.datastack_pop()
    if symb1.type != symb2.type:
      error.error_exit(error.TYPE_ERROR, "Bad operator types")
    if symb1.type == "nil" or symb2.type == "nil":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    result = Value()
    result.value = symb1.value > symb2.value
    result.type = "bool"
    self._interpreter.datastack_push(result)

## EQS instruction.
class EqualsStackInstr(Instruction):
  def do(self):
    symb2 = self._interpreter.datastack_pop()
    symb1 = self._interpreter.datastack_pop()
    if symb1.type != symb2.type and symb1.type != "nil" and symb2.type != "nil":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")
    
    result = Value()
    result.value = symb1.value == symb2.value
    result.type = "bool"
    self._interpreter.datastack_push(result)

## ANDS instruction.
class AndStackInstr(Instruction):
  def do(self):
    symb2 = self._interpreter.datastack_pop()
    symb1 = self._interpreter.datastack_pop()
    if symb1.type != "bool" or symb2.type != "bool":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    result = Value()
    result.value = symb1.value and symb2.value
    result.type = "bool"
    self._interpreter.datastack_push(result)

## ORS instruction.
class OrStackInstr(Instruction):
  def do(self):
    symb2 = self._interpreter.datastack_pop()
    symb1 = self._interpreter.datastack_pop()
    if symb1.type != "bool" or symb2.type != "bool":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    result = Value()
    result.value = symb1.value or symb2.value
    result.type = "bool"
    self._interpreter.datastack_push(result)

## NOTS instruction.
class NotStackInstr(Instruction):
  def do(self):
    symb = self._interpreter.datastack_pop()
    if symb.type != "bool":
      error.error_exit(error.TYPE_ERROR, "Bad operator type")

    result = Value()
    result.value = not symb.value
    result.type = "bool"
    self._interpreter.datastack_push(result)

## INT2CHARS instruction.
class IntToCharStackInstr(Instruction):
  def do(self):
    symb = self._interpreter.datastack_pop()
    if symb.type != "int":
      error.error_exit(error.TYPE_ERROR, "Bad operator type")

    result = Value()
    try:
      result.value = chr(symb.value)
      result.type = "string"
      self._interpreter.datastack_push(result)
    except ValueError:
      error.error_exit(error.STRING_ERROR, "Value is not valid UNICODE codepoint")

## STRI2INTS instruction.
class StringToIntStackInstr(Instruction):
  def do(self):
    symb2 = self._interpreter.datastack_pop()
    symb1 = self._interpreter.datastack_pop()
    if symb1.type != "string" or symb2.type != "int":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")
    if symb2.value >= len(symb1.value):
      error.error_exit(error.STRING_ERROR, "Index out of range")

    result = Value()
    result.value = ord(symb1.value[symb2.value])
    result.type = "int"
    self._interpreter.datastack_push(result)

  ## JUMPIFEQS instruction.
class JumpIfEqStackInstr(Instruction):
  def do(self):
    jump_val = self._interpreter.get_label(self.arg1.value)
    symb2 = self._interpreter.datastack_pop()
    symb1 = self._interpreter.datastack_pop()
    if symb1.type != symb2.type and symb1.type != "nil" and symb2.type != "nil":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    if symb1.value == symb2.value:
      self._interpreter.jump(jump_val)

## JUMPIFNEQS instruction.
class JumpIfNotEqStackInstr(Instruction):
  def do(self):
    jump_val = self._interpreter.get_label(self.arg1.value)
    symb2 = self._interpreter.datastack_pop()
    symb1 = self._interpreter.datastack_pop()
    if symb1.type != symb2.type and symb1.type != "nil" and symb2.type != "nil":
      error.error_exit(error.TYPE_ERROR, "Bad operator types")

    if symb1.value != symb2.value:
      self._interpreter.jump(jump_val)
