from lexeme import *
import sys


#def while



def printList(args, env ):
    for a in args:
        while isinstance( a , Lexeme ):
            a = a.token
        if isinstance( a , list ):
            printList( a, env )
        else:
            while isinstance( a , Lexeme ):
                a = a.token
            print( str( a ) , end = " " )
    print( end= "\n" )

def myPrint(args,env):
    
    for arg in args:
        if( isinstance( arg.token , list) ):
            printList( arg.token, env )
        else:
            while isinstance( arg , Lexeme ):
                arg = arg.token
            print( arg , end = " ")
        print()

def _input(args, env):
    return Lexeme(input(args[0].token + " "), "prompt")


def assign(args,env):
    if( len( args ) != 2 ):
        print( "Incorrect number of arguments for assign. Takes in 2 arguments only. You provided", str(len(args)), "arguments instead.")
        sys.exit(1)
    env.assignEnvironment( args[0].token , args[1] )
    return args[1]

def concatenate(args,env):
    result = ""
    for arg in args:
        result += arg.token 
    return Lexeme(result, "STRING")

def pow(args, env):
    if(len(args) != 2):
        print("Incorrect number of arguments for func pow. Takes in 2 arguments only. You provided", str(len(args)), "argument(s) instead.")
    return Lexeme(args[0] ** args[1], "INTEGER")

def length(args, env):
    return Lexeme( len(args), "INTEGER")

def size(args, env):
    return Lexeme( len(args[0].token), "INTEGER")

def toInt(args, env):
    if len(args) != 1:
        print("Incorrect number of arguments for fun toInt. Takes in 1 argument. You provided", str(len(args)), "arguments instead.")
    return Lexeme( int(args[0].token), "INTEGER")


def add(args,env):
    result = 0
    for arg in args:
        result += arg.token
    return Lexeme( result , "INTEGER" )

def subtract(args,env):
    result = None
    for arg in args:
        if type(arg.token) != int:
            print("Error. Incorrect token type for func subtract. Should be integers only. You supplied:", str(arg.token) + "," ,"a", arg.tokenType)
            sys.exit(1)
        elif result != None:
            result -= arg.token
        else:
            result = arg.token
    return Lexeme( result , "INTEGER" )

def mul(args,env):
    result = 1
    for arg in args:
        result *= arg.token
    return Lexeme( result , "INTEGER" )

def factorial(args,env):
    if( len( args ) != 1 ):
        print( "Incorrect number of arguments for func factorial. Takes in 1 argument only. You provided", str(len(args)), "arguments instead")
        sys.exit(1)
    result = 1
    while args[0].token > 0:
        result *= args[0].token
        args[0].token -= 1
    return Lexeme( result , "INTEGER" )

def neg(args,env):
    if( len( args ) != 1 ):
        print( "Incorrect number of arguments for func neg")
        sys.exit(1)
    return Lexeme( -args[0].token , "INTEGER" )

def string(args,env):
    if( len( args ) != 1 ):
        print( "Incorrect number of arguments for func string. Takes in 1 argument only. You provided", str(len(args)), "arguments instead.")
        sys.exit(1)
    return Lexeme( str(args[0].token) , "STRING" )

def noteq(args, env):
    if( len( args ) != 2 ):
        print( "Incorrect number of arguments for func noteq. Takes in 2 argument only. You provided", str(len(args)), "arguments instead.")
        sys.exit(1)
    return Lexeme( args[0].token != args[1].token , "Boolean" )


def lt(args,env):
    if( len( args ) != 2 ):
        print( "Incorrect number of arguments for func lt. Takes in 2 argument only. You provided", str(len(args)), "arguments instead.")
        sys.exit(1)
    return Lexeme( args[0].token < args[1].token , "Boolean" )

