import sys
from tokens import *

class Lexer:
    def __init__(self, input):
        self.source = input + '\n'
        self.curChar = ''
        self.curPos = -1
        self.nextChar();

    # Process the next character.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'
        else:
            self.curChar = self.source[self.curPos]

    # Return the lookahead character.
    def peek(self):
        if (self.curPos + 1) >= len(self.source):
            return '\0'
        else:
            return self.source[self.curPos + 1]

    # Invalid token found, print error message and exit.
    def abort(self, message):
        sys.exit("Lexing Error OwO: " + message)

    def legalvarname(self, str):
        if str.isupper():
            self.abort("Upper Case in Variable Name OWO")
        if str.isdigit():
            self.abort("Number in Variable Name OWO")
        return True


    # Skip whitespace except newlines, which we will use to indicate the end of a statement.
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    # Skip comments in the code.
    def skipComment(self):
        if self.curChar == '#' :
            while self.curChar != '\n':
                self.nextChar()


    # Return the next token.
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()
#         operators

        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token(' ', TokenType.EOF)
        elif self.curChar == '=':
            if self.peek() == '=':
                prevChar = self.curChar
                self.nextChar()
                token = Token(prevChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == '<' :
            if self.peek() == '=':
                prevChar = self.curChar
                self.nextChar()
                token = Token(prevChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '>' :
            if self.peek() == '=':
                prevChar = self.curChar
                self.nextChar()
                token = Token(prevChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '!':
            if self.peek() == '=':
                prevChar = self.curChar
                self.nextChar()
                token = Token(prevChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("! not followed by =")


        #     some strings

        elif self.curChar == '\"':
            self.nextChar()
            startIndex = self.curPos
            while self.curChar != '\"':
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal characters in a String")
                self.nextChar()

            stringText = self.source[startIndex:self.curPos]
            token = Token(stringText, TokenType.STRING)

        # some numbers

        elif self.curChar.isdigit():
            startIndex = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.curChar == '.':
                if not self.peek().isdigit():
                    self.abort("Bad character is number after decimal point. Check brain. ")
                while self.peek().isdigit():
                    self.nextChar()
            number  = self.source[startIndex:self.curPos + 1]
            token = Token(number, TokenType.NUMBER)

        # identifiers and keyword

        elif self.curChar.isalnum():
            startIndex = self.curPos
            while self.peek().isalnum():
                self.nextChar()
            stringText = self.source[startIndex:self.curPos + 1]
            ident = Token.checkifKeyword(stringText)
            if ident != None:
                token = Token(stringText, ident)
            else:
                self.legalvarname(stringText)
                token = Token(stringText, TokenType.IDENT)


        else:
            self.abort("Illegal Character: " + self.curChar)


        self.nextChar()
        return token

