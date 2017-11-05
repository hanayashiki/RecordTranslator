"""
    design:
        1. syntax
            a. id_definition (simplified)
                <id_def> -> 'VAR' <comp> ';'
            b. expression (simplified)
                <expr> -> integer
            c. assign
                <assign> ->  id ':=' <expr> ';'
            d. stat_list (simplified)
                <stat_list> -> 'statements' ';'
            e. for_loop
                <for_loop> -> <for_head> <rest_of_loop> ';'
                <for_head> -> 'for' id ':=' <expr> 'to' <expr> 'by' <expr>
                <rest_of_loop> -> 'do' <stat_list> 'end' 'for'

        2. translation
            a. id_definition
                <id_def> -> 'VAR' <comp>(output comp_name, output comp_type)
                    @insert_simple_sym(input comp_name, input comp_type)
            b. expression
                <expr> -> integer(output value) @push_i(input value)
            c. assign
                <assign> -> id(output symbol) @look_up(input symbol, output addr)
                    @ push(input symbol) ':=' <expr> @store_in()
            d. stat_list
                <stat_list> -> @ dump_none() 'statements' ';'
            e. for_loop
                <for_loop> -> <for_head>(output end_label, output ret_label)
                                <rest_of_loop>(input end_label, input ret_label) ';'
                <for_head>(output end_label, output ret_label) ->
                    'for' @label_gen(output end_label)
                    id(output symbol) @look_up(input symbol, output addr) @ push(input addr)
                    ':=' <expr> @store_in()
                    @jump_to_start # 第一次赋值后，立即跳到start_label
                    'to' @label_gen(output ret_label)
                    @label_emit(ret_label)  # 校验开头
                    <expr> 'by' @load_id(input symbol) <expr> @add_and_cjump(input symbol, input end_label)  # 累加并条件跳转
                    @label_emit(start_label)

                <rest_of_loop>(input end_label, input ret_label) ->
                    'do' <stat_list> 'end' 'for'
                    @ret_branch(ret_label) @label_emit(end_label)

"""



from syntax import *
from type_def import *
from syntax_record import *


class Syntax_For(Syntax_Record):

    def parse_for(self, file_addr):
        self.lexer_obj = Lexer(file_addr)
        self.lexer_obj.getsym()
        self.test_stats()

    def test_stats(self):
        if self.lexer_obj.token == "VAR":
            self.id_def()
            self.test_stats()
        elif self.lexer_obj.token == "for":
            self.for_loop()
            self.test_stats()
        elif self.lexer_obj.symbol == "ID":
            self.assign()
            self.test_stats()
        else:
            return

    def id_def(self):
        if self.lexer_obj.token == "VAR":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

        id_name, id_type = self.comp()
        id_sym = self.tokener_obj.new_sym(id_name)
        # TODO: debug offset
        id_sym.stype = id_type

        print("# defined: "+ str(id_sym))

        if self.lexer_obj.symbol == "SEMI":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

    def expr(self):
        """
        <expr> -> integer(output value) @push_i(input value)
        """
        if self.lexer_obj.symbol == "INTEGER":
            self.push_i(self.lexer_obj.num)
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)


    def assign(self):
        """
        <assign> -> id(output symbol) @look_up(input symbol, output addr)
                    @ push(input symbol) ':=' <expr> @store_in() ';'
        """
        if self.lexer_obj.symbol == "ID":
            sym = self.tokener_obj.fetch_sym(self.lexer_obj.token) # corresponds @look_up
            if not sym:
                raise Exception(SE, "Symbol not defined: "+self.lexer_obj.token)
            # addr = sym.addr
            self.push(self.lexer_obj.token) # @push
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

        if self.lexer_obj.symbol == "ASSIGN":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

        self.expr()
        self.store_in()

        if self.lexer_obj.symbol == "SEMI":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

    def stat_list(self):
        """
        <stat_list> -> @ dump_none() 'statements' ';'
        """
        self.printer_obj.emit("# do something")
        if self.lexer_obj.token == "statements":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

        if self.lexer_obj.symbol == "SEMI":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

    def for_loop(self):
        """
        <for_loop> -> <for_head>(output end_label, output ret_label)
                        <rest_of_loop>(input end_label, input ret_label) ';'
        """
        end_label, ret_label = self.for_head()
        self.rest_of_loop(end_label, ret_label)

    def for_head(self):
        """
        <for_head>(output end_label, output ret_label) ->
            'for' @label_gen(output end_label) @label_gen(output start_label)
            id(output symbol) @look_up(input symbol, output addr) @ push(input symbol)
            ':=' <expr> @store_in()
            @jump_to_start # 第一次赋值后，立即跳到start_label
            to' @label_gen(output ret_label)
            @label_emit(ret_label)  # 校验开头
            <expr> 'by' @load_id(input symbol) <expr> @add_and_cjump(input symbol, input end_label)  # 累加并条件跳转
            @label_emit(start_label)  # 校验开头
        :return: "end", "ret"
        """
        # for
        if self.lexer_obj.token == "for":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)
        # id
        end_label = self.labeller_obj.generate()
        start_label = self.labeller_obj.generate()
        id_token = "Unknown"
        if self.lexer_obj.symbol == "ID":
            id_token = self.lexer_obj.token
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

        symbol = self.tokener_obj.fetch_sym(id_token)
        if not symbol:
            raise Exception(SE, "Not defined: "+id_token)
        self.push(symbol.token)
        # :=
        if self.lexer_obj.symbol == "ASSIGN":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)
        # expr
        self.expr()
        self.store_in()

        self.printer_obj.emit("BR", start_label)

        # to
        if self.lexer_obj.token == "to":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

        ret_label = self.labeller_obj.generate()
        self.label_emit(ret_label)
        # expr
        self.expr()
        # by
        if self.lexer_obj.token == "by":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

        self.load_id(symbol)
        # expr
        self.expr()
        # @add_and_cjump
        self.add_and_cjump(symbol, end_label)

        self.label_emit(start_label)

        return end_label, ret_label

    def rest_of_loop(self, end_label, ret_label):
        if self.lexer_obj.token == "do":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)
        self.stat_list()
        if self.lexer_obj.token == "end":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

        if self.lexer_obj.token == "for":
            self.lexer_obj.getsym()
        else:
            raise Exception(SE)

        self.printer_obj.emit("BR", ret_label)
        self.label_emit(end_label)


    def add_and_cjump(self, symbol, end_label):
        self.printer_obj.emit("ADD")
        self.printer_obj.emit("STO", symbol.token)
        self.printer_obj.emit("BR<", end_label)



