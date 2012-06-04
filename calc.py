#!/usr/bin/python

import sys
from constants import *
from calculator import Calculator
from variable_table import VariableTable

def main(argv=None):
    if argv is None:
        argv = sys.argv

    variable_table = VariableTable()
    calculator = Calculator(variable_table)

    # get user input
    while True:

        try:
            input_str = raw_input('> ')
        except EOFError:
            break
        except KeyboardInterrupt:
            print ''
            break

        #print "input: '" + input_str + "'"

        try:
            print calculator.run(input_str)
        except UndefinedVariableException as e:
            print 'Undefined variable: %s' % e
        except ParserException:
            print 'Parser error'
        except LexerException:
            print 'Lexer error'
        except ExitCMD:
            return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
