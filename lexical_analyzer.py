from constants import *
from FSM import LexerFiniteStateMachine


class LexicalAnalyzer:

    def __init__(self):

        self.machine = LexerFiniteStateMachine(STATE_SIZE, SYMBOL_SIZE)

        # in the form of : current_state, next_symbol, destination_state, accepted_token_so_far

        self.machine.add_transition(State.START, Symbol.EPSILON, State.ACCEPT, Token.EOS)
        self.machine.add_transition(State.START, Symbol.DIGIT, State.INT, Token.NUMBER)
        self.machine.add_transition(State.START, Symbol.ALPHA, State.ID, Token.ID)
        self.machine.add_transition(State.START, Symbol.DOT, State.DOT, None)
        self.machine.add_transition(State.START, Symbol.E, State.ID, Token.ID)
        self.machine.add_transition(State.START, Symbol.OP_PLUS, State.ACCEPT, Token.OP_PLUS)
        self.machine.add_transition(State.START, Symbol.OP_MINUS, State.ACCEPT, Token.OP_MINUS)
        self.machine.add_transition(State.START, Symbol.OP_MUL, State.ACCEPT, Token.OP_MUL)
        self.machine.add_transition(State.START, Symbol.OP_DIV, State.ACCEPT, Token.OP_DIV)
        self.machine.add_transition(State.START, Symbol.OP_POW, State.ACCEPT, Token.OP_POW)
        self.machine.add_transition(State.START, Symbol.OP_ASSIGN, State.ACCEPT, Token.OP_ASSIGN)
        self.machine.add_transition(State.START, Symbol.OP_LPAREN, State.ACCEPT, Token.OP_LPAREN)
        self.machine.add_transition(State.START, Symbol.OP_RPAREN, State.ACCEPT, Token.OP_RPAREN)

        self.machine.add_transition(State.ID, Symbol.EPSILON, State.ACCEPT, Token.ID)
        self.machine.add_transition(State.ID, Symbol.DIGIT, State.ID, Token.ID)
        self.machine.add_transition(State.ID, Symbol.ALPHA, State.ID, Token.ID)
        self.machine.add_transition(State.ID, Symbol.DOT, State.ERROR, None)
        self.machine.add_transition(State.ID, Symbol.E, State.ID, Token.ID)

        self.machine.add_transition(State.DOT, Symbol.EPSILON, State.ERROR, None)
        self.machine.add_transition(State.DOT, Symbol.DIGIT, State.FLOAT, Token.NUMBER)
        self.machine.add_transition(State.DOT, Symbol.ALPHA, State.ERROR, None)
        self.machine.add_transition(State.DOT, Symbol.DOT, State.ERROR, None)
        self.machine.add_transition(State.DOT, Symbol.E, State.ERROR, None)

        self.machine.add_transition(State.FLOAT, Symbol.EPSILON, State.ACCEPT, Token.NUMBER)
        self.machine.add_transition(State.FLOAT, Symbol.DIGIT, State.FLOAT, Token.NUMBER)
        self.machine.add_transition(State.FLOAT, Symbol.ALPHA, State.ERROR, None)
        self.machine.add_transition(State.FLOAT, Symbol.DOT, State.ERROR, None)
        self.machine.add_transition(State.FLOAT, Symbol.E, State.SCI_E, None)

        self.machine.add_transition(State.INT, Symbol.EPSILON, State.ACCEPT, Token.NUMBER)
        self.machine.add_transition(State.INT, Symbol.DIGIT, State.INT, Token.NUMBER)
        self.machine.add_transition(State.INT, Symbol.ALPHA, State.ERROR, None)
        self.machine.add_transition(State.INT, Symbol.DOT, State.FLOAT, Token.NUMBER)
        self.machine.add_transition(State.INT, Symbol.E, State.SCI_E, None)

        self.machine.add_transition(State.SCI_E, Symbol.EPSILON, State.ERROR, None)
        self.machine.add_transition(State.SCI_E, Symbol.DIGIT, State.REAL, Token.NUMBER)
        self.machine.add_transition(State.SCI_E, Symbol.ALPHA, State.ERROR, None)
        self.machine.add_transition(State.SCI_E, Symbol.DOT, State.ERROR, None)
        self.machine.add_transition(State.SCI_E, Symbol.E, State.ERROR, None)
        self.machine.add_transition(State.SCI_E, Symbol.OP_PLUS, State.SCI_E_SIGNED, None)
        self.machine.add_transition(State.SCI_E, Symbol.OP_MINUS, State.SCI_E_SIGNED, None)

        self.machine.add_transition(State.SCI_E_SIGNED, Symbol.EPSILON, State.ERROR, None)
        self.machine.add_transition(State.SCI_E_SIGNED, Symbol.DIGIT, State.REAL, Token.NUMBER)
        self.machine.add_transition(State.SCI_E_SIGNED, Symbol.ALPHA, State.ERROR, None)
        self.machine.add_transition(State.SCI_E_SIGNED, Symbol.DOT, State.ERROR, None)
        self.machine.add_transition(State.SCI_E_SIGNED, Symbol.E, State.ERROR, None)
        self.machine.add_transition(State.SCI_E_SIGNED, Symbol.OP_PLUS, State.ERROR, None)
        self.machine.add_transition(State.SCI_E_SIGNED, Symbol.OP_MINUS, State.ERROR, None)

        self.machine.add_transition(State.REAL, Symbol.EPSILON, State.ACCEPT, Token.NUMBER)
        self.machine.add_transition(State.REAL, Symbol.DIGIT, State.REAL, Token.NUMBER)
        self.machine.add_transition(State.REAL, Symbol.ALPHA, State.ERROR, None)
        self.machine.add_transition(State.REAL, Symbol.DOT, State.ERROR, None)
        self.machine.add_transition(State.REAL, Symbol.E, State.ERROR, None)

    def set_input(self, string):
        self.input = string
        try:
            self.machine.set_input(string)
        except FSMException:
            raise LexerException

    def __iter__(self):
        return self

    def next(self):

        token_string = ''
        token = None

        try:

            for (state, token, char) in self.machine:
                token_string += char

            if token == Token.ID:  # parse for reserved words
                if token_string in ['exit', 'quit']:
                    token = Token.CMD_EXIT
                elif token_string in ['clear']:
                    token = Token.CMD_CLEAR
                elif token_string in ['list']:
                    token = Token.CMD_LIST

            #print 'LEX : token %s in char "%s"' % (token, token_string)

            if token == None:  # skip blanks
                return self.next()
            else:
                return (token, token_string)

        except FSMException:
            raise LexerException
