from syntax import *
import sys

if __name__ == '__main__':
    syntax_obj = Syntax()
    syntax_obj.parse(sys.argv[1])