import sys
from lexeme import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.currentLexeme = self.lexer.lex()
        self.nextLexeme = self.lexer.lex()

    def advance(self):
        self.currentLexeme = self.nextLexeme
        self.nextLexeme = self.lexer.lex()

    def check(self, tokenType):
        if self.currentLexeme == None:
            return False
        else:
            return self.currentLexeme.tokenType == tokenType
    
    def join(self, left, right, name = "JOIN"):
        l = Lexeme("", str(name), -1, -1)
        l.left = left
        l.right = right
        return l


    def checkNext(self, tokenType):
        return self.nextLexeme.tokenType == tokenType

    def match(self, tokenType):
        if self.currentLexeme == None:
            print("Syntax Error. Reached end of input too early. Expecting type: ", tokenType)
            sys.exit(1)
        elif self.check(tokenType) == False:
            print("Syntax error on line:", self.currentLexeme.linepos, "at position:", self.currentLexeme.colpos)
            print("Was expecting type:", tokenType, "found token type", self.currentLexeme.tokenType, "instead.")
            print("Invalid program")
            sys.exit(1)
        else:
            tmp = self.currentLexeme
            self.advance()
            return tmp

    def program(self):
        return self.statement_list()

    def statement_list(self):
        return self.join(self.statement(), self.opt_statement_list(), "statement_list")


    def statement(self):
        if(self.funcDef_pending()):
            l = self.funcDef()

        elif(self.classDef_pending()):
            l = self.classDef()

        elif(self.ifStatement_pending()):
            l = self.ifStatement()
        
        elif(self.cycle_pending()):
            l = self.cycle()

        elif(self.expr_pending()):
            l = self.expr()
            sc = self.match("SEMICOLON")
            l = self.join(l,sc,"NeedsSemiColon")
        else:
            l = None
        return l

    def opt_statement_list(self):
        if(self.statement_pending()):
            return self.join(self.statement(), self.opt_statement_list(), "statement_list")
        return None

    def expr(self):
        if(self.funcCall_pending()):
            return self.funcCall()
        elif(self.var_pending()):
            return self.var()
        else:
            return self.literal()

    def funcDef(self):
        self.match("snowflake")
        a = self.var()
        self.match("OPAREN")
        b = self.var_list()
        self.match("CPAREN")
        self.match("COLON")
        c = self.body()
        return self.join(a, self.join(b,c), "funcDef")

    def classDef(self):
        self.match("snowball")
        a = self.var()
        self.match("COLON")
        b = self.body()
        return self.join(a,b, "classDef")

    def ifStatement(self):
        self.match("if")
        self.match("OPAREN")
        a = self.expr()
        self.match("CPAREN")
        self.match("COLON")
        b = self.body()
        c = self.opt_elif()
        d = self.opt_else()
        return self.join(a, self.join(b, self.join(c,d)), "ifStatement")

    def cycle(self):
        self.match("cycle")
        self.match("OPAREN")
        a = self.expr()
        self.match("CPAREN")
        self.match("COLON")
        b = self.body()
        return self.join(a,b, "cycle")


    def opt_elif(self):
        if(self.elif_pending()):
            return self.join(self.elif_(), self.opt_elif(), "elif")
        return None
    
    def opt_else(self):
        if(self.else_pending()):
            return self.else_()
        return None

    def else_(self):
        self.match("else")
        self.match("COLON")
        return self.join(self.body(),None, "else")


    def elif_(self):
        self.match("elif")
        self.match("OPAREN")
        a = self.expr()
        self.match("CPAREN")
        self.match("COLON")
        b = self.body()
        return self.join(a,b, "elif")

    def body(self):
        self.match("form")
        l = self.statement_list() 
        self.match("freeze")
        return self.join(l,None, "body")

    def literal(self):
        if(self.integer_pending()):
            return self.integer()
        else:
            return self.string()

    def integer(self):
        return self.match("INTEGER")

    def string(self):
        return self.match("STRING")

    def var(self):
       return self.match("var")

    def funcCall(self):
        a = self.var()
        if self.check("STAR"):
            self.match("STAR")
            className = a
            funcName = self.var()
        else:
            className = None
            funcName = a
        self.match("OPAREN")
        exprList = self.expr_list()
        self.match("CPAREN")
        return self.join(className, self.join(funcName, exprList), "funcCall")



    def secret( self , tree , count ):
        if( tree == None ): return
        self.secret( tree.left , count + 1 )
        print( ("  " * count) + "'" + str(tree.token) + "'" )
        self.secret( tree.right , count + 1 )

    def printToken(self , tree ):
        print( "------------------------------" );
        self.secret( tree , 0 )
        print( "------------------------------" );
    def expr_list(self):
        if self.expr_pending():
            a = self.expr()
            b = self.opt_expr_list()
            return self.join(a,b,"expr_list")
        return None

    def opt_expr_list(self):
        if self.check("COMMA"):
            self.match("COMMA")
            a = self.expr()
            b = self.opt_expr_list()
            return self.join(a,b,"opt_expr_list")
        return None

    def var_list(self):
        if self.var_pending():
            a = self.var()
            b = self.opt_var_list()
            return self.join(a,b, "var_list")
        return None

    def opt_var_list(self):
        if self.check("COMMA"):
            self.match("COMMA")
            a = self.var()
            b = self.opt_var_list()
            return self.join(a,b, "opt_var_list")
        else:
            None

    def expr_pending(self):
        return self.funcCall_pending() or self.var_pending() or self.literal_pending()

    def funcCall_pending(self):
        return self.check("var") and (self.checkNext("OPAREN") or self.checkNext("STAR"))

    def var_pending(self):
        return self.check("var")

    def funcDef_pending(self):
        return self.check("snowflake")

    def classDef_pending(self):
        return self.check("snowball")

    def ifStatement_pending(self):
        return self.check("if")

    def elif_pending(self):
        return self.check("elif")

    def else_pending(self):
        return self.check("else")

    def cycle_pending(self):
        return self.check("cycle")

    def statement_pending(self):
        return self.expr_pending() or self.funcDef_pending() or self.classDef_pending() or self.ifStatement_pending() or self.cycle_pending()

    def literal_pending(self):
        return self.integer_pending() or self.check("STRING")

    def integer_pending(self):
        return self.check("INTEGER")
