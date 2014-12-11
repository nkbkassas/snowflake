from parser import *
from lexeme import *
from lexer import *
from environment import *
import builtinfuncs as b
import math as m
import sys 

class Eval:
    def __init__(self):
        self.globalEnvironment = Environment()
        self.globalEnvironment.assignEnvironment("!", "delay")
        self.globalEnvironment.assignEnvironment("$", "evaluate")
        self.globalEnvironment.assignEnvironment("assign", b.assign)
        self.globalEnvironment.assignEnvironment("crystalize", b.myPrint)
        self.globalEnvironment.assignEnvironment("concatenate", b.concatenate)
        self.globalEnvironment.assignEnvironment("add", b.add)
        self.globalEnvironment.assignEnvironment("subtract", b.subtract)
        self.globalEnvironment.assignEnvironment("mul", b.mul)
        self.globalEnvironment.assignEnvironment("div", b.div)
        self.globalEnvironment.assignEnvironment("pow", b.pow)
        self.globalEnvironment.assignEnvironment("mod", b.mod)
        self.globalEnvironment.assignEnvironment("factorial", b.factorial)
        self.globalEnvironment.assignEnvironment("sqrt", m.sqrt)
        self.globalEnvironment.assignEnvironment("string", b.string)
        self.globalEnvironment.assignEnvironment("int", b.toInt)
        self.globalEnvironment.assignEnvironment("input", b._input)
        self.globalEnvironment.assignEnvironment("len", b.length)
        self.globalEnvironment.assignEnvironment("true", Lexeme( True , "Boolean" ))
        self.globalEnvironment.assignEnvironment("false", Lexeme( False , "Boolean" ))
        self.globalEnvironment.assignEnvironment("OR", b.OR)
        self.globalEnvironment.assignEnvironment("AND", b.AND)
        self.globalEnvironment.assignEnvironment("NOT", b.NOT)
        self.globalEnvironment.assignEnvironment("sin", Lexeme(m.sin, "INTEGER"))
        self.globalEnvironment.assignEnvironment("cos", Lexeme(m.cos, "INTEGER"))
        self.globalEnvironment.assignEnvironment("tan", Lexeme(m.tan, "INTEGER"))
        self.globalEnvironment.assignEnvironment("acos", Lexeme(m.acos, "INTEGER"))
        self.globalEnvironment.assignEnvironment("asin", Lexeme(m.asin, "INTEGER"))
        self.globalEnvironment.assignEnvironment("atan", Lexeme(m.atan, "INTEGER"))
        self.globalEnvironment.assignEnvironment("int", b.toInt)
        self.globalEnvironment.assignEnvironment("nil", Lexeme( None, "nil"))
        self.globalEnvironment.assignEnvironment("array", b.array)
        self.globalEnvironment.assignEnvironment("size", b.size)
        self.globalEnvironment.assignEnvironment("printArray", b.printList)
        self.globalEnvironment.assignEnvironment("setItem", b.setItem)
        self.globalEnvironment.assignEnvironment("getItem", b.getItem)
        self.globalEnvironment.assignEnvironment("deleteItem", b.deleteItem)
        self.globalEnvironment.assignEnvironment("setItem", b.setItem)
        self.globalEnvironment.assignEnvironment("append", b.append)
        self.globalEnvironment.assignEnvironment("head", b.head)
        self.globalEnvironment.assignEnvironment("tail", b.tail)
        self.globalEnvironment.assignEnvironment("preList", b.preList)
        self.globalEnvironment.assignEnvironment("postList", b.postList)
        self.globalEnvironment.assignEnvironment("cons", b.cons)
        self.globalEnvironment.assignEnvironment("car", b.car)
        self.globalEnvironment.assignEnvironment("cdr", b.cdr)
        self.globalEnvironment.assignEnvironment("lt", b.lt)
        self.globalEnvironment.assignEnvironment("gt", b.gt)
        self.globalEnvironment.assignEnvironment("lte", b.lte)
        self.globalEnvironment.assignEnvironment("gte", b.gte)
        self.globalEnvironment.assignEnvironment("eq", b.eq)
        self.globalEnvironment.assignEnvironment("noteq", b.noteq)


    def eval(self, tree, env):
        if tree == None:
            return 
        if tree.tokenType == "funcDef":
            return self.eval_funcDef(tree, env)
        elif tree.tokenType == "body":
            return self.eval_body(tree, env)
        elif tree.tokenType == "var_list":
            return self.eval_var_list(tree, env)
        elif tree.tokenType == "statement_list":
            return self.eval_statement_list(tree, env)
        elif tree.tokenType == "ifStatement":
            return self.eval_ifStatement(tree, env)
        elif tree.tokenType == "cycle":
            return self.eval_cycle(tree, env)
        elif tree.tokenType == "classDef":
            return self.eval_classDef(tree, env)
        elif tree.tokenType == "elif":
            return self.eval_elif(tree, env)
        elif tree.tokenType == "else":
            return self.eval_else(tree, env)
        elif tree.tokenType == "funcCall":
            return self.eval_funcCall(tree, env)
        elif tree.tokenType == "expr_list":
            return self.eval_expr_list(tree, env)
        elif tree.tokenType == "opt_var_list":
            return self.eval_var_list(tree, env)
        elif tree.tokenType == "opt_expr_list":
            return self.eval_expr_list(tree, env)
        elif tree.tokenType == "STRING":
            return tree
        elif tree.tokenType == "INTEGER":
            return tree
        elif tree.tokenType == "NeedsSemiColon":
            return self.eval_needsSemiColon(tree, env)
        elif tree.tokenType == "var":
            return env.lookupEnvironment( tree.token )
        return 


    def eval_funcDef(self, tree, env):
        name = tree.left.token
        params = self.eval(tree.right.left, env)
        body = tree.right.right
        env.assignEnvironment(name, ("funcDef", params, body, env))

    def eval_classDef(self, tree, env):
        name = tree.left.token
        body = tree.right
        env.assignEnvironment(name, ("classDef", [], body, env))

    def eval_body(self, tree, env):
        return self.eval(tree.left, env)


    def eval_statement_list(self, tree, env):
        statement = None
        while tree:
            statement = self.eval(tree.left, env)
            tree = tree.right
        return statement

    def eval_ifStatement(self, tree, env):
        #if expr of first if statment is true, evaluate body 
        tmp = self.eval( tree.left , env );
        if(tmp.token):
            return self.eval(tree.right.left, env)
        #else, check for elifs and else statements
        else:
            #Get elIf statements
            ELIF = tree.right.right.left
            #While there still are elif statements, evaluate in sequence
            while ELIF:
                #Check to see if an elif expr evaluates to true
                tmp = self.eval( ELIF.left.left , env );
                if(tmp.token):
                #if elif evaluates to true, evaluate body of elif
                    return self.eval(ELIF.left.right,env)
                else:
                    ELIF = ELIF.right 
            #else none of the if-statements are true, evaluate body of else
            return self.eval(tree.right.right.right, env)


    def eval_cycle(self, tree, env):
        #get cond, execute while loop if cond is true
        cond = self.eval(tree.left, env)
        while cond.token:
            body = self.eval(tree.right,env)
            cond = self.eval(tree.left, env)

    def eval_elif(self, tree, env):
        return self.eval(tree.left, env)

    def eval_else(self, tree, env):
        return self.eval(tree.left, env)

    def secret( self , tree , depth ):
        if tree == None:
            return;
        self.secret( tree.left , depth + 1 )
        print( ("   " * depth) + "'" + tree.token + "' : " + tree.tokenType )
        self.secret( tree.right , depth + 1 );

    def printToken( self , tree ):
        self.secret( tree , 0 )
        print("------------------------------")

    def eval_funcCall(self, tree, env):

        if(tree.left != None):
            obj = env.lookupEnvironment(tree.left.token)
            tree.left = None
            return self.eval(tree, obj)

        # Info is the function we are calling
        info = env.lookupEnvironment(tree.right.left.token)
        eargs = []
        if( info == b.assign ):
            eargs.append( tree.right.right.left )
            args = self.eval( tree.right.right.right , env)
        #elif( info == b.delay ):
         #   eargs.append( (tree.right.right.left, env))
            #args = self.eval(tree.right.right, env)
        else:
            args = self.eval(tree.right.right, env)

        #  built-in
        if not isinstance(info, tuple):
            for atree in args:
                eargs.append(atree)
            return info(eargs,env)


        #info is not a tuple
        params = info[1]
        body = info[2]
        defEnv = info[3]

        #Check to make sure the number of arguments in a func call is 
        #equal to the number of parameters in the func def
        if(args and params and len(args) != len(params)):
            print("Error. The number of arguments given does not match the number of parameters.")
            #print("info is", info)
            sys.exit(1)
       
        addToEnv = dict()
        #if the func def included params
        #add the param (var) and its arg (value) to the environment
        if(params):
            for i, item in enumerate(params):
                addToEnv[item.token] = args[i]

        #Extend the def environment
        xenv = defEnv.extendEnvironment(addToEnv)
        xenv.assignEnvironment("flurry", xenv)
        return self.eval(body, xenv)

    def eval_expr_list(self, tree, env):
        exprList = []
        while tree:
            exprList.append(self.eval(tree.left,env))
            tree = tree.right
        return exprList

    def eval_var_list(self, tree, env):
        varList = []
        while tree:
            varList.append(tree.left)
            tree = tree.right
        return varList

    def eval_needsSemiColon(self, tree, env):
        return self.eval(tree.left, env)

    #def eval_var(self, tree, env):

def evaluate():
    lex = Lexer(sys.argv[1])
    parse = Parser(lex)
    tree = parse.program()
    e = Eval()
    # call eval with the parse tree and global environment
    e.eval(tree, e.globalEnvironment)

evaluate()
