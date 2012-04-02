def enum(**enums):
    return type('Enum', (), enums)

from collections import deque

Token = enum(
        ERROR = -1,
        EOS = 'EOS', # End-Of-String
    )

Symbols = enum(
        DIGIT = '0123456789',
        ALPHA = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        DOT = '.',
        E = 'eE',
        PLUS = '+',
        MINUS = '-',
        TIMES = '*',
        DIVIDE = '/',
        POWER = '^',
        EQUAL = '=',
        SPACE = ' ',
        LEFT_PARENTHESIS = '(',
        RIGHT_PARENTHESIS = ')',
    )

class LexicalAnalyzer:

    _token_string = None #Detected string for the current token.
    _stack = None

    # SetInputString sets the input string for lexical analysis.
    def SetInputString(self, input_string):
        self._stack = deque(list(input_string))

    # Lex function returns the next token from the input string.
    # The detected token string is stored until the next Lex is called.
    def Lex(self):

        try:
            char = self._stack.popleft()
        except IndexError: # stack is empty -> empty string or EOS
            self._token_string = ''
            return Token.EOS

        return Token.ERROR

    # GetTokenString returns the character string for the detected token.
    def GetTokenString(self):
        return self._token_string
