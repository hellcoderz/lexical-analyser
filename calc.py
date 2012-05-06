#!/usr/bin/python

import sys

from parser import Parser


def main(argv=None):
    if argv is None:
        argv = sys.argv

    # get user input
    while True:

        try:
            input_str = raw_input('> ')
        except EOFError:
            break
        except KeyboardInterrupt:
            print ''
            break

        print "input: '" + input_str + "'"

        Parser.ParseInputString(input_str)

    return 0


if __name__ == "__main__":
    sys.exit(main())
