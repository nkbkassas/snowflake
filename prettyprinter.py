from parser import *
from lexer import *
import sys 


def prettyPrint(filename):
    lex = Lexer(filename)
    parse = Parser(lex)
    tree = parse.program()
    print(printTree(tree)) 

def printTree(tree,depth=0):
    if tree == None:
        return ""
    string = ""
    if tree.tokenType == "funcDef":
        string += "snowflake "
        string += printTree(tree.left, depth)
        string += "("
        string += printTree(tree.right.left, depth)
        string += "):\n"
        depth += 1 
        string += "  " * depth
        string += printTree(tree.right.right, depth)
    elif tree.tokenType == "cycle":
        string += "cycle("
        string += printTree(tree.left, depth)
        string += ":\n"
        depth += 1
        string += "  " * depth
        string += printTree(tree.right.left, depth)
    elif tree.tokenType == "body":
        string += "form \n"
        depth += 1
        string += "  " * depth
        string += printTree(tree.left, depth)
        depth -= 1
        string += "  " * depth
        string += "freeze \n"
    elif tree.tokenType == "var_list":
        string += printTree(tree.left, depth)
        string += printTree(tree.right, depth)
    elif tree.tokenType == "statement_list":
        string += printTree(tree.left, depth)
        string += "\n"
        if(tree.right != None):
            string += "  " * depth
        string += printTree(tree.right, depth)
    elif tree.tokenType == "ifStatement":
        string += "if("
        string += printTree(tree.left, depth)
        string += "):\n"
        depth += 1
        string += "  " * depth
        string += printTree(tree.right.left, depth)
        if(tree.right.right.left != None):
            string += "  " * depth
        string += printTree(tree.right.right.left, depth)
        if(tree.right.right.right != None):
            string += "  " * depth
        string += printTree(tree.right.right.right, depth)
    elif tree.tokenType == "cycle":
        string += "cycle("
        string += printTree(tree.left, depth)
        string += "):\n"
        depth += 1
        string += "  " * depth
        string += printTree(tree.right.left, depth)
    elif tree.tokenType == "classDef":
        string += "snowball "
        string += printTree(tree.left, depth)
        string += ": \n"
        depth += 1
        string += "  " * depth
        string += printTree(tree.right, depth)
    elif tree.tokenType == "elif":
        string += "elif("
        string += printTree(tree.left.left, depth)
        string += "): \n"
        depth += 1
        string += "  " * depth
        string += printTree(tree.left.right, depth)
        string += printTree(tree.right, depth)
    elif tree.tokenType == "else":
        string += "else: \n"
        depth += 1
        string += "  " * depth
        string += printTree(tree.left, depth)
    elif tree.tokenType == "funcCall":
        if(tree.left != None):
            string += printTree(tree.left,depth)
            string += "*"
        string += printTree(tree.right.left, depth)
        string += "("
        string += printTree(tree.right.right, depth)
        string += ")"
    elif tree.tokenType == "expr_list":
        string += printTree(tree.left, depth)
        string += printTree(tree.right, depth)
    elif tree.tokenType == "opt_var_list":
        string += ", "
        string += printTree(tree.left, depth)
        string += printTree(tree.right, depth)
    elif tree.tokenType == "opt_expr_list":
        string += ", "
        string += printTree(tree.left, depth)
        string += printTree(tree.right, depth)
    elif tree.tokenType == "STRING":
        string += '"'
        string += tree.token
        string += '"'
    elif tree.tokenType == "INTEGER":
        string += str(tree.token)
    elif tree.tokenType == "NeedsSemiColon":
        string += printTree(tree.left, depth)
        string += ";"
    elif tree.tokenType == "var":
       string += tree.token
    return string

prettyPrint(sys.argv[1])
