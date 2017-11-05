class Symboller:
    next_addr = 1
    tmp_cnter = 0
    tkn2addr = {}
    syms = set()

    def __init__(self):
        self.next_addr = 1
        self.tmp_cnter = 0
        self.tkn2addr = {}
        self.syms = set()

    def new_sym(self, token):
        sym = Symbol()
        sym.token = token
        if sym not in self.syms:
            sym.addr = self.next_addr
            if sym.token.startswith("%"):
                sym.token = "%" + str(self.tmp_cnter)
                self.tmp_cnter += 1
            self.tkn2addr[sym.token] = sym.addr
            #print("get symbol: " + token)
            self.next_addr += + 1
            self.syms.add(sym)
            return sym
        else:
            sym.addr = self.tkn2addr[sym.token]
            return sym

    def fetch_sym(self, token):
        for sym in self.syms:
            if sym.token == token:
                return sym
        return None


class Symbol:
    token = "Default"
    addr = -1
    stype = None

    def __eq__(self, other):
        return self.token == other.token

    def __hash__(self):
        return self.token.__hash__()

    def __str__(self):
        string = self.token + ": " + str(self.stype)
        return string