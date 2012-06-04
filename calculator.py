from __future__ import division
from constants import *
from parser import Parser


class Calculator():

    def __init__(self, variable_table):
        self.variable_table = variable_table
        self.parser = Parser()
        self.stack = []

    def run(self, input_str):

        self.stack = []
        parser_generator = self.parser.parseIntputString(input_str)

        for (action, arg1, arg2) in parser_generator:

            if action == Action.S:
                self.stack.append(arg1)
            else:  # action == Action.R
                reduced_args = []
                for i in range(0, arg2):
                    reduced_args.append(self.stack.pop())
                reduced_args.reverse()

                self.stack.append(getattr(self, 'R' + str(arg1))(*reduced_args))

        return self.stack[0]

    def R1(self, cmd):
        print cmd
        if cmd == 'clear':
            return self.variable_table.clear()
        elif cmd == 'list':
            return self.variable_table.list()
        else:
            raise ExitCMD()
            pass

    def R2(self, ident, equal, E):
        self.variable_table.set(ident, E)
        S = '%s = %s' % (ident, E)
        return S

    def R3(self, E):
        S = E
        return S

    def R4(self, E, plus, T):
        E = E + T
        return E

    def R5(self, E, minus, T):
        E = E - T
        return E

    def R6(self, T):
        E = T
        return E

    def R7(self, T, mul, F):
        print T, mul, F
        T = T * F
        return T

    def R8(self, T, div, F):
        T = T / F
        return T

    def R9(self, F):
        T = F
        return T

    def R10(self, B):
        T = B
        return T

    def R11(self, B, power, F):
        F = B ** F
        return F

    def R12(self, plus, B):
        F = B
        return F

    def R13(self, plus, B, power, F):
        F = B ** F
        return F

    def R14(self, minus, B):
        F = - B
        return F

    def R15(self, minus, B, power, F):
        F = - (B ** F)
        return F

    def R16(self, ident):
        B = self.variable_table.get(ident)
        return B

    def R17(self, num):

        num = num.lower()

        if 'e' in num:

            l = num.split('e')
            lhs = float(l[0]) if '.' in l[0] else int(l[0])

            rhs = l[1]
            if rhs.startswith('-'):
                rhs = - int(rhs[1:])
            elif rhs.startswith('+'):
                rhs = int(rhs[1:])
            else:
                rhs = int(rhs)
            B = lhs * 10 ** rhs

        elif '.' in num:
            B = float(num)
        else:
            B = int(num)

        return B

    def R18(self, lparen, E, rparen):
        B = E
        return B
