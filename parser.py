from lexical_analyzer import *
import sys

Terminal = enum(
                S = 0,
                E = 1,
                T = 2,
                F = 3,
                B = 4
                )

Action = enum(
            S = 'S',
            R = 'R',
            ACCEPT = 'A'
            )

STATES_COUNT = 33
TOKEN_COUNT = 23
TERMINAL_COUNT = 5
RULES_COUNT = 18 + 1  # index from 1


class ParsingTable:

    def __init__(self):

        self.actions = []
        for i in range(STATES_COUNT):
            self.actions.append([])
            for j in range(TOKEN_COUNT):
                self.actions[i].append(None)

        self.gotos = []
        for k in range(STATES_COUNT):
            self.gotos.append([])
            for l in range(TERMINAL_COUNT):
                self.gotos[k].append(None)

        self.lhs = []
        for m in range(RULES_COUNT):
            self.lhs.append(None)

        self.rhs = []
        for n in range(RULES_COUNT):
            self.rhs.append(None)

    def add_action(self, current_state, token, action, action_arg):
        self.actions[current_state][token] = (action, action_arg)

    def add_goto(self, current_state, nonterminal, next_state):
        self.gotos[current_state][nonterminal] = next_state

    def add_lhs(self, rule, nonterminal):
        self.lhs[rule] = nonterminal

    def add_rhs(self, rule, symbol_count):
        self.rhs[rule] = symbol_count

    def get_action(self, current_state, token):
        return self.actions[current_state][token]

    def get_goto(self, current_state, nonterminal):
        return self.gotos[current_state][nonterminal]

    def get_lhs(self, rule):
        return self.lhs[rule]

    def get_rhs(self, rule):
        return self.rhs[rule]

    def __str__(self):
        str = '### ACTION TABLE ### \n\n'
        str += '____|'
        for k in range(TOKEN_COUNT):
            str += '  %02d |' % k

        str += '\n'

        for m in range(TERMINAL_COUNT):
            str += '  %02d |' % m

        str += '\n'

        for i in range(STATES_COUNT):
            str += ' %02d |' % i
            for j in range(len(self.actions[i])):
                if self.actions[i][j] == None:
                    str += '     |'
                else:
                    str += ' %s%02d |' % self.actions[i][j]

            str += '|'

            for l in range(len(self.gotos[i])):
                if self.gotos[i][l] == None:
                    str += '     |'
                else:
                    str += '  %02d |' % self.gotos[i][l]

            str += '\n'

        str += '\n\n### RHS ###\n\n'

        for n in range(RULES_COUNT):
            if n == 0:
                continue
            str += '%02d -> %d terms\n' % (n, self.rhs[n])

        str += '\n\n### LHS ###\n\n'

        for o in range(RULES_COUNT):
            if o == 0:
                continue
            str += '%02d -> %d\n' % (o, self.lhs[o])

        return str


