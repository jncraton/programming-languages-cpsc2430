import sys
import re

def lex_one(value):
    if re.match('\d+', value):
        return ('number', value)
    elif re.match('[\+\-\*\/]', value):
        return ('operator', value)
    else:
        raise ValueError(f'Invalid token: {value}')

def lex(text):
    return [lex_one(v) for v in text.split()]

print(lex(sys.argv[1]))
