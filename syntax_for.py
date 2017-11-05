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
                    @ push(input addr) ':=' <expr> @store_in()
            d. stat_list
                <stat_list> -> @ dump_none() 'statements' ';'
            e. for_loop
                <for_loop> -> <for_head>(output end_label, output ret_label)
                                <rest_of_loop>(input end_label, input ret_label) ';'
                <for_head>(output end_label, output ret_label) ->
                    'for' @label_gen(output end_label)
                    id(output symbol) @look_up(input symbol, output addr) @ push(input addr)
                    ':=' <expr> @store_in()
                    'to' @label_gen(output ret_label)
                    @label_emit(ret_label)  # 校验开头
                    <expr> 'by' @load_id(input symbol) <expr> @add_and_cjump(input symbol, input end_label)  # 累加并条件跳转

                <rest_of_loop>(input end_label, input ret_label) ->
                    'do' <stat_list> 'end' 'for'
                    @ret_branch(ret_label) @label_emit(end_label)

"""



from syntax import *
from type_def import *
from syntax_record import *


class Syntax_For(Syntax_Record):
