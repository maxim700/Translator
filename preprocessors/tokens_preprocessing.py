from analyzers.Token import Token


def py_tokens_preprocessing(tokens):
    res = []
    buf = []

    deep = 0
    count = 0

    for token in tokens:
        if token.name == 'tkSpace': continue
        if token.name == 'tkColon': continue

        if token.name == 'tkTab':
            count+=1
            continue
        
        if token.name == 'tkNewline':
            if not len(buf): continue

            if count>deep:
                res.append(Token('tkOCurlyBr', '{'))
                deep += 1

            elif count<deep:
                while deep>count:
                    res.append(Token('tkCCurlyBr', '}'))
                    deep -=1

            for i in buf:
                res.append(Token(i.name, i.value))

            buf.clear()
            count = 0

            continue

        buf.append(token)

    for i in range(deep,0,-1):
        res.append(Token('tkCCurlyBr', '}'))

    return res

def c_tokens_preprocessing(tokens):
    res = []

    for token in tokens:
        if token.name == 'tkSpace': continue
        if token.name == 'tkColon': continue
        if token.name == 'tkSemiColon': continue
        if token.name == 'tkNewline': continue
        if token.name == 'tkTab': continue

        res.append(Token(token.name, token.value))
    return res