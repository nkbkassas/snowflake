from lexeme import *

class Lexer:

    def __init__(self,filename):
        self.tokens = []
        self.filename = filename
        self.readFile = False
        self.currentCh = self.generateCh()
        self.saved = None 
        self.linenum = 0
        self.colnum = 0

    #Generate characters one by one 

    def generateCh(self):
        self.linenum = 0
        for line in open(self.filename):
            self.linenum += 1
            self.colnum = 0
            for ch in line:
                self.colnum += 1
                yield ch

   #Retreive next unparsed character

    def getNextCh(self):
        try:
            return next(self.currentCh) 
        except StopIteration:
            return None

    #Lex a number

    def lexNumber(self):
        num = self.saved
        ch = self.getNextCh()
        while ch.isdigit():
            num += ch
            ch = self.getNextCh()
        self.saved = ch
        num = int(num)
        return Lexeme(num, "INTEGER", self.linenum, self.colnum)

    #Lex a string

    def lexString(self):
        string = ""
        ch = self.getNextCh()
        while ch != '"':
            string += ch
            ch = self.getNextCh()
        self.saved = self.getNextCh()
        return Lexeme(string, "STRING", self.linenum, self.colnum)


    #Lex variable or keyword

    def lexNames(self):
        name = self.saved
        ch = self.getNextCh()
        while ch.isdigit() or ch.isalpha() or ch == "_" or ch == "!":
            name += ch
            ch = self.getNextCh()
        self.saved = ch
        if name == "snowflake":
            return Lexeme(name, "snowflake", self.linenum, self.colnum)
        elif name == "if":
            return Lexeme(name, "if", self.linenum, self.colnum)
        elif name == "elif":
            return Lexeme(name, "elif", self.linenum, self.colnum)
        elif name == "else":
            return Lexeme(name, "else", self.linenum, self.colnum)
        elif name == "cycle":
            return Lexeme(name, "cycle", self.linenum, self.colnum)
        elif name == "form":
            return Lexeme(name, "form", self.linenum, self.colnum)
        elif name == "freeze":
            return Lexeme(name, "freeze", self.linenum, self.colnum)
        elif name == "snowball":
            return Lexeme(name, "snowball", self.linenum, self.colnum)
        else:
            return Lexeme(name, "var", self.linenum, self.colnum)


    def skipAllWhiteSpace(self):
        if self.saved == None:
            ch = self.getNextCh()
        else:
            ch = self.saved 
        while ch == "\n" or ch == "\t" or ch == " " or ch == "~":
            if ch == "~":
                self.skipComment()
            ch = self.getNextCh()
        self.saved = ch
        
    def skipComment(self):
        comment = "~"
        comment += self.getNextCh()
        comment += self.getNextCh()
        comment += self.getNextCh()
        comment += self.getNextCh()
        if comment == "~*X*~":
            ch = self.getNextCh()
            while ch != "\n":
                ch = self.getNextCh()
        else:
            print("Invalid comment syntax. You used: ", comment, " should be: ~*X*~", "on line ", self.linenum)


    #Lexer

    def lex(self):
        self.skipAllWhiteSpace()
        c = self.saved
        if c == None: 
            return None
        elif c == "*":
            self.saved = None
            return Lexeme(c, "STAR", self.linenum, self.colnum)
        elif c == "(":
            self.saved = None
            return Lexeme(c, "OPAREN", self.linenum, self.colnum)
        elif c == ")":
            self.saved = None
            return Lexeme(c, "CPAREN", self.linenum, self.colnum)
        elif c == ":":
            self.saved = None
            return Lexeme(c, "COLON", self.linenum, self.colnum)
        elif c == ";":
            self.saved = None
            return Lexeme(c, "SEMICOLON", self.linenum, self.colnum)
        elif c == ",":
            self.saved = None
            return Lexeme(c, "COMMA", self.linenum, self.colnum)
        elif c.isdigit() or c == "+" or c == "-":
            return self.lexNumber()
        elif c.isalpha() or c == "!" or c == "_":
            return self.lexNames()
        elif c == '"':
            return self.lexString()
        else:
            print("Token ", c, "  not recognized", self.linenum, self.colnum)
