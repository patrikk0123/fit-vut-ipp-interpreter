## @package parse_xml
#  Parse XML from input file.

from interpret.factory import InstrFactory
from interpret.structs import Argument
import utils.error as error

import re
from sys import stdin
import xml.etree.ElementTree as ET

## Read XML code file and get all instructions.
#  @details Instructions are appended to interpreter.
#           Exits if not valid.
#  @param args        CLI arguments object.
#  @param interpreter Interpreter object to which
#                     instructions are appended.
def get_instructions(args, interpreter):
  xml_file = stdin
  try:
    if args.source:
      xml_file = open(args.source, "r")
  except EnvironmentError as e:
    error.error_exit(error.FILE_ERROR, f"Cannot access file {e.filename}")

  try:
    root_node = ET.parse(xml_file).getroot()
  except ET.ParseError:
    error.error_exit(error.XMLFORMAT_ERROR, "XML not well-formed")
  parse_xml(root_node, interpreter)

  if args.source:
    xml_file.close()

## Check validness of XML document, create instructions
#  and append them to interpreter.
#  @details Converts instructions and arguments from XML
#           to respective classes and created instructions
#           appends to interpreter. Exits if not valid.
#  @param root_node  XML root element.
#  @param interpeter Interpreter object to which
#                    instructions are appended.
def parse_xml(root_node, interpreter):
  check_root(root_node)
  for instr_node in root_node:
    check_instr(instr_node)

    try:
      order = int(instr_node.attrib["order"])
    except ValueError:
      error.error_exit(error.XMLSTRUCT_ERROR, "Opcode not a number")

    if order < 0:
      error.error_exit(error.XMLSTRUCT_ERROR, "Negative opcode")
    instr_obj = InstrFactory.create_instr(instr_node.attrib["opcode"].upper(), order)
    interpreter.append_instr(instr_obj)

    for arg_node in instr_node:
      check_arg(arg_node)
      arg_obj = xml_to_arg(arg_node)
      if(arg_node.tag == "arg1"):
        instr_obj.arg1 = arg_obj
      elif(arg_node.tag == "arg2"):
        instr_obj.arg2 = arg_obj
      elif(arg_node.tag == "arg3"):
        instr_obj.arg3 = arg_obj

## Check validness of XML root element.
#  @details Exits if not valid.
#  @param root_node XML root element.
def check_root(root_node):
  if root_node.tag != "program":
    error.error_exit(error.XMLSTRUCT_ERROR, "Root element must be 'program'")

  if "language" in root_node.attrib:
    if root_node.attrib["language"] != "IPPcode22":
      error.error_exit(error.XMLSTRUCT_ERROR,
                       "'language' attribute must be IPPcode22")
  else:
    error.error_exit(error.XMLSTRUCT_ERROR, "Missing 'language' attribute")

## Check validness of XML instruction element.
#  @details Exits if not valid.
#  @param instr_node XML instruction element.
def check_instr(instr_node):
  if instr_node.tag != "instruction":
    error.error_exit(error.XMLSTRUCT_ERROR,
                     "Root element must contain only instruction elements")

  if "opcode" not in instr_node.attrib:
    error.error_exit(error.XMLSTRUCT_ERROR, "Missing 'opcode' attribute")
  if "order" not in instr_node.attrib:
    error.error_exit(error.XMLSTRUCT_ERROR, "Missing 'order' attribute")

## Check validness of XML argument element.
#  @details Exits if not valid.
#  @param arg XML argument element.
def check_arg(arg_node):
  if not re.match(r"^arg[123]$", arg_node.tag):
    error.error_exit(error.XMLSTRUCT_ERROR,
                     "Instruction element must contain only argument elements")
  
  if not "type" in arg_node.attrib:
    error.error_exit(error.XMLSTRUCT_ERROR, "Missing 'type' attribute")
  if not re.match(r"(int|bool|string|nil|label|type|var)",
                  arg_node.attrib["type"]):
    error.error_exit(error.XMLSTRUCT_ERROR, "Invalid 'type' attribute value")

## Convert XML argument element to Argument class object.
#  @details Exits if not valid.
#  @param arg XML argument element.
#  @return Argument object.
def xml_to_arg(arg_node):
  value = arg_node.text
  type = arg_node.attrib["type"]
  frame = None

  try:
    if type == "var":
      frame = arg_node.text.split("@")[0]
      value = arg_node.text.split("@")[1]
    elif type == "int":
      value = int(value)
    elif type == "string":
      if value is None:
        value = ""
      else:
        value = re.sub(r"\\([0-9]{3})", lambda x: chr(int(x[1])), value)
    elif type == "bool":
      value = True if value.lower() == "true" else False
    elif type == "nil":
      value = None
  except ValueError:
    error.error_exit(error.XMLSTRUCT_ERROR, "Invalid value")
  except IndexError:
    error.error_exit(error.XMLSTRUCT_ERROR, "Invalid variable")

  arg_obj = Argument(type, value, frame)
  return arg_obj
