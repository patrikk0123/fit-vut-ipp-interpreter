Documentation of Project no. 2 Implementation for IPP 2021/2022  
Name and surname: Patrik Korytár  
Login: xkoryt04  

# IPPcode22 Interpreter

Interpreter of XML representation of IPPcode22 language.

## Programming Paradigm

This implementaton uses Object Oriented Programming and implements `NVI` extension.
Factory design pattern is implemented in file (module) `interpret/factory.py`. More description below.

## Used Libraries

Only standard library of Python is used (especially, `regexp`, `argparse`, `xml.etree` modules).

## Code Documentation

Code is documented using Doxygen.

## Implementation Outline

### Parsing XML document

`parse` package includes modules for parsing of CLI arguments and XML file.

`parse.cli` module is used to parse and get CLI arguments. Python's `argparse` module is used for convenience.

Program then uses `parse.parse_xml` module to load XML representation of code. There, it nests and cycles through XML nodes to check if required elements and atrributes are present. During this process, instruction and argument objects are also created and appended to the interpreter instruction list. Implementation uses standard `xml.etree` module.

### Interpretation

`interpret` package implements interpeter and instructions data structures.

`parse.core` module provides `Interpreter` class. This class includes instruction list, label dictionary, all data structures (frames, data / call stack) and instruction counter.

`append_instr` method appends instruction to instruction list. `instr_sort` method sorts all instructions by their order. `find_labels` method cycles through instructions, looks for LABEL instructions and stores position of labels into the dictionary.

`execute` method can then be run to execute all instructions. Instruction counter is used to get instruction to be run from the instruction list. It starts by executing first instruction and ends when last instruction in the list is executed (or EXIT instruction is encountered). After each instruction is run, instruction counter is incremented by one.

`Instruction` class also provides interface for instructions to change state of interpretation, which includes: creating temporary frame, creating new variable, reading from variable, changing instruction counter (by calling a label, for example), work with data stack, etc.

### Instructions

`interpret.instruction` module includes `Instruction` class which provides common interface for all types (opcodes) of instructions. `set_interpeter` class method sets interpeter for all instructions so all of them are being interpreted on the same interpeter. `do` method does nothing, but is overriden in inherited classes to implement instruction code.

Specific types of instructions inherit from `Instruction` class and implement `do` method. They communicate with interpreter to get / store data or change interpreter's state and perform calculations.

### NVI extension

Script is implemented using Object Oriented Programming. Encapsulation made storing of data easier. Classes also help with abstraction and programming is made easier. Inheritance helps reduce code repetition and provide common interface.

All modules insides `interpret` package include classes. Inside `interpret.instruction` module, all types of instruction inherit from `Instruction` class.

`interpret.factory` module implements Factory design pattern. `InstrFactory` class has dictionary to map opcode name to the appropiate class of instruction. `create_instr` class method takes opcode string, searches dictionary using that opcode for appropiate class of instruction and then runs constructor on that class to create instruction object and return it the the caller.

Factory design pattern helped me with creation of instruction objects and worked best for my script stucture.

### STACK extension

Implementation includes `STACK` extension - stack instructions are included in module `interpret.instruction`. These instructions work with inrepteters methods `datastack_push` and `datastack_pop` to get / store data. Other than that, they perform calculations in pretty same manner as non-stack instructions.

### Generic info

Program exits immediately if invalid data / code are inputed to the script. See `utils.error` module.
