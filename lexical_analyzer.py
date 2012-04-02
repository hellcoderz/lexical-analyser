def enum(**enums):
    return type('Enum', (), enums)

from collections import deque

Token = enum(
        ERROR = -1,
        EOS = 0, # End-Of-String
    )

class LexicalAnalyzer:

    _token_string = None #Detected string for the current token.
    _stack = None

    # SetInputString sets the input string for lexical analysis.
    def SetInputString(self, input_string):
        return

    # Lex function returns the next token from the input string.
    # The detected token string is stored until the next Lex is called.
    def Lex(self):
        return Token.ERROR

    # GetTokenString returns the character string for the detected token.
    def GetTokenString(self):
        return self._token_string
