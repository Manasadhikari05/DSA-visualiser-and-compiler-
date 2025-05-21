class CodeGenerator:
    def __init__(self):
        self.output = []
        self.ir = []
        self.temp_counter = 0

    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def generate(self, node):
        nodetype = node[0]

        if nodetype == 'block':
            code = ''
            for stmt in node[1]:
                line = self.generate(stmt)
                if line:
                    code += line + '\n'
            return code.strip()

        if nodetype == 'decl':
            var, expr = node[1], node[2]
            if expr is not None:
                result = self.generate(expr)
                self.ir.append(f"{var} = {result}")
                return f"{var} = {result}"
            else:
                self.ir.append(f"{var} = 0")
                return f"{var} = 0"

        if nodetype == 'assign':
            var, expr = node[1], node[2]
            result = self.generate(expr)
            self.ir.append(f"{var} = {result}")
            return f"{var} = {result}"

        if nodetype == 'if':
            cond = self.generate(node[1])
            then_block = self.generate(node[2])
            else_block = self.generate(node[3]) if node[3][1] else None

            # IR code for conditional jump
            self.ir.append(f"if {cond} goto L1")
            self.ir.append("goto L2")
            self.ir.append("L1:")
            self.ir.append(then_block)
            if else_block:
                self.ir.append("L2:")
                self.ir.append(else_block)
            else:
                self.ir.append("L2:")

            # Python code generation
            code = f"if {cond}:\n"
            code += self.indent(then_block)
            if else_block:
                code += f"\nelse:\n{self.indent(else_block)}"
            return code

        if nodetype == 'for':
            init = self.generate(node[1])
            cond = self.generate(node[2])
            update_var, update_expr = node[3]
            update_code = f"{update_var} = {self.generate(update_expr)}"
            body = self.generate(node[4])

            # IR code for loop
            self.ir.append(init)
            self.ir.append("L1:")
            self.ir.append(f"if not {cond} goto L2")
            self.ir.append(body)
            self.ir.append(update_code)
            self.ir.append("goto L1")
            self.ir.append("L2:")

            # Python code generation using while loop
            code = f"{init}\nwhile {cond}:\n"
            code += self.indent(body)
            code += '\n' + self.indent(update_code)
            return code

        if nodetype == 'print':
            expr = self.generate(node[1])
            self.ir.append(f"print {expr}")
            return f"print({expr})"

        if nodetype == 'binop':
            op, left, right = node[1], node[2], node[3]
            l = self.generate(left)
            r = self.generate(right)
            expr = f"({l} {op} {r})"   # Inline expression for Python code
            temp = self.new_temp()
            self.ir.append(f"{temp} = {expr}")  # temp used only in IR
            return expr  # Return inline expr so Python code is valid

        if nodetype == 'num':
            return str(node[1])

        if nodetype == 'var':
            return node[1]

        return ''

    def indent(self, code):
        return '\n'.join('    ' + line for line in code.split('\n') if line.strip())

    def get_ir(self):
        return self.ir
