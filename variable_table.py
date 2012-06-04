from constants import UndefinedVariableException


class VariableTable():

    def __init__(self):
        self.clear()

    def set(self, ident, value):
        self.table[ident] = value

    def get(self, ident):
        try:
            return self.table[ident]
        except KeyError:
            raise UndefinedVariableException(ident)

    def clear(self):
        self.table = dict()
        return ''

    def list(self):
        return self.__str__()

    def __str__(self):
        s = ''
        for (ident, value) in self.table.iteritems():
            s += '%s = %s' % (ident, value)
            s += '\n'
        return s[:-1] if s != '' else ''
