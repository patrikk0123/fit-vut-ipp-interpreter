## @package structs
#  Various data structures.

## Interpreter value (variable, datatastack value).
#
#  When created, value and type
#  are uninitialized.
class Value:
  ## Value constructor.
  def __init__(self):
    self.type = None  ## Value type.
    self.value = None ## Value.

## Instruction argument.
#
#  Type and value are compatible with Value class.
class Argument:
  ## Argument constructor.
  def __init__(self, type, value, frame = None):
    self.type = type   ## Argument type (variable, label, int, etc.)
    self.value = value ## Value (variable name, int constant, etc.)
    self.frame = frame ## Name of frame if variable type.
