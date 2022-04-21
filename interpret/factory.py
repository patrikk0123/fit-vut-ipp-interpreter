## @package factory
#  Factory design pattern implementation.

from interpret.instruction import *
import utils.error as error

## Instruction factory.
#
#  Implements Factory design pattern.
class InstrFactory:
  ## Map of opcodes to classes.
  _opcodes = {
    "MOVE":        MoveInstr,
    "CREATEFRAME": CreateframeInstr,
    "PUSHFRAME":   PushframeInstr,
    "POPFRAME":    PopframeInstr,
    "DEFVAR":      DefvarInstr,
    "CALL":        CallInstr,
    "RETURN":      ReturnInstr,
    "PUSHS":       PushsInstr,
    "POPS":        PopsInstr,
    "RETURN":      ReturnInstr,
    "ADD":         AddInstr,
    "SUB":         SubInstr,
    "MUL":         MulInstr,
    "IDIV":        IdivInstr,
    "LT":          LesserThanInstr,
    "GT":          GreaterThanInstr,
    "EQ":          EqualsInstr,
    "AND":         AndInstr,
    "OR":          OrInstr,
    "NOT":         NotInstr,
    "INT2CHAR":    IntToCharInstr,
    "STRI2INT":    StringToIntInstr,
    "READ":        ReadInstr,
    "WRITE":       WriteInstr,
    "CONCAT":      ConcatInstr,
    "STRLEN":      StrlenInstr,
    "GETCHAR":     GetcharInstr,
    "SETCHAR":     SetcharInstr,
    "TYPE":        TypeInstr,
    "LABEL":       LabelInstr,
    "JUMP":        JumpInstr,
    "JUMPIFEQ":    JumpIfEqInstr,
    "JUMPIFNEQ":   JumpIfNeqInstr,
    "EXIT":        ExitInstr,
    "DPRINT":      DprintInstr,
    "BREAK":       BreakInstr,
    "CLEARS":      ClearsInstr,
    "ADDS":        AddStackInstr,
    "SUBS":        SubStackInstr,
    "MULS":        MulStackInstr,
    "IDIVS":       IdivStackInstr,
    "LTS":         LesserThanStackInstr,
    "GTS":         GreaterThanStackInstr,
    "EQS":         EqualsStackInstr,
    "ANDS":        AndStackInstr,
    "ORS":         OrStackInstr,
    "NOTS":        NotStackInstr,
    "INT2CHARS":   IntToCharStackInstr,
    "STRI2INTS":   StringToIntStackInstr,
    "JUMPIFEQS":   JumpIfEqStackInstr,
    "JUMPIFNEQS":  JumpIfNotEqStackInstr
  }

  ## Create instruction object of given opcode.
  #  @param opcode Opcode of instruction.
  #  @param order Order of instruction.
  #  @return Created instruction object.
  @classmethod
  def create_instr(cls, opcode, order):
    try:
      return cls._opcodes[opcode](order)
    except KeyError:
      error.error_exit(error.XMLSTRUCT_ERROR, "Invalid opcode")
