class Lexeme:
    def __init__(self, token, tokenType, linepos = -1, colpos = -1):
        self.token = token
        self.tokenType = tokenType
        self.linepos = linepos
        self.colpos = colpos
        self.right = None
        self.left = None

    def __str__(self):
        return "Lexeme:" + str(self.token) + ", " + str(self.tokenType) 
