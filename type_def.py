from symboller import *

name2size = {
    "INTEGER": 2,
    "REAL": 6,
    "BOOLEAN": 1,
    "CHAR": 1,
}


class SimpleType:
    global name2size

    name = "UnknownType"
    size = 0

    def __init__(self, name):
        self.name = name
        self.size = name2size[name]

    def __str__(self):
        return ("{type: " + self.name + ", " + "size: "+ str(self.size) + "}")


class ArrayType:
    atype = None
    size = 0
    dimensions = []

    def __init__(self, atype, dimensions):
        self.atype = atype
        self.dimensions = dimensions
        self.size = atype.size
        for d in dimensions:
            self.size *= d



class RecordType:
    comp_list = None

    def __init__(self, comp_dict):
        self.comp_list = []
        offset = 0
        for comp_name, comp_type in comp_dict.items():
            comp_list_entry = Symbol()
            comp_list_entry.token = comp_name
            comp_list_entry.stype = comp_type
            comp_list_entry.addr = offset
            self.comp_list.append(comp_list_entry)
            offset += comp_list_entry.stype.size

    def __str__(self):
        show = ""
        for comp in self.comp_list:
            show += comp.token + ":"
            show += str(comp.stype) + " @"
            show += str(comp.addr)
            show += "\n"
        return show