import sys

from analyzers.Lexer import Lexer
from analyzers.CParser import CParser
from analyzers.PyParser import PyParser

from tokens.tkIDs import tkIDsList
from tokens.CRegEx import CRegExList
from tokens.PyRegEx import PyRegExList

from preprocessors.tokens_preprocessing import py_tokens_preprocessing, c_tokens_preprocessing




def main():
    match sys.argv:
        case _, '-i'|'--input', input_path, '-o'|'--output', output_path:
            code = ''

            with open(input_path, 'r') as file:
                for line in file.readlines():
                    code += f'{line.rstrip()}\n'

            if input_path.endswith('.py'):
                lexer = Lexer(zip(tkIDsList, PyRegExList))

                parser = PyParser(tkIDsList)
                parser.parse()
                parser = parser.pg.build()

                tokens = py_tokens_preprocessing(lexer(code))

                result = parser.parse(iter(tokens))
            
            else:
                lexer = Lexer(zip(tkIDsList, CRegExList))

                parser = CParser(tkIDsList)
                parser.parse()
                parser = parser.pg.build()

                code = code[code.find('{')+1:code.rfind('}')]

                tokens = c_tokens_preprocessing(lexer(code))

                result = parser.parse(iter(tokens))

            with open(output_path, 'w') as file:
                file.write(result)

        case _, '-h'|'--help'|'?':
            print('[INFO]:\t[-i] | [--input] - path to file with translated code\n\t[-o] | [--output] - path to file for save result of translating (auto create)\n\t[-h] | [--help] | [?] - help')

        case _:
            print('[ERROR]:\tInvalid args!')
            print(sys.argv)





if __name__ == '__main__':
    main()