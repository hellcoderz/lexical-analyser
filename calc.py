#!/usr/bin/python

import sys

from lexical_analyzer import *

def main(argv=None):
    if argv is None:
        argv = sys.argv

    lex = LexicalAnalyzer()

    # get user input
    while 1:

        try:
            input_str = raw_input('> ')
        except EOFError:
            break
        except KeyboardInterrupt:
            print ''
            break

        # Setup lexical analyzer
        lex.SetInputString(input_str)
        token = Token.ERROR

        while True:

            token = lex.Lex()

            if token == Token.ERROR:
                print "calc: lex error in '{0}'".format(input_str)
            else:
                print "calc: lex {0} - {1}".format(token, lex.GetTokenString())


            if (token == Token.ERROR or token == Token.EOS):
                break

    return 0


if __name__ == "__main__":
    sys.exit(main())