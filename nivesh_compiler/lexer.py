import re

class Lexer:
    def __init__(self, code):
        self.code = code

    def tokenize(self):
        token_specification = [
            ('NUMBER',   r'\d+'),
            ('ID',       r'[A-Za-z_]\w*'),
            ('OP',       r'[+\-*/=<>]'),
            ('PUNC',     r'[{}();]'),
            ('SKIP',     r'[ \t\n]+'),
            ('MISMATCH', r'.'),
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        tokens = []
        for mo in re.finditer(tok_regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NUMBER':
                tokens.append(('NUMBER', value))
            elif kind == 'ID':
                tokens.append(('ID', value))
            elif kind == 'OP':
                tokens.append(('OP', value))
            elif kind == 'PUNC':
                tokens.append(('PUNC', value))
            elif kind == 'SKIP':
                continue
            else:
                raise SyntaxError(f'Unexpected character {value}')
        return tokens
