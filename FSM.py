from constants import *

class FiniteStateMachine:

    def __init__(self, STATE_SIZE, SYMBOL_SIZE):

        self.transitions = []
        for i in range(STATE_SIZE):
            l = []
            for j in range(SYMBOL_SIZE):
                l.append((None))
            self.transitions.append(l)

    def set_input(self, string):
        self.input = list(string)
        self.input.reverse()

    def add_transition(self, start, symbol, destination, arg):
        self.transitions[start][symbol] = (destination, arg)

    def get_transition(self, start, symbol):
        return self.transitions[start][symbol]

    def get_next_symbol(self):
        try:
            next_char = self.input[-1]
        except IndexError:
            return Symbol.EPSILON

        if next_char == '':
            return Symbol.EPSILON
        elif next_char in ' \t':
            return Symbol.BLANK
        elif next_char in '0123456789':
            return Symbol.DIGIT
        elif next_char in 'abcdfghijklmnopqrstuvwxyzABCDFGHIJKLMNOPQRSTUVWXYZ_':  # without E
            return Symbol.ALPHA
        elif next_char in '.,':
            return Symbol.DOT
        elif next_char in 'eE':
            return Symbol.E
        elif next_char in '+':
            return Symbol.OP_PLUS
        elif next_char in '-':
            return Symbol.OP_MINUS
        elif next_char in '*':
            return Symbol.OP_MUL
        elif next_char in '/':
            return Symbol.OP_DIV
        elif next_char in '^':
            return Symbol.OP_POW
        elif next_char in '=':
            return Symbol.OP_ASSIGN
        elif next_char in '(':
            return Symbol.OP_LPAREN
        elif next_char in ')':
            return Symbol.OP_RPAREN
        else:
            raise LexerException

    def __iter__(self):
        self.state = State.START
        #print '=============='
        #print 'FSM IN : %s' % self.input
        return self

    def next(self):

        if self.state == State.ACCEPT:
            #print 'FSM: In ACCEPT, Stop iter'
            raise StopIteration


        next_symbol = self.get_next_symbol()
        if next_symbol == Symbol.BLANK:  # consume whitespace and restart machine
            #print 'FSM: Next symbol = BLANK'
            self.input.pop()
            raise StopIteration
        else:
            #print 'FSM: Next symbol = %s' % next_symbol
            try:
                (dest, arg) = self.get_transition(self.state, next_symbol)
            except TypeError:  # returned None, stop machine here
                #print 'FSM: No destination set for state %s and symbol %s, Stop Iteration' % (self.state, next_symbol)
                raise StopIteration

        #print 'FSM : In state %s with symbol %s, got to %s with arg %s' % (self.state, next_symbol, dest, arg)

        if dest == State.ERROR:
            #print 'FSM : In State.ERROR'
            raise LexerException

        self.state = dest

        accepted_token = arg
        accepted_token_string = self.input.pop() if (next_symbol != Symbol.EPSILON) else ''

        return (accepted_token, accepted_token_string)