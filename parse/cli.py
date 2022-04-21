## @package cli
#  Parse arguments from CLI.

import utils.error as error

import argparse

## Create argument parser with settings.
#  @details Argument options along with help messages
#           are set.
#  @return Created parser.
def create_argparser():
  arg_parser = argparse.ArgumentParser()
  arg_parser.add_argument("--source", help="XML source code")
  arg_parser.add_argument("--input", help="input values file")
  return arg_parser

## Get parsed arguments from CLI.
#  @details Exits with error code when argument is invalid or missing.
#           Also exits with 0 code with -h argument entered.
#  @return Object of arguments.
def get_args():
  argparser = create_argparser()
  try:
    args = argparser.parse_args()
  except SystemExit as e:
    # -h arg exits with 0 code
    exit(0) if not e.code else exit(error.CLIARG_ERROR)
  
  # at least one must be entered
  if not args.source and not args.input:
    error.error_exit(error.CLIARG_ERROR,
                     "Either source code or input file must be entered")

  return args
