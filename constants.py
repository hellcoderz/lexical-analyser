def enum(**enums):
    return type('Enum', (), enums)


State = enum(
            ACCEPT = -2,
            ERROR = -1,
            START = 0,
            ID = 1,
            FLOAT = 2,
            INT = 3,
            SCI_E = 4,
            SCI_E_SIGNED = 5,
            REAL = 6,
            DOT = 7
        )
STATE_SIZE = 10

Symbol = enum(
            BLANK = 1,
            EPSILON = 2,
            DIGIT = 3,
            ALPHA = 4,  # WITHOUT E
            DOT = 5,
            E = 6,
            OP_PLUS = 7,
            OP_MINUS = 8,
            OP_MUL = 9,
            OP_DIV = 10,
            OP_POW = 11,
            OP_ASSIGN = 12,
            OP_LPAREN = 13,
            OP_RPAREN = 14
        )
SYMBOL_SIZE = 15

Token = enum(
        ERROR = -1,
        EOS = 0,
        ID = 1,
        NUMBER = 2,
        OP_PLUS = 10,
        OP_MINUS = 11,
        OP_MUL = 12,
        OP_DIV = 13,
        OP_POW = 14,
        OP_ASSIGN = 15,
        OP_LPAREN = 16,
        OP_RPAREN = 17,
        CMD_EXIT = 20,
        CMD_LIST = 21,
        CMD_CLEAR = 22
    )


class LexerException(Exception):
    pass