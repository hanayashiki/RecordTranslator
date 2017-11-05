class Printer:
    tg_file = open("text.txt", 'w+')
    last_quad = ("", 0, 0, 0, 0)

    def dump(self, str_operator, sym_source_1, sym_source_2, sym_output):
        self.last_quad = (str_operator, sym_source_1.addr, sym_source_2.addr, sym_output.addr)
        print(str_operator+' '+str(sym_source_1.addr)+' '+str(sym_source_2.addr)\
              + ' ' + str(sym_output.addr))

    def emit(self, *list):
        for entry in list:
            print(str(entry)+" ", end='')
        print("")
