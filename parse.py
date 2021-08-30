import sys
from lex import *

# Parser object keeps track of current token and checks if the code matches the grammar.
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()

    # Return true if the current token matches.
    def checkToken(self, kind):
        return self.curToken.kind == kind

    # Return true if the next token matches.
    def checkPeek(self, kind):
        return self.peekToken.kind == kind

    # Try to match current token. If not, error. Advances the current token.
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected: " + kind.name + ", got  " + self.curToken.kind.name)
        self.nextToken()

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message):
        sys.exit("Error. " + message)

    def program(self):
        print("PROGRAM")

        while not self.checkToken(TokenType.EOF):
            self.statement()

    def statement(self):
        # print statement
        if self.checkToken(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()
            if self.checkToken(TokenType.STRING):
                self.nextToken()
            else:
                self.expression()

        elif self.checkToken(TokenType.IF):
            print("STATEMENT-IF")
            self.nextToken()
            self.comp()
            self.match(TokenType.THEN)
            self.nl()
            while not self.checkToken(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)

        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.nextToken()
            self.comp()
            self.match(TokenType.REPEAT)
            self.nl()
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()
            self.match(TokenType.ENDWHILE)

        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.nextToken()
            self.match(TokenType.IDENT)

        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.nextToken()
            self.match(TokenType.IDENT)

        elif self.checkToken(TokenType.LET):
            print("STATEMENT-LET")
            self.nextToken()
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()

        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.nextToken()
            self.match(TokenType.IDENT)

        else:
            self.abort("Statement Expected, Not a Statement Current Token: " + self.curToken.kind.name )

        self.nluwu()

    def nl(self):
        print("NEWLINE")
        if self.checkToken(TokenType.NEWLINE):
            while self.checkPeek(TokenType.NEWLINE):
                self.nextToken()
            self.nextToken()
        else:
            self.abort("New Line expected")

    def nluwu(self):
        print("NEWLINE-UWU")
        if self.checkToken(TokenType.UWU):
            self.nextToken()
            while self.checkToken(TokenType.NEWLINE):
                self.nextToken()
        else:
            self.abort("UWU expected")

    def comp(self):
        print("COMPARISON")
        self.expression()
        if self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ) or self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ):
            self.nextToken()
            self.expression()
            while self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ) or self.checkToken(TokenType.GT) or self.checkToken(TokenType.GTEQ) or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ):
                self.nextToken()
                self.expression()
        else:
            self.abort("Comparator Expected")

    def expression(self):
        print("EXPRESSION")
        self.term()
        while self.checkToken(TokenType.MINUS) or self.checkToken(TokenType.PLUS):
            self.nextToken()
            self.term()

    def term(self):
        print("TERM")
        self.unary()
        while self.checkToken(TokenType.SLASH) or self.checkToken(TokenType.ASTERISK):
            self.nextToken()
            self.unary()

    def unary(self):
        print("UNARY")
        if self.checkToken(TokenType.MINUS) or self.checkToken(TokenType.PLUS):
            self.nextToken()
        self.primary()

    def primary(self):
        print("PRIMARY: " + self.curToken.text)
        if self.checkToken(TokenType.NUMBER):
            self.nextToken()
        else:
            self.match(TokenType.IDENT)
