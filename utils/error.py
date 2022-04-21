## @package error
#  Error codes and exit function.

import sys

# Error code constants.
## Invalid or missing CLI argument.
CLIARG_ERROR    = 10
## Cannot acces file.
FILE_ERROR      = 11
## XML is not well-formed.
XMLFORMAT_ERROR = 31
## Bad XML structure.
XMLSTRUCT_ERROR = 32
## Semantic error.
SEMANTIC_ERROR  = 52
## Invalid operator types.
TYPE_ERROR      = 53
## Variable does not exist.
NOVAR_ERROR     = 54
## Frame does not exist.
NOFRAME_ERROR   = 55
## Missing value in data structure.
NOVALUE_ERROR   = 56
## Invalid value of a operand.
INVVALUE_ERROR  = 57
## String operation error.
STRING_ERROR    = 58

## Error exit of a program.
#  @details Print message to STDERR and
#           exit program with error code.
#           Message is printed in following format:
#           "ERROR: message\n"
#  @param error_code Error code to exit with.
#  @param error_msg  Error message to print to STDERR.
def error_exit(error_code, error_msg):
  sys.stderr.write(f"ERROR: {error_msg}\n")
  exit(error_code)
