import sys
import re
import doctest
from dataclasses import dataclass, field
from typing import List, Tuple, Union, Iterable

@dataclass
class Rule:
    lhs: str
    rhs: Tuple[str, ...]

@dataclass
class Node:
    type: str
    value: str = ''
    children: List['Node'] = field(default_factory=list)

    def __repr__(self):
        if self.children:
            return f'({self.type} {" ".join(map(repr, self.children))})'
        return f'{self.value}'

def lex(text: str) -> Iterable[Node]:
    """
    >>> list(lex('1+2'))
    [1, +, 2]
    >>> list(lex('1 $ 2'))
    Traceback (most recent call last):
    ...
    ValueError: Invalid token: $
    """
    token_rules = [
        ('number', r'\d+'),
        ('operator', r'[-+*/]'),
        ('whitespace', r'\s+'),
    ]

    i = 0
    while i < len(text):
        for token_type, rule in token_rules:
            match = re.match(rule, text[i:])
            if match:
                value = match.group()
                if token_type != 'whitespace':
                    yield Node(token_type, value)
                i += len(value)
                break
        else:
            raise ValueError(f'Invalid token: {text[i]}')

def reduce(stack: List[Node], rules: List[Rule]) -> bool:
    """
    >>> rules = [Rule('expr', ('number',)), Rule('expr', ('expr', 'operator', 'expr'))]
    >>> stack = [Node('number', '1')]
    >>> reduce(stack, rules)
    True
    >>> stack
    [(expr 1)]
    >>> stack.extend([Node('operator', '+'), Node('number', '2')])
    >>> reduce(stack, rules)
    True
    >>> stack
    [(expr 1), +, (expr 2)]
    >>> reduce(stack, rules)
    True
    >>> stack
    [(expr (expr 1) + (expr 2))]
    """
    for rule in rules:
        if len(stack) < len(rule.rhs):
            continue
        
        if tuple(node.type for node in stack[-len(rule.rhs):]) == rule.rhs:
            children = stack[-len(rule.rhs):]
            del stack[-len(rule.rhs):]
            stack.append(Node(type=rule.lhs, children=children))
            return True
    return False

def parse(tokens: Iterable[Node], rules: List[Rule], trace: bool = False) -> Node:
    """
    >>> rules = [Rule('expr', ('number',)), Rule('expr', ('expr', 'operator', 'expr'))]
    >>> parse(lex('1 + 2'), rules)
    (expr (expr 1) + (expr 2))
    """
    stack = []
    for token in tokens:
        stack.append(token)
        if trace: print(f'Shift:  {token}')
        
        while reduce(stack, rules):
            if trace: print(f'Reduce: {stack[-1]}')
    
    if len(stack) != 1:
        raise ValueError(f'Invalid Expression: {stack}')
    
    return stack[0]

if __name__ == '__main__':
    doctest.testmod()
    if len(sys.argv) > 1:
        rules = [
            Rule('expr', ('number',)),
            Rule('expr', ('expr', 'operator', 'expr')),
        ]
        print(parse(lex(sys.argv[1]), rules, trace=True))
