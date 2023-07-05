CRegExList = [
    r'\n', # Новая строка
    r'\s{4}', # Табуляция
    r'\s', # Пробел

    r'cout', #
    r'cin', #

    r'int', # integer
    r'float|double', # float
    r'char\[[0-9]*\]', # string
    r'int', # boolean

    r'\;', # ;
    r'\:', # :
    r'\,', # ,
    r'\.', # .

    r'\(', r'\)', # ( )
    r'\[', r'\]', # [ ]
    r'\{', r'\}', # { }

    r'[-+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)', #
    r'[-+]?(\d+([.,]\d*)?|[.,]\d+)([eE][-+]?\d+)?', #
    r'[\'\"].*[\'\"]', #
    r'1|0', #

    r'\*\*\=', # **=
    r'\+\=', # +=
    r'\-\=', # -=
    r'\*\=', # *=
    r'\/\=', # /=
    r'\%\=', # %=
    r'\/\/\=', # //=

    r'\*\*', # **
    r'\+', # + 
    r'\-', # -
    r'\*', # *
    r'\/', # /
    r'\%', # %
    r'\/\/', # //

    r'<<',
    r'endl',

    r'\=\=', # ==
    r'\!\=', # !=
    r'\>\=', # >=
    r'\<\=', # <=
    r'\<', # <
    r'\>', # >

    r'\=', # =

    r'\&\&', # and
    r'\|\|', # or
    r'\!', # not

    # r'False', # False
    # r'True', # True

    r'if', # if
    r'else if', # elif
    r'else', # else

    r'for', # for
    r'in',
    r'range', # range
    r'while', # while
    r'continue', # continue
    r'break', # break

    r'free', # del

    r'None', # None

    r'[a-zA-Z_][a-zA-Z0-9_]*' # Идентификатор переменной
]