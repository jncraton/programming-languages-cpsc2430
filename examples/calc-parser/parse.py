import sys
import re
import doctest

import pprint
pp = pprint.PrettyPrinter(indent=2)

def lex_one(value):
    """
    >>> lex_one('123')
    ('number', '123')
    >>> lex_one('+')
    ('operator', '+')
    >>> lex_one('!')
    ('postfix_unary_operator', '!')
    """
    if re.match(r'\d+', value):
        return ('number', value)
    elif re.match(r'[\+\-\*\/]', value):
        return ('operator', value)
    elif re.match('!', value):
        return ('postfix_unary_operator', value)
    else:
        raise ValueError(f'Invalid token: {value}')

def lex(text):
    """
    >>> list(lex('1 + 2'))
    [(0, 'number', '1'), (1, 'operator', '+'), (2, 'number', '2')]
    """
    for i, v in enumerate(text.split()):
        token = lex_one(v)
        yield (i, token[0], token[1])

def reduce(parse_tree, rules):
    """
    >>> rules = [('number', ('number', 'operator', 'number'))]
    >>> tree = [[(0, 'number', '1')], [(1, 'operator', '+')], [(2, 'number', '2')]]
    >>> reduce(tree, rules)
    True
    >>> tree
    [[(1, 'number'), [(0, 'number', '1')], [(1, 'operator', '+')], [(2, 'number', '2')]]]
    """
    for lhs, rhs in rules:
        if tuple([t[0][1] for t in parse_tree[-len(rhs):]]) == rhs:
            # Create new root
            root = (parse_tree[1][0][0], lhs)
            children = reversed([parse_tree.pop() for i in range(len(rhs))])

            parse_tree.append([root] + list(children))
            return True

def parse(tokens, rules):
    """
    >>> rules = [('number', ('number', 'operator', 'number'))]
    >>> parse(lex('1 + 2'), rules)
    [[(1, 'number'), [(0, 'number', '1')], [(1, 'operator', '+')], [(2, 'number', '2')]]]
    """
    
    parse_tree = []

    for token in tokens:
        # Shift token on to parse tree
        parse_tree.append([token])

        # Reduce tokens matching production rules
        while reduce(parse_tree, rules): pass
            

    if len(parse_tree) != 1:
        raise ValueError('Invalid Expression')

    return parse_tree

if __name__ == '__main__':
    doctest.testmod()
    if len(sys.argv) > 1:
        rules = [
            ('number', ('number', 'operator', 'number')),
            ('number', ('number', 'postfix_unary_operator')),
        ]
        
        pp.pprint(parse(lex(sys.argv[1]), rules))
