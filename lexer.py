class Lexer:
    char = '\0'
    token = ""
    num = 0x33333334
    symbol = ""
    src = None
    srcpos = 0

    def __init__(self, file):
        try:
            self.src = open(file, "rb+")
        except Exception as e:
            print(e.__str__())

    def getchar(self):
        self.char = self.src.read(1).decode('utf-8')
        if self.char == "":
            #print ("EOF")
            self.char = "$"
        #print("getchar:" + self.char)
        #print("from srcpos:", self.srcpos)
        self.srcpos += 1

    def retract(self):
        #print("backchar:" + self.char)
        self.srcpos -= 1
        self.src.seek(-1, 1)
        #print("to srcpos:", self.srcpos)

    def getsym(self):
        self.token = ""
        self.getchar()
        while self.char == ' ' or self.char == '\t' or self.char == '\n' or self.char == '\r':
            self.getchar()
        if self.char == ";":
            self.symbol = "SEMI"
        elif self.char == "=":
            self.symbol = "EQ"
        elif self.char == ":":
            self.getchar()
            if self.char == "=":
                self.symbol = "ASSIGN"
            else:
                self.retract()
                self.symbol = "COLON"

        elif self.char == "+":
            self.symbol = "ADD"
        elif self.char == "*":
            self.symbol = "MULT"
        elif self.char == "(":
            self.symbol = "LP"
        elif self.char == ")":
            self.symbol = "RP"
        elif self.char.isalpha():
            tried = False
            self.symbol = "ID"
            self.token += self.char
            self.getchar()
            while self.char.isalpha() or self.char.isdigit():
                tried = True
                self.token += self.char
                self.getchar()
            self.retract()
        elif self.char.isnumeric():
            self.symbol = "INTEGER"
            self.token += self.char
            self.getchar()
            while self.char.isdigit():
                tried = True
                self.token += self.char
                self.getchar()
            self.retract()
            self.num = eval(self.token)
        elif self.char == "$":
            self.symbol = "EOF"
        else:
            raise Exception("Lexical Error", self.srcpos)

