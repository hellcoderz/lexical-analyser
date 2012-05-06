def enum(**enums):
    return type('Enum', (), enums)

Token = enum(
        ERROR = -1,
        EOS = 0,  # End-Of-String
        ID = 1,
        INT_NUMBER = 2,
        REAL_NUMBER = 2,
        PLUS = 10,
        MINUS = 11,
        TIMES = 12,
        DIVIDE = 13,
        POWER = 14,
        EQUAL = 15,
        LEFT_PARENTHESIS = 16,
        RIGHT_PARENTHESIS = 17,
        CMD_EXIT = 20,
        CMD_LIST = 21,
        CMD_CLEAR = 22
    )

Symbols = enum(
        BLANK = ' \t',
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
        CMD_EXIT = ['exit', 'quit'],
        CMD_LIST = 'list',
        CMD_CLEAR = 'clear'
    )


class LexicalAnalyzer:

    _token_string = None  # Detected string for the current token.
    _stack = None

    # SetInputString sets the input string for lexical analysis.
    def SetInputString(self, input_string):
        self._stack = list(input_string)
        self._stack.reverse()  # python does not have popleft so we reverse the list tu use pop.

    # Lex function returns the next token from the input string.
    # The detected token string is stored until the next Lex is called.
    def Lex(self):
        return self._state_start()

    # GetTokenString returns the character string for the detected token.
    def GetTokenString(self):
        return self._token_string

    def _peekNextChar(self):
        try:
            return self._stack[-1]
        except IndexError:  # stack is empty
            return ''

    def _popChar(self):
        try:
            return self._stack.pop()
        except IndexError:
            return ''

    def _state_start(self):

        char = self._token_string = self._popChar()

        if char == '':
            return Token.EOS

        if char in Symbols.BLANK:
            return self._state_start()  # restart FSM if we found a blank char

        elif char in Symbols.DIGIT:
            return self._state_int()

        elif char in Symbols.ALPHA:
            return self._state_id()

        elif char in Symbols.DOT:
            return self._state_float()

        elif char in Symbols.E:  # useless but here if we change the definition of E
            return self._state_id()

        elif char == Symbols.PLUS:
            return Token.PLUS

        elif char == Symbols.MINUS:
            return Token.MINUS

        elif char == Symbols.TIMES:
            return Token.TIMES

        elif char == Symbols.DIVIDE:
            return Token.DIVIDE

        elif char == Symbols.POWER:
            return Token.POWER

        elif char == Symbols.EQUAL:
            return Token.EQUAL

        elif char == Symbols.LEFT_PARENTHESIS:
            return Token.LEFT_PARENTHESIS

        elif char == Symbols.RIGHT_PARENTHESIS:
            return Token.RIGHT_PARENTHESIS

        else:
            return Token.ERROR

    def _state_id(self):

        char = self._peekNextChar()  # only look at the next char, don't unstack it

        if char == '':
            return self._parse_id()

        elif (char in Symbols.ALPHA) or (char in Symbols.DIGIT):
            self._token_string += char
            self._popChar()  # it's processed, we can delete it
            return self._state_id()

        elif char == Symbols.DOT:
            return Token.ERROR

        else:
            return self._parse_id()

    def _state_int(self):

        char = self._peekNextChar()

        if char == '':
            return Token.INT_NUMBER

        elif char in Symbols.DIGIT:
            self._token_string += char
            self._popChar()
            return self._state_int()

        elif char == Symbols.DOT:
            self._token_string += char
            self._popChar()
            return self._state_float()

        elif char in Symbols.E:
            self._token_string += char
            self._popChar()
            return self._state_sci_e()

        elif char in Symbols.ALPHA:
            return Token.ERROR

        else:
            return Token.INT_NUMBER

    def _state_float(self):

        char = self._peekNextChar()

        if char == '':
            return Token.REAL_NUMBER

        elif char in Symbols.DIGIT:  # that's a digit after the dot
            self._token_string += char
            self._popChar()
            return self._state_float()

        elif char in Symbols.E:
            self._token_string += char
            self._popChar()
            return self._state_sci_e()

        elif (char in Symbols.ALPHA) or (char == Symbols.DOT):
            return Token.ERROR

        else:
            return Token.REAL_NUMBER

    def _state_sci_e(self):

        char = self._peekNextChar()

        if char == '':
            return Token.ERROR

        elif char in Symbols.DIGIT:
            self._token_string += char
            self._popChar()
            return self._state_real()

        elif (char == Symbols.PLUS) or (char == Symbols.MINUS):
            self._token_string += char
            self._popChar()
            return self._state_sci_e_signed()

        else:
            return Token.ERROR

    def _state_sci_e_signed(self):

        char = self._peekNextChar()

        if char == '':
            return Token.ERROR

        elif char in Symbols.DIGIT:
            self._token_string += char
            self._popChar()
            return self._state_real()

        else:
            return Token.ERROR

    def _state_real(self):

        char = self._peekNextChar()

        if char == '':
            return Token.REAL_NUMBER

        elif char in Symbols.DIGIT:
            self._token_string += char
            self._popChar()
            return self._state_real()

        elif (char in Symbols.ALPHA) or (char == Symbols.DOT):
            return Token.ERROR

        else:
            return Token.REAL_NUMBER

    def _parse_id(self):
            if (self._token_string in Symbols.CMD_EXIT):
                return Token.CMD_EXIT
            elif self._token_string == Symbols.CMD_LIST:
                return Token.CMD_LIST
            elif self._token_string == Symbols.CMD_CLEAR:
                return Token.CMD_CLEAR
            else:
                return Token.ID