def gt(args,env):
    if( len( args ) != 2 ):
        print( "Incorrect number of arguments for func gt. Takes in 2 arguments only. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    return Lexeme( args[0].token < args[1].token , "Boolean" )

def lte(args,env):
    if( len( args ) != 2 ):
        print( "Incorrect number of arguments for func lte. Takes in 2 arguments only. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    return Lexeme(args[0].token <= args[1].token, "Boolean")

def gte(args,env):
    if( len( args ) != 2 ):
        print( "Incorrect number of arguments for func gte. Takes in 2 arguments only. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    return Lexeme( args[0].token <= args[1].token , "Boolean" )

def eq(args,env):
    if( len( args ) != 2 ):
        print( "Incorrect number of arguments for func eq. Takes in 2 arguments only. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    return Lexeme( args[0].token == args[1].token , "Boolean" )

def NOT(args,env):
    if( len( args ) != 1 ):
        print( "Incorrect number of arguments for func not. Takes in 1 argument only. You provided", str(len(args)), "arguments instead.")
        sys.exit(1)
    return Lexeme( not(args[0].token) , "Boolean" )

def AND(args,env):
    for arg in args:
        if( not arg ):
            return Lexeme( False , "Boolean" )
    return Lexeme( True , "Boolean" )

def OR(args,env):
    for arg in args:
        if( arg ):
            return Lexeme( True , "Boolean" )
    return Lexeme( False , "Boolean" )

def mod(args,env):
    if( len( args ) != 2 ):
        print( "Incorrect number of arguments for func mod. Takes in 2 argument onlys. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    return Lexeme( args[0].token % args[1].token , "INTEGER" )

def div(args,env):
    if( len( args ) != 2 ):
        print( "Incorrect number of arguments for func div. Takes in 2 arguments only. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    return Lexeme(args[0].token / args[1].token, "INTEGER")

def getItem(args,env):
    if(len(args) != 2):
        print( "Incorrect number of arguments for func getItem. Takes in 2 arguments only. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    return Lexeme(args[0].token[args[1].token], "INTEGER")

def setItem(args,env):
    if(len(args) != 2):
        print( "Incorrect number of arguments for func setItem. Takes in 2 arguments only. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    return Lexeme(args[0].token.insert(args[1].token,args[2].token), "ARRAY")

def append(args,env):
    if(len(args) != 2):
        print( "Incorrect number of arguments for func append. Takes in 2 arguments only. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    args[0].token.append(args[1].token)

def deleteItem(args,env):
    if(len(args) != 1):
        print( "Incorrect number of arguments for func deleteItem. Takes in 1 argument only. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    return Lexeme(args[0].token.pop(args[1].token), "ARRAY")

def cons(args,env):
    if(len(args) != 2):
        print( "Incorrect number of arguments for func getItem. Takes in 2 arguments only. You provided", str(len(args)), "argument(s) instead.")
        sys.exi(1)
    args[0].token.append(args[1].token)
    return Lexeme( [args[0].token,args[1].token] , "ARRAY" )

def car(args,env):
    if(len(args) != 1):
        print( "Incorrect number of arguments for func car. Takes in 1 argument only. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    args[0].token.append(args[1].token)
    return Lexeme( args[0].token[0] , "ARRAY" )

def cdr(args,env):
    if(len(args) != 1):
        print( "Incorrect number of arguments for func cdr. Takes in 1 argument only. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    return Lexeme( args[0].token[1], "ARRAY" ) 

def head(args,env):
    if(len(args) != 1):
        print( "Incorrect number of arguments for func head. Takes in 1 argument only. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    return Lexeme( args[0].token[0] , "ARRAY" )

def tail(args,env):
    if(len(args) != 1):
        print( "Incorrect number of arguments for func tail. Takes in 1 argument only. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    return Lexeme( args[0].token[1:] , "ARRAY" )

def array(args,env):
    lst = []
    for arg in args:
        lst.append(arg)
    return Lexeme( lst , "ARRAY" )

def preList(args,env):
    if(len(args) != 2):
        print( "Incorrect number of arguments for func preList. Takes in 2 argument only. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    return Lexeme( args[0].token[:args[1].token] , "ARRAY" )

def postList(args,env):
    if(len(args) != 2):
        print( "Incorrect number of arguments for func postList. Takes in 2 argument only. You provided", str(len(args)), "argument(s) instead.")
        sys.exit(1)
    return Lexeme( args[0].token[args[1].token:] , "ARRAY" )
