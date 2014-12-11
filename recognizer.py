import sys
from lexer import *
from parser import *


def main():
    filename = sys.argv[1]
    l = Lexer(filename)
    p = Parser(l)
    p.program()
    print("Valid program")

main()