class Parser:

    def __init__(self):

        t = ParsingTable()

        t.add_action(0, Token.ID, Action.S, 3)
        t.add_action(0, Token.NUMBER, Action.S, 10)
        t.add_action(0, Token.CMD_EXIT, Action.S, 2)
        t.add_action(0, Token.CMD_LIST, Action.S, 2)
        t.add_action(0, Token.CMD_CLEAR, Action.S, 2)
        t.add_action(0, Token.PLUS, Action.S, 8)
        t.add_action(0, Token.MINUS, Action.S, 9)
        t.add_action(0, Token.EOS, Action.S, 1)

        t.add_action(1, Token.EOS, Action.ACCEPT, -1)

        t.add_action(2, Token.EOS, Action.R, 1)

        t.add_action(3, Token.EQUAL, Action.S, 12)
        t.add_action(3, Token.PLUS, Action.R, 16)
        t.add_action(3, Token.MINUS, Action.R, 16)
        t.add_action(3, Token.TIMES, Action.R, 16)
        t.add_action(3, Token.DIVIDE, Action.R, 16)
        t.add_action(3, Token.POWER, Action.R, 16)
        t.add_action(3, Token.RIGHT_PARENTHESIS, Action.R, 16)
        t.add_action(3, Token.EOS, Action.R, 16)

        t.add_action(4, Token.PLUS, Action.S, 13)
        t.add_action(4, Token.MINUS, Action.S, 14)
        t.add_action(4, Token.EOS, Action.R, 3)

        t.add_action(5, Token.PLUS, Action.R, 6)
        t.add_action(5, Token.MINUS, Action.R, 6)
        t.add_action(5, Token.TIMES, Action.S, 15)
        t.add_action(5, Token.DIVIDE, Action.S, 16)
        t.add_action(5, Token.RIGHT_PARENTHESIS, Action.R, 6)
        t.add_action(5, Token.EOS, Action.R, 6)

        t.add_action(6, Token.PLUS, Action.R, 9)
        t.add_action(6, Token.MINUS, Action.R, 9)
        t.add_action(6, Token.TIMES, Action.R, 9)
        t.add_action(6, Token.DIVIDE, Action.R, 9)
        t.add_action(6, Token.RIGHT_PARENTHESIS, Action.R, 9)
        t.add_action(6, Token.EOS, Action.R, 9)

        t.add_action(7, Token.PLUS, Action.R, 10)
        t.add_action(7, Token.MINUS, Action.R, 10)
        t.add_action(7, Token.TIMES, Action.R, 10)
        t.add_action(7, Token.DIVIDE, Action.R, 10)
        t.add_action(7, Token.POWER, Action.S, 17)
        t.add_action(7, Token.RIGHT_PARENTHESIS, Action.R, 10)
        t.add_action(7, Token.EOS, Action.R, 10)

        t.add_action(8, Token.ID, Action.S, 20)
        t.add_action(8, Token.NUMBER, Action.S, 10)
        t.add_action(8, Token.LEFT_PARENTHESIS, Action.S, 11)

        t.add_action(9, Token.ID, Action.S, 20)
        t.add_action(9, Token.NUMBER, Action.S, 10)
        t.add_action(9, Token.LEFT_PARENTHESIS, Action.S, 11)

        t.add_action(10, Token.PLUS, Action.R, 17)
        t.add_action(10, Token.MINUS, Action.R, 17)
        t.add_action(10, Token.TIMES, Action.R, 17)
        t.add_action(10, Token.DIVIDE, Action.R, 17)
        t.add_action(10, Token.POWER, Action.R, 17)
        t.add_action(10, Token.RIGHT_PARENTHESIS, Action.R, 17)
        t.add_action(10, Token.EOS, Action.R, 17)

        t.add_action(11, Token.ID, Action.S, 20)
        t.add_action(11, Token.NUMBER, Action.S, 10)
        t.add_action(11, Token.PLUS, Action.S, 8)
        t.add_action(11, Token.MINUS, Action.S, 9)
        t.add_action(11, Token.LEFT_PARENTHESIS, Action.S, 11)

        t.add_action(12, Token.ID, Action.S, 20)
        t.add_action(12, Token.NUMBER, Action.S, 10)
        t.add_action(12, Token.PLUS, Action.S, 8)
        t.add_action(12, Token.MINUS, Action.S, 9)
        t.add_action(12, Token.LEFT_PARENTHESIS, Action.S, 11)

        t.add_action(13, Token.ID, Action.S, 20)
        t.add_action(13, Token.NUMBER, Action.S, 10)
        t.add_action(13, Token.PLUS, Action.S, 8)
        t.add_action(13, Token.MINUS, Action.S, 9)
        t.add_action(13, Token.LEFT_PARENTHESIS, Action.S, 11)

        t.add_action(14, Token.ID, Action.S, 20)
        t.add_action(14, Token.NUMBER, Action.S, 10)
        t.add_action(14, Token.PLUS, Action.S, 8)
        t.add_action(14, Token.MINUS, Action.S, 9)
        t.add_action(14, Token.LEFT_PARENTHESIS, Action.S, 11)

        t.add_action(15, Token.ID, Action.S, 20)
        t.add_action(15, Token.NUMBER, Action.S, 10)
        t.add_action(15, Token.PLUS, Action.S, 8)
        t.add_action(15, Token.MINUS, Action.S, 9)
        t.add_action(15, Token.LEFT_PARENTHESIS, Action.S, 11)

        t.add_action(16, Token.ID, Action.S, 20)
        t.add_action(16, Token.NUMBER, Action.S, 10)
        t.add_action(16, Token.PLUS, Action.S, 8)
        t.add_action(16, Token.MINUS, Action.S, 9)
        t.add_action(16, Token.LEFT_PARENTHESIS, Action.S, 11)

        t.add_action(17, Token.ID, Action.S, 20)
        t.add_action(17, Token.NUMBER, Action.S, 10)
        t.add_action(17, Token.PLUS, Action.S, 8)
        t.add_action(17, Token.MINUS, Action.S, 9)
        t.add_action(17, Token.LEFT_PARENTHESIS, Action.S, 11)

        t.add_action(18, Token.PLUS, Action.R, 12)
        t.add_action(18, Token.MINUS, Action.R, 12)
        t.add_action(18, Token.TIMES, Action.R, 12)
        t.add_action(18, Token.DIVIDE, Action.R, 12)
        t.add_action(18, Token.POWER, Action.S, 28)
        t.add_action(18, Token.RIGHT_PARENTHESIS, Action.R, 12)
        t.add_action(18, Token.EOS, Action.R, 12)

        t.add_action(19, Token.PLUS, Action.R, 14)
        t.add_action(19, Token.MINUS, Action.R, 14)
        t.add_action(19, Token.TIMES, Action.R, 14)
        t.add_action(19, Token.DIVIDE, Action.R, 14)
        t.add_action(19, Token.POWER, Action.S, 29)
        t.add_action(19, Token.RIGHT_PARENTHESIS, Action.R, 14)
        t.add_action(19, Token.EOS, Action.R, 14)

        t.add_action(20, Token.PLUS, Action.R, 16)
        t.add_action(20, Token.MINUS, Action.R, 16)
        t.add_action(20, Token.TIMES, Action.R, 16)
        t.add_action(20, Token.DIVIDE, Action.R, 16)
        t.add_action(20, Token.POWER, Action.R, 16)
        t.add_action(20, Token.RIGHT_PARENTHESIS, Action.R, 16)
        t.add_action(20, Token.EOS, Action.R, 16)

        t.add_action(21, Token.PLUS, Action.S, 13)
        t.add_action(21, Token.MINUS, Action.S, 14)
        t.add_action(21, Token.RIGHT_PARENTHESIS, Action.S, 30)

        t.add_action(22, Token.PLUS, Action.S, 13)
        t.add_action(22, Token.MINUS, Action.S, 14)
        t.add_action(22, Token.EOS, Action.R, 2)

        t.add_action(23, Token.PLUS, Action.R, 4)
        t.add_action(23, Token.MINUS, Action.R, 4)
        t.add_action(23, Token.TIMES, Action.S, 15)
        t.add_action(23, Token.DIVIDE, Action.S, 16)
        t.add_action(23, Token.RIGHT_PARENTHESIS, Action.R, 4)
        t.add_action(23, Token.EOS, Action.R, 4)

        t.add_action(24, Token.PLUS, Action.R, 5)
        t.add_action(24, Token.MINUS, Action.R, 5)
        t.add_action(24, Token.TIMES, Action.S, 15)
        t.add_action(24, Token.DIVIDE, Action.S, 16)
        t.add_action(24, Token.RIGHT_PARENTHESIS, Action.R, 5)
        t.add_action(24, Token.EOS, Action.R, 5)

        t.add_action(25, Token.PLUS, Action.R, 7)
        t.add_action(25, Token.MINUS, Action.R, 7)
        t.add_action(25, Token.TIMES, Action.R, 7)
        t.add_action(25, Token.DIVIDE, Action.R, 7)
        t.add_action(25, Token.RIGHT_PARENTHESIS, Action.R, 7)
        t.add_action(25, Token.EOS, Action.R, 7)

        t.add_action(26, Token.PLUS, Action.R, 8)
        t.add_action(26, Token.MINUS, Action.R, 8)
        t.add_action(26, Token.TIMES, Action.R, 8)
        t.add_action(26, Token.DIVIDE, Action.R, 8)
        t.add_action(26, Token.RIGHT_PARENTHESIS, Action.R, 8)
        t.add_action(26, Token.EOS, Action.R, 8)

        t.add_action(27, Token.PLUS, Action.R, 15)
        t.add_action(27, Token.MINUS, Action.R, 15)
        t.add_action(27, Token.TIMES, Action.R, 15)
        t.add_action(27, Token.DIVIDE, Action.R, 15)
        t.add_action(27, Token.RIGHT_PARENTHESIS, Action.R, 15)
        t.add_action(27, Token.EOS, Action.R, 15)

        t.add_action(28, Token.ID, Action.S, 20)
        t.add_action(28, Token.NUMBER, Action.S, 10)
        t.add_action(28, Token.PLUS, Action.S, 8)
        t.add_action(28, Token.MINUS, Action.S, 9)
        t.add_action(28, Token.LEFT_PARENTHESIS, Action.S, 11)

        t.add_action(29, Token.ID, Action.S, 20)
        t.add_action(29, Token.NUMBER, Action.S, 10)
        t.add_action(29, Token.PLUS, Action.S, 8)
        t.add_action(29, Token.MINUS, Action.S, 9)
        t.add_action(29, Token.LEFT_PARENTHESIS, Action.S, 11)

        t.add_action(30, Token.PLUS, Action.R, 18)
        t.add_action(30, Token.MINUS, Action.R, 18)
        t.add_action(30, Token.TIMES, Action.R, 18)
        t.add_action(30, Token.DIVIDE, Action.R, 18)
        t.add_action(30, Token.POWER, Action.R, 18)
        t.add_action(30, Token.RIGHT_PARENTHESIS, Action.R, 18)
        t.add_action(30, Token.EOS, Action.R, 18)

        t.add_action(31, Token.PLUS, Action.R, 13)
        t.add_action(31, Token.MINUS, Action.R, 13)
        t.add_action(31, Token.TIMES, Action.R, 13)
        t.add_action(31, Token.DIVIDE, Action.R, 13)
        t.add_action(31, Token.RIGHT_PARENTHESIS, Action.R, 13)
        t.add_action(31, Token.EOS, Action.R, 13)

        t.add_action(32, Token.PLUS, Action.R, 15)
        t.add_action(32, Token.MINUS, Action.R, 15)
        t.add_action(32, Token.TIMES, Action.R, 15)
        t.add_action(32, Token.DIVIDE, Action.R, 15)
        t.add_action(32, Token.RIGHT_PARENTHESIS, Action.R, 15)
        t.add_action(32, Token.EOS, Action.R, 15)


        t.add_goto(0, Terminal.S, 1)
        t.add_goto(0, Terminal.E, 4)
        t.add_goto(0, Terminal.T, 5)
        t.add_goto(0, Terminal.F, 6)
        t.add_goto(0, Terminal.B, 7)

        t.add_goto(8, Terminal.B, 18)

        t.add_goto(9, Terminal.B, 19)

        t.add_goto(11, Terminal.E, 21)
        t.add_goto(11, Terminal.T, 5)
        t.add_goto(11, Terminal.F, 6)
        t.add_goto(11, Terminal.B, 7)

        t.add_goto(12, Terminal.E, 22)
        t.add_goto(12, Terminal.T, 5)
        t.add_goto(12, Terminal.F, 6)
        t.add_goto(12, Terminal.B, 7)

        t.add_goto(13, Terminal.T, 23)
        t.add_goto(13, Terminal.F, 6)
        t.add_goto(13, Terminal.B, 7)

        t.add_goto(14, Terminal.T, 24)
        t.add_goto(14, Terminal.F, 6)
        t.add_goto(14, Terminal.B, 7)

        t.add_goto(15, Terminal.F, 25)
        t.add_goto(15, Terminal.B, 7)

        t.add_goto(16, Terminal.F, 26)
        t.add_goto(16, Terminal.B, 7)

        t.add_goto(17, Terminal.F, 27)
        t.add_goto(17, Terminal.B, 7)

        t.add_goto(28, Terminal.F, 31)
        t.add_goto(28, Terminal.B, 7)

        t.add_goto(29, Terminal.F, 32)
        t.add_goto(29, Terminal.B, 7)

        t.add_rhs(1, 1)
        t.add_rhs(2, 3)
        t.add_rhs(3, 1)
        t.add_rhs(4, 3)
        t.add_rhs(5, 3)
        t.add_rhs(6, 1)
        t.add_rhs(7, 3)
        t.add_rhs(8, 3)
        t.add_rhs(9, 1)
        t.add_rhs(10, 1)
        t.add_rhs(11, 3)
        t.add_rhs(12, 2)
        t.add_rhs(13, 4)
        t.add_rhs(14, 2)
        t.add_rhs(15, 4)
        t.add_rhs(16, 1)
        t.add_rhs(17, 1)
        t.add_rhs(18, 3)

        t.add_lhs(1, Terminal.S)
        t.add_lhs(2, Terminal.S)
        t.add_lhs(3, Terminal.S)
        t.add_lhs(4, Terminal.E)
        t.add_lhs(5, Terminal.E)
        t.add_lhs(6, Terminal.E)
        t.add_lhs(7, Terminal.T)
        t.add_lhs(8, Terminal.T)
        t.add_lhs(9, Terminal.T)
        t.add_lhs(10, Terminal.F)
        t.add_lhs(11, Terminal.F)
        t.add_lhs(12, Terminal.F)
        t.add_lhs(13, Terminal.F)
        t.add_lhs(14, Terminal.F)
        t.add_lhs(15, Terminal.F)
        t.add_lhs(16, Terminal.B)
        t.add_lhs(17, Terminal.B)
        t.add_lhs(18, Terminal.B)

        # print t

        self.table = t

    def ParseInputString(self, input_str):

        self.init_stack()

        lexer_ = LexicalAnalyzer()
        lexer_.SetInputString(input_str)

        token = Token.ERROR

        error = False
        accepted = False

        while (not error and not accepted):
            token = lexer_.Lex()
            if (token == Token.ERROR):
                cls.OnLexerError()
                break
            else:

                while True:

                    try:
                        (action, arg) = self.table.get_action(self.current_state, token)
                    except TypeError:  # probably returned None
                        error = True
                        break

                    if action == Action.S:

                        if arg == None:
                            error = True
                            break

                        self.push_state(arg)
                        self.OnShift(token, lexer_.GetTokenString(), arg)
                        break

                    elif action == Action.R:

                        if arg == None:
                            error = True
                            break

                        rhs = self.table.get_rhs(arg)
                        lhs = self.table.get_lhs(arg)

                        if lhs == None or rhs == None:
                            error = True
                            break

                        self.pop_states(rhs)

                        goto = self.table.get_goto(self.current_state, lhs)
                        if goto == None:
                            error = True
                            break

                        self.push_state(goto)
                        self.OnReduce(arg, goto)

                    elif action == Action.ACCEPT:
                        accepted = True
                        break
                    else:
                        error = True
                        break


        if error:
            self.OnParseError()
        elif accepted:
            self.OnAccept()

        return token == Token.EOS

    def init_stack(self):
        self.stack = [0]

    def push_state(self, state):
        self.stack.append(state)

    def pop_states(self, number):
        for i in range(number):
            self.stack.pop()

    @property
    def current_state(self):
        return self.stack[-1]

    def OnShift(self, token, token_string, next_state):
        sys.stdout.write(' S%s[%s:%s]' % (next_state, token, token_string))
        return True

    def OnReduce(self, rule, next_state):
        sys.stdout.write(' R%s,%s' % (rule, next_state))
        return True

    def OnAccept(self):
        sys.stdout.write(" **\n")

    def OnParseError(self):
        sys.stdout.write(' ParseError\n')

    def OnLexerError(self):
        sys.stdout.write(' LexerError\n')
