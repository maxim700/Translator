from rply import ParserGenerator
from analyzers.Token import Token

tab = '    '

class CParser():
    def __init__(self, tokens) -> None:
        self.pg = ParserGenerator(tokens)

        self.tabulate_compound = lambda compound: tab.join(compound.splitlines(True))


    def parse(self):
        @self.pg.production("main : compound_stmt")
        def main(p) -> str:
            return '\n'.join(p)


        @self.pg.production("compound_stmt : if_stmt")
        @self.pg.production("compound_stmt : for_stmt")
        @self.pg.production("compound_stmt : while_stmt")
        @self.pg.production("compound_stmt : assignment_stmt")
        @self.pg.production("compound_stmt : function_stmt")
        @self.pg.production("compound_stmt : if_stmt compound_stmt")
        @self.pg.production("compound_stmt : for_stmt compound_stmt")
        @self.pg.production("compound_stmt : while_stmt compound_stmt")
        @self.pg.production("compound_stmt : assignment_stmt compound_stmt")
        @self.pg.production("compound_stmt : function_stmt compound_stmt")
        def compound_stmt(p):
            '''
                Главная структура программы
            '''

            match p:
                case [statement]:
                    result = f'{statement}'

                case [statement, compound]:
                    result = f'{statement}\n{compound}'

            return result


        @self.pg.production("if_stmt : tkIf tkORoundBr condition_stmt tkCRoundBr tkOCurlyBr compound_stmt tkCCurlyBr")
        @self.pg.production("if_stmt : tkIf tkORoundBr condition_stmt tkCRoundBr tkOCurlyBr compound_stmt tkCCurlyBr elif_stmt")
        @self.pg.production("if_stmt : tkIf tkORoundBr condition_stmt tkCRoundBr tkOCurlyBr compound_stmt tkCCurlyBr else_stmt")
        def if_stmt(p):
            '''
                Условный оператор if
            '''

            match p:
                case Token('tkIf') as tkIf, Token('tkORoundBr'), condition, Token('tkCRoundBr'), Token('tkOCurlyBr'), compound, Token('tkCCurlyBr'):
                    result = f'{tkIf.value} ({condition}):\n{tab}{self.tabulate_compound(compound)}\n'

                case Token('tkIf') as tkIf, Token('tkORoundBr'), condition, Token('tkCRoundBr'), Token('tkOCurlyBr'), compound, Token('tkCCurlyBr'), other:
                    result = f'{tkIf.value} ({condition}):\n{tab}{self.tabulate_compound(compound)}\n{other}'

            return result


        @self.pg.production("elif_stmt : tkElif tkORoundBr condition_stmt tkCRoundBr tkOCurlyBr compound_stmt tkCCurlyBr")
        @self.pg.production("elif_stmt : tkElif tkORoundBr condition_stmt tkCRoundBr tkOCurlyBr compound_stmt tkCCurlyBr elif_stmt")
        @self.pg.production("elif_stmt : tkElif tkORoundBr condition_stmt tkCRoundBr tkOCurlyBr compound_stmt tkCCurlyBr else_stmt")
        def elif_stmt(p):
            '''
                Условный оператор elif
            '''

            match p:
                case Token('tkElif'), Token('tkORoundBr'), condition, Token('tkCRoundBr'), Token('tkOCurlyBr'), compound, Token('tkCCurlyBr'):
                    result = f'elif ({condition}):\n{tab}{self.tabulate_compound(compound)}\n'


                case Token('tkElif'), Token('tkORoundBr'), condition, Token('tkCRoundBr'), Token('tkOCurlyBr'), compound, Token('tkCCurlyBr'), other:
                    result = f'elif ({condition}):\n{tab}{self.tabulate_compound(compound)}\n{other}'

            return result


        @self.pg.production("else_stmt : tkElse tkOCurlyBr compound_stmt tkCCurlyBr")
        def else_stmt(p):
            '''
                Условный оператор else
            '''

            match p:
                case Token('tkElse') as tkElse, Token('tkOCurlyBr'), compound, Token('tkCCurlyBr'):
                    result = f'{tkElse.value}:\n{tab}{self.tabulate_compound(compound)}\n'
    
            return result


        @self.pg.production("for_stmt : tkFor tkORoundBr assignment_stmt tkID boolean_stmt expression_stmt assignment_stmt tkCRoundBr tkOCurlyBr compound_stmt tkCCurlyBr")
        def for_stmt(p):
            '''
                Цикл for
            '''

            match p:
                case Token('tkFor') as tkFor, Token('tkORoundBr'), assignment, Token('tkID') as tkID, boolean, expression, statement, Token('tkCRoundBr'), Token('tkOCurlyBr'), compound, Token('tkCCurlyBr'):
                    start = assignment.split()[-1]
                    end = expression
                    step = statement.split()[-1]

                    result = f'{tkFor.value} {tkID.value} in range({start}, {end}, {step}):\n{tab}{self.tabulate_compound(compound)}\n'

            return result


        @self.pg.production("while_stmt : tkWhile tkORoundBr condition_stmt tkCRoundBr tkOCurlyBr compound_stmt tkCCurlyBr")
        def while_stmt(p):
            '''
                Цикл while
            '''

            match p:
                case Token('tkWhile') as tkWhile, Token('tkORoundBr'), condition, Token('tkCRoundBr'), Token('tkOCurlyBr'), compound, Token('tkCCurlyBr'):
                    result = f'{tkWhile.value} {condition}:\n{tab}{self.tabulate_compound(compound)}\n'

            return result


        @self.pg.production("condition_stmt : tkORoundBr condition_stmt tkCRoundBr")
        @self.pg.production("condition_stmt : condition_stmt boolean_stmt condition_stmt")
        @self.pg.production("condition_stmt : tkNot condition_stmt")
        @self.pg.production("condition_stmt : variable_stmt")
        @self.pg.production("condition_stmt : expression_stmt")
        def condition_stmt(p):
            '''
                Логическое выражение
            '''

            match p:
                case Token('tkORoundBr'), condition, Token('tkCRoundBr'):
                    result = f'{condition}'

                case left_condition, sigh, right_condition:
                    result = f'{left_condition} {sigh} {right_condition}'
                
                case Token('tkNot'), condition:
                    result = f'not({condition})'

                case [variable]:
                    result = variable

            return result


        @self.pg.production("variable_stmt : tkVarBoolean")
        @self.pg.production("variable_stmt : tkVarInteger")
        @self.pg.production("variable_stmt : tkVarString")
        @self.pg.production("variable_stmt : tkVarFloat")
        @self.pg.production("variable_stmt : tkID")
        @self.pg.production("variable_stmt : tkORoundBr type_stmt tkCRoundBr tkID")
        def variable_stmt(p):
            '''
                Переменная
            '''

            match p:
                case Token('tkORoundBr'), TYPE, Token('tkCRoundBr'), Token('tkID') as tkID:
                    result = f'{TYPE}({tkID.value})'

                case [Token(_) as token]:
                    result = token.value

            return result


        @self.pg.production("boolean_stmt : tkAnd")
        @self.pg.production("boolean_stmt : tkOr")
        @self.pg.production("boolean_stmt : tkEqual")
        @self.pg.production("boolean_stmt : tkNotEqual")
        @self.pg.production("boolean_stmt : tkGreaterOrEqual")
        @self.pg.production("boolean_stmt : tkLessOrEqual")
        @self.pg.production("boolean_stmt : tkGreater")
        @self.pg.production("boolean_stmt : tkLess")
        def boolean_stmt(p):
            '''
                Логические операторы
            '''

            match p:
                case [Token('tkAnd')]:
                    result = 'and'

                case [Token('tkOr')]:
                    result = 'or'

                case [Token(_) as token]:
                    result = token.value

            return result


        @self.pg.production("assignment_stmt : type_stmt tkID tkAssign expression_stmt")
        @self.pg.production("assignment_stmt : tkID tkAssign expression_stmt")
        @self.pg.production("assignment_stmt : tkID tkAssignAdd expression_stmt")
        @self.pg.production("assignment_stmt : tkID tkAssignSub expression_stmt")
        @self.pg.production("assignment_stmt : tkID tkAssignMul expression_stmt")
        @self.pg.production("assignment_stmt : tkID tkAssignDiv expression_stmt")
        @self.pg.production("assignment_stmt : tkID tkAssignMod expression_stmt")
        @self.pg.production("assignment_stmt : tkID tkAssignPower expression_stmt")
        @self.pg.production("assignment_stmt : tkID tkAssignFloor expression_stmt")
        def assignment_stmt(p):
            '''
                Оператор присвоения
            '''

            match p:
                case TYPE, Token('tkID') as tkID, Token('tkAssign') as sign, expression:
                    result = f'{tkID.value} : {TYPE} {sign.value} {expression}'

                case Token('tkID') as tkID, Token(_) as sign, expression:
                    result = f'{tkID.value} {sign.value} {expression}'

            return result


        @self.pg.production("type_stmt : tkInteger")
        @self.pg.production("type_stmt : tkFloat")
        @self.pg.production("type_stmt : tkString")
        @self.pg.production("type_stmt : tkBoolean")
        def type_stmt(p):

            match p:
                case [Token('tkInteger')]:
                    result = 'int'

                case [Token('tkBoolean')]:
                    result = 'bool'

                case [Token('tkFloat')]:
                    result = 'float'

                case [Token('tkString')]:
                    result = 'str'

            return result


        @self.pg.production("expression_stmt : expression_stmt tkAdd expression_stmt")
        @self.pg.production("expression_stmt : expression_stmt tkSub expression_stmt")
        @self.pg.production("expression_stmt : expression_stmt tkMul expression_stmt")
        @self.pg.production("expression_stmt : expression_stmt tkDiv expression_stmt")
        @self.pg.production("expression_stmt : expression_stmt tkMod expression_stmt")
        @self.pg.production("expression_stmt : expression_stmt tkPower expression_stmt")
        @self.pg.production("expression_stmt : expression_stmt tkFloor expression_stmt")
        @self.pg.production("expression_stmt : variable_stmt")
        def expression_stmt(p):
            '''
                Математические выражения
            '''

            match p:
                case left_expression, Token(_) as sign, right_expression:
                    result = f'{left_expression} {sign.value} {right_expression}'

                case [variable]:
                    result = variable

            return result


        @self.pg.production("function_stmt : print_stmt")
        def function_stmt(p):
            '''
                Функции
            '''

            match p:
                case [PRINT]:
                    result = PRINT

            return result

        @self.pg.production("cout_stmt : tkoutop expression_stmt cout_stmt")
        @self.pg.production("cout_stmt : tkoutop expression_stmt")
        @self.pg.production("cout_stmt : tkoutop tkoutend")
        def cout_stmt(p):


            match p:
                case Token('tkoutop'), Token('tkoutend'):
                    result = f"end='\\n'"
                case Token('tkoutop'), content:
                    result = f"{content}"
                case Token('tkoutop'), content, cout:
                    result = f"{content}, {cout}"

            return result



        @self.pg.production("print_stmt : tkPrint tkORoundBr tkCRoundBr ")
        @self.pg.production("print_stmt : tkPrint tkORoundBr expression_stmt tkComma expression_stmt tkCRoundBr ")
        @self.pg.production("print_stmt : tkPrint cout_stmt")
        def print_stmt(p):
            '''
                Функция вывода данных
            '''

            match p:
                case Token('tkPrint'), Token('tkORoundBr'), Token('tkCRoundBr'):
                    result = 'print(\n)'

                case Token('tkPrint'), Token('tkORoundBr'), pattern, Token('tkComma'), content, Token('tkCRoundBr'):
                    result = f"print(\"{content}\")"

                case Token('tkPrint'), cout:
                    result = f"print({cout})"
            return result


        @self.pg.error
        def error_handle(token):
            raise ValueError(token)