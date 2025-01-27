import re


# Lexer
class Lexer:
    def __init__(self, rules):
        self.rules = [(name, re.compile(pattern)) for name, pattern in rules]

    def tokenize(self, text):
        tokens = []
        position = 0

        while position < len(text):
            match = None
            for token_name, token_regex in self.rules:
                match = token_regex.match(text, position)
                if match:
                    if token_name != "WHITESPACE":  # Ignorar espacios
                        tokens.append((token_name, match.group(0)))
                    position = match.end()
                    break
            if not match:
                raise SyntaxError(f"Unexpected character: {text[position]}")
        return tokens


# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def match(self, expected_type):
        token = self.current_token()
        if token and token[0] == expected_type:
            self.position += 1
            return token
        raise SyntaxError(f"Expected {expected_type} but found {token}")

    def parse_expression(self):
        left = self.parse_term()
        while self.current_token() and self.current_token()[0] in ("PLUS", "MINUS"):
            operator = self.match(self.current_token()[0])
            right = self.parse_term()
            left = (operator[1], left, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token() and self.current_token()[0] in ("MULTIPLY", "DIVIDE"):
            operator = self.match(self.current_token()[0])
            right = self.parse_factor()
            left = (operator[1], left, right)
        return left

    def parse_factor(self):
        token = self.current_token()
        if token[0] == "NUMBER":
            return self.match("NUMBER")[1]
        elif token[0] == "IDENTIFIER":
            return self.match("IDENTIFIER")[1]
        elif token[0] == "LPAREN":
            self.match("LPAREN")
            expr = self.parse_expression()
            self.match("RPAREN")
            return expr
        raise SyntaxError(f"Unexpected token: {token}")

    def parse_assignment(self):
        identifier = self.match("IDENTIFIER")[1]
        self.match("ASSIGN")
        expression = self.parse_expression()
        return ("assign", identifier, expression)

    def parse_print(self):
        self.match("PRINT")
        identifier = self.match("IDENTIFIER")[1]
        return ("print", identifier)

    def parse(self):
        statements = []
        while self.current_token():
            if self.current_token()[0] == "IDENTIFIER":
                statements.append(self.parse_assignment())
            elif self.current_token()[0] == "PRINT":
                statements.append(self.parse_print())
            else:
                raise SyntaxError(f"Unexpected token: {self.current_token()}")
        return statements


# Code Generator
class AssemblyCodeGenerator:
    def __init__(self):
        self.instructions = []
        self.variables = {}
        self.variable_count = 0

    def allocate_variable(self, name):
        if name not in self.variables:
            self.variables[name] = f"[rbp-{8 * (self.variable_count + 1)}]"
            self.variable_count += 1
        return self.variables[name]

    def generate_expression(self, expr):
        if isinstance(expr, tuple):
            operator, left, right = expr
            self.generate_expression(left)
            self.instructions.append("push rax")
            self.generate_expression(right)
            self.instructions.append("pop rbx")
            if operator == "+":
                self.instructions.append("add rax, rbx")
            elif operator == "-":
                self.instructions.append("sub rax, rbx")
            elif operator == "*":
                self.instructions.append("imul rax, rbx")
            elif operator == "/":
                self.instructions.append("mov rdx, 0")
                self.instructions.append("div rbx")
        else:
            if expr.isdigit():
                self.instructions.append(f"mov rax, {expr}")
            else:
                var_addr = self.variables.get(expr)
                if not var_addr:
                    raise RuntimeError(f"Variable no definida: {expr}")
                self.instructions.append(f"mov rax, qword {var_addr}")

    def generate(self, ast):
        self.instructions.append("section .data")
        self.instructions.append("section .bss")
        self.instructions.append("section .text")
        self.instructions.append("global _start")
        self.instructions.append("_start:")

        for statement in ast:
            if statement[0] == "assign":
                _, identifier, expression = statement
                self.generate_expression(expression)
                var_addr = self.allocate_variable(identifier)
                self.instructions.append(f"mov qword {var_addr}, rax")
            elif statement[0] == "print":
                _, identifier = statement
                var_addr = self.variables.get(identifier)
                if not var_addr:
                    raise RuntimeError(f"Variable no definida: {identifier}")
                self.instructions.append(f"mov rax, qword {var_addr}")
                self.instructions.append("call print_number")

        self.instructions.append("mov rax, 60")
        self.instructions.append("xor rdi, rdi")
        self.instructions.append("syscall")

        self.instructions.append("""
print_number:
    ; código para imprimir un número
    ret
        """)

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            f.write("\n".join(self.instructions))



# Programa principal
if __name__ == "__main__":
    code = """
    a = 10
    b = 20
    c = a + b * 2
    
    """
    rules = [
        ("NUMBER", r"\d+"),
        ("IDENTIFIER", r"[a-zA-Z_]\w*"),
        ("ASSIGN", r"="),
        ("PLUS", r"\+"),
        ("MINUS", r"-"),
        ("MULTIPLY", r"\*"),
        ("DIVIDE", r"/"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("PRINT", r"print"),
        ("WHITESPACE", r"\s+"),
    ]

    lexer = Lexer(rules)
    tokens = lexer.tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()

    generator = AssemblyCodeGenerator()
    generator.generate(ast)

    output_file = "program.asm"
    generator.write_to_file(output_file)
    print(f"Código ensamblador generado en: {output_file}")


