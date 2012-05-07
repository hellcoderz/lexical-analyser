from constants import *

class FiniteStateMachine:

    def __init__(self, STATE_SIZE, SYMBOL_SIZE):

        self.transitions = []
        for i in range(STATE_SIZE):
            l = []
            for j in range(SYMBOL_SIZE):
                l.append((None))
            self.transitions.append(l)

    def set_input(self, inp):
        self.stack = list(inp)
        self.stack.reverse()

    def add_transition(self, start, symbol, destination, arg):
        self.transitions[start][symbol] = (destination, arg)

    def get_transition(self, start, symbol):
        return self.transitions[start][symbol]

    def pop(self):
        return self.stack.pop()

    def next(self):

        if self.state == State.ACCEPT:
            #print 'FSM: In ACCEPT, Stop iter'
            raise StopIteration

        try:
            next_symbol = self.stack[-1]
        except IndexError:
            next_symbol = Symbol.EPSILON

        if next_symbol == Symbol.BLANK:  # consume whitespace and restart machine
            #print 'FSM: Next symbol = BLANK'
            self.pop()
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
            raise FSMException

        self.state = dest
        accepted_symbol = self.pop() if (next_symbol != Symbol.EPSILON) else ''
        return (dest, arg, accepted_symbol)


class LexerFiniteStateMachine(FiniteStateMachine):

    def __iter__(self):
        self.state = State.START
        #print '=============='
        #print 'FSM IN : %s' % self.stack
        return self

    def set_input(self, string):
        self.input = list(string)
        self.input.reverse()

        self.stack = []
        for char in self.input:
            self.stack.append(self.get_symbol(char))

    def pop(self):

        self.stack.pop()
        return self.input.pop()

    def get_symbol(self, char):

        if char == '':
            return Symbol.EPSILON
        elif char in ' \t':
            return Symbol.BLANK
        elif char in '0123456789':
            return Symbol.DIGIT
        elif char in 'abcdfghijklmnopqrstuvwxyzABCDFGHIJKLMNOPQRSTUVWXYZ_':  # without E
            return Symbol.ALPHA
        elif char in '.,':
            return Symbol.DOT
        elif char in 'eE':
            return Symbol.E
        elif char in '+':
            return Symbol.OP_PLUS
        elif char in '-':
            return Symbol.OP_MINUS
        elif char in '*':
            return Symbol.OP_MUL
        elif char in '/':
            return Symbol.OP_DIV
        elif char in '^':
            return Symbol.OP_POW
        elif char in '=':
            return Symbol.OP_ASSIGN
        elif char in '(':
            return Symbol.OP_LPAREN
        elif char in ')':
            return Symbol.OP_RPAREN
        else:
            raise FSMException
