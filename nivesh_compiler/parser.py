class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', '')

    def eat(self, expected_type=None, expected_value=None):
        token = self.current()
        if expected_type and token[0] != expected_type:
            raise SyntaxError(f'Expected {expected_type}, got {token}')
        if expected_value and token[1] != expected_value:
            raise SyntaxError(f'Expected {expected_value}, got {token}')
        self.pos += 1
        return token

    def parse(self):
        stmts = []
        while self.current()[0] != 'EOF':
            stmts.append(self.statement())
        return ('block', stmts)

    def statement(self):
        token = self.current()
        if token[1] == 'int':
            return self.declaration()
        elif token[1] == 'if':
            return self.if_stmt()
        elif token[1] == 'for':
            return self.for_stmt()
        elif token[1] == 'print':
            return self.print_stmt()
        else:
            return self.assignment()

    def declaration(self):
        self.eat('ID', 'int')
        var = self.eat('ID')[1]
        expr = None
        if self.current()[1] == '=':
            self.eat('OP', '=')
            expr = self.expression()
        self.eat('PUNC', ';')
        return ('decl', var, expr)

    def assignment(self):
        var = self.eat('ID')[1]
        self.eat('OP', '=')
        expr = self.expression()
        self.eat('PUNC', ';')
        return ('assign', var, expr)

    def if_stmt(self):
        self.eat('ID', 'if')
        self.eat('PUNC', '(')
        cond = self.expression()
        self.eat('PUNC', ')')
        self.eat('PUNC', '{')
        then_block = []
        while self.current()[1] != '}':
            then_block.append(self.statement())
        self.eat('PUNC', '}')
        else_block = []
        if self.current()[1] == 'else':
            self.eat('ID', 'else')
            self.eat('PUNC', '{')
            while self.current()[1] != '}':
                else_block.append(self.statement())
            self.eat('PUNC', '}')
        return ('if', cond, ('block', then_block), ('block', else_block))

    def for_stmt(self):
        self.eat('ID', 'for')
        self.eat('PUNC', '(')
        init = self.statement()  # usually a decl or assign ends with ;
        cond = self.expression()
        self.eat('PUNC', ';')
        update_var = self.eat('ID')[1]
        self.eat('OP', '=')
        update_expr = self.expression()
        self.eat('PUNC', ')')
        self.eat('PUNC', '{')
        body = []
        while self.current()[1] != '}':
            body.append(self.statement())
        self.eat('PUNC', '}')
        return ('for', init, cond, (update_var, update_expr), ('block', body))

    def print_stmt(self):
        self.eat('ID', 'print')
        self.eat('PUNC', '(')
        expr = self.expression()
        self.eat('PUNC', ')')
        self.eat('PUNC', ';')
        return ('print', expr)

    def expression(self):
        # Very simple expression parser supporting number, var, and + - * / and comparisons < >
        left = self.term()
        while self.current()[1] in ('+', '-', '<', '>'):
            op = self.eat('OP')[1]
            right = self.term()
            left = ('binop', op, left, right)
        return left

    def term(self):
        left = self.factor()
        while self.current()[1] in ('*', '/'):
            op = self.eat('OP')[1]
            right = self.factor()
            left = ('binop', op, left, right)
        return left

    def factor(self):
        token = self.current()
        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return ('num', int(token[1]))
        elif token[0] == 'ID':
            self.eat('ID')
            return ('var', token[1])
        elif token[1] == '(':
            self.eat('PUNC', '(')
            expr = self.expression()
            self.eat('PUNC', ')')
            return expr
        else:
            raise SyntaxError(f"Unexpected token {token}")
