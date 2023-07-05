from rply import LexerGenerator


class Lexer():
    def __init__(self, lexemes):
        self.lexer = LexerGenerator()
        self.lexemes = lexemes
    
        self.__add_tokens()
        self.lexer = self.lexer.build()

    def __add_tokens(self):
        for ID, regex in self.lexemes:
            self.lexer.add(ID, regex)
            

    def __call__(self, text):
        return self.lexer.lex(text)