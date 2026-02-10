import sys
import re
import doctest
from dataclasses import dataclass, field
from typing import List, Tuple, Union, Iterable

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
    >>> list(lex('1 + 2'))
    [1, +, 2]
    """
    for v in text.split():
        if re.match(r'\d+', v):
            yield Node(type='number', value=v)
        elif re.match(r'[\+\-\*\/]', v):
            yield Node(type='operator', value=v)
        elif re.match('!', v):
            yield Node(type='postfix_unary_operator', value=v)
        else:
            raise ValueError(f'Invalid token: {v}')

def reduce(stack: List[Node], rules: List[Tuple[str, Tuple[str, ...]]]) -> bool:
    """
    >>> rules = [('expr', ('number', 'operator', 'number'))]
    >>> stack = [Node('number', '1'), Node('operator', '+'), Node('number', '2')]
    >>> reduce(stack, rules)
    True
    >>> stack
    [(expr 1 + 2)]
    """
    for lhs, rhs in rules:
        if len(stack) < len(rhs):
            continue
        
        stack_types = tuple(node.type for node in stack[-len(rhs):])
        if stack_types == rhs:
            children = [stack.pop() for _ in range(len(rhs))]
            new_node = Node(type=lhs, children=list(reversed(children)))
            stack.append(new_node)
            return True
    return False

def parse(tokens: Iterable[Node], rules: List[Tuple[str, Tuple[str, ...]]]) -> Node:
    """
    >>> rules = [('number', ('number', 'operator', 'number'))]
    >>> parse(lex('1 + 2'), rules)
    (number 1 + 2)
    """
    stack = []
    for token in tokens:
        stack.append(token)
        while reduce(stack, rules):
            pass
    
    if len(stack) != 1:
        raise ValueError('Invalid Expression')
    
    return stack[0]

if __name__ == '__main__':
    doctest.testmod()
    if len(sys.argv) > 1:
        rules = [
            ('number', ('number', 'operator', 'number')),
            ('number', ('number', 'postfix_unary_operator')),
        ]
        print(parse(lex(sys.argv[1]), rules))
