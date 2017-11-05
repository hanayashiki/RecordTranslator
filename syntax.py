"""
design

    syntax:
        <record> -> 'TYPE' id '=' 'RECORD' <comp_list> 'END' ';'
        <comp_list> -> <comp> <comp_tail>
        <comp_tail> -> ';' <comp> <comp_tail>
        <comp_tail> -> ""
        <comp> -> id : type

    translation:
        <record> -> 'TYPE' id(output record_name) '=' 'RECORD' <comp_list>(output comp_dict)
            @insert_sym(input record_name, input comp_dict) 'END' ';'
        <comp_list>(output comp_dict)  -> @comp_dict={} <comp>(output comp_name, output comp_type)
            @comp_dict[comp_name]=comp_type <comp_tail>(input comp_dict)
        <comp_tail>(input comp_dict) -> ';' <comp>(output comp_name, output comp_type)
            @comp_dict[comp_name]=comp_type <comp_tail>
        <comp>(output comp_name, output comp_type) -> id(output comp_name) : type(output comp_type)

"""

from lexer import *
from symboller import *
from printer import *
from labeller import *

SE = "Syntax Error"


class Syntax:
    lexer_obj = Lexer("text.txt")
    tokener_obj = Symboller()
    printer_obj = Printer()
    labeller_obj = Labeller()

    def __init__(self):
        self.tokener_obj = Symboller()
        self.printer_obj = Printer()
        self.labeller_obj = Labeller()

    def parse(self, file_addr):
        self.lexer_obj = Lexer(file_addr)
        self.lexer_obj.getsym()
        self.expr()

    def expr(self):
        sym = self.term()
        sym_self = self.expr_tail(sym)
        return sym_self

    def expr_tail(self, sym):
        if self.lexer_obj.symbol != "ADD":
            return sym
        else:
            self.lexer_obj.getsym()
            sym_ = self.term()
            temp = self.tokener_obj.new_sym("%TEMP")
            self.printer_obj.dump("ADD", sym, sym_, temp)
            sym_self = self.expr_tail(temp)
            return sym_self

    def term(self):
        #print("term begins")
        sym = self.fact()
        sym_self = self.term_tail(sym)
        return sym_self

    def term_tail(self, sym):
        if self.lexer_obj.symbol != "MULT":
            #print("term_tail_1 begins")
            return sym
        else:
            #print("term_tail_2 begins")
            self.lexer_obj.getsym()
            sym_ = self.fact()
            temp = self.tokener_obj.new_sym("%TEMP")
            self.printer_obj.dump("MULT", sym, sym_, temp)
            sym_self = self.term_tail(temp)
            return sym_self

    def fact(self):
        if self.lexer_obj.symbol == "ID":
            sym = self.tokener_obj.new_sym(self.lexer_obj.token)
            self.lexer_obj.getsym()
            return sym
        elif self.lexer_obj.symbol == "LP":
            self.lexer_obj.getsym()
            sym_self = self.expr()
            if self.lexer_obj.symbol != "RP":
                raise Exception(SE, "missing )")
            self.lexer_obj.getsym()
            return sym_self
        else:
            raise Exception(SE)

    def push_i(self, i):
        self.printer_obj.emit("LOADI", i)

    def push(self, token):
        self.printer_obj.emit("LOAD", "(" + token + ")")

    def store_in(self):
        self.printer_obj.emit("STOREIN")

    def label_emit(self, label):
        self.printer_obj.emit(label + ':')

    def load_id(self, sym):
        self.printer_obj.emit("LOAD", sym.token)


