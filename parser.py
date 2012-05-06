from lexical_analyzer import *
import sys


class Parser:

    @classmethod
    def ParseInputString(cls, input_str):
        lexer_ = LexicalAnalyzer()
        lexer_.SetInputString(input_str)

        token = Token.ERROR

        while True:
            token = lexer_.Lex()
            if (token == Token.ERROR):
                cls.OnLexerError()
            else:
                cls.OnShift(token, lexer_.GetTokenString(), 0)

            if (token == Token.ERROR) or (token == Token.EOS):
                break

        if token != Token.ERROR:
            cls.OnAccept()

        return token == Token.EOS

    @classmethod
    def OnShift(cls, token, token_string, next_state):
        sys.stdout.write(' S%s[%s:%s]' % (next_state, token, token_string))
        return True

    @classmethod
    def OnReduce(cls, rule, next_state):
        sys.stdout.write(' R%s,%s' % (rule, next_state))
        return True

    @classmethod
    def OnAccept(cls):
        sys.stdout.write(" **\n")

    @classmethod
    def OnParseError(cls):
        sys.stdout.write(' ParseError\n')

    @classmethod
    def OnLexerError(cls):
        sys.stdout.write(' LexerError\n')
