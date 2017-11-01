"""
design

    syntax:
        <record> -> 'TYPE' id '=' 'RECORD' <comp_list> 'END' ';'
        <comp_list> -> <comp> <comp_tail>
        <comp_tail> -> ';' <comp> <comp_tail>
        <comp_tail> -> ""
        <comp> -> id : ctype

    translation:
        <record> -> 'TYPE' id(output record_name) '=' 'RECORD' <comp_list>(output comp_dict)
            @insert_sym(input record_name, input comp_dict) 'END' ';'
        <comp_list>(output comp_dict)  -> @comp_dict={} <comp>(output comp_name, output comp_type)
            @comp_dict[comp_name]=comp_type <comp_tail>(input comp_dict)
        <comp_tail>(input comp_dict) -> ';' <comp>(output comp_name, output comp_type)
            @comp_dict[comp_name]=comp_type <comp_tail>
        <comp>(output comp_name, output comp_type) -> id(output comp_name) : ctype(output comp_type)

"""

from syntax import *
from symboller import *
from printer import *
from type_def import *


class Syntax_Record(Syntax):

    def parse_record(self, file_addr):
        self.lexer_obj = Lexer(file_addr)
        self.lexer_obj.getsym()
        self.exprs()

    def exprs(self):
        while self.lexer_obj.token == "TYPE":
            self.record()

    def record(self):
        record_name = "UnknowName"

        if self.lexer_obj.token == "TYPE":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

        if self.lexer_obj.symbol == "ID":
            record_name = self.lexer_obj.token
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

        if self.lexer_obj.symbol == "EQ":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

        if self.lexer_obj.token == "RECORD":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

        comp_dict = self.comp_list()

        self.insert_sym(record_name, comp_dict)

        if self.lexer_obj.token == "END":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

        if self.lexer_obj.symbol == "SEMI":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

    def comp_list(self):
        comp_dict = {}
        comp_name, comp_type = self.comp()
        comp_dict[comp_name] = comp_type

        self.comp_tail(comp_dict)
        return comp_dict

    def comp(self):
        comp_name = "UnknownName"
        comp_type = None
        # id
        if self.lexer_obj.symbol == "ID":
            comp_name = self.lexer_obj.token
            # print("got comp_name:"+comp_name)
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

        #:
        if self.lexer_obj.symbol == "COLON":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE, self.lexer_obj.symbol, self.lexer_obj.token)

        # ctype
        comp_type = self.ctype()

        return comp_name, comp_type

    def ctype(self):
        get_type = None
        if self.lexer_obj.symbol == "ID":
            if self.lexer_obj.token in name2size:
                get_type = SimpleType(self.lexer_obj.token)
                self.lexer_obj.getsym()
            else:
                # TODO: array, record
                raise Exception(SE, "Type Not Found: " + self.lexer_obj.token)

        return get_type

    def comp_tail(self, comp_dict):
        """
        <comp_tail>(input comp_dict) -> ';' <comp>(output comp_name, output comp_type)
            @comp_dict[comp_name]=comp_type <comp_tail>
        <comp_tail> -> ""
        """
        if self.lexer_obj.symbol == "SEMI":
            self.lexer_obj.getsym()
            comp_name, comp_type = self.comp()
            comp_dict[comp_name] = comp_type
            self.comp_tail(comp_dict)
        else:
            pass

    def insert_sym(self, record_name, record_dict):
        record_type = RecordType(record_dict)
        record_sym = self.tokener_obj.new_sym(record_name)
        record_sym.stype = record_type
        print(record_type)
