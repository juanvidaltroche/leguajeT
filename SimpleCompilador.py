import re

# Definimos los tipos de tokens y sus expresiones regulares
TOKEN_REGEX = [
    ('NUMBER',   r'\d+'),
    ('ID',       r'[a-zA-Z_]\w*'),
    ('ASSIGN',   r'='),
    ('PLUS',     r'\+'),
    ('MINUS',    r'-'),
    ('MULT',     r'\*'),
    ('DIV',      r'/'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('SKIP',     r'[ \t]+'),  # Espacios y tabulaciones
    ('NEWLINE',  r'\n'),
]

def lexer(code):
    tokens = []
    position = 0
    while position < len(code):
        match = None
        for token_type, regex in TOKEN_REGEX:
            regex = re.compile(regex)
            match = regex.match(code, position)
            if match:
                if token_type != 'SKIP':
                    token = (token_type, match.group(0))
                    tokens.append(token)
                position = match.end(0)
                break
        if not match:
            raise SyntaxError(f'Illegal character at position {position}')
    return tokens

# Ejemplo de uso del lexer
code = """
a = 5
b = 10
c = a + b * 2
d = c - b / a
"""
tokens = lexer(code)
print("Tokens generados:")
print(tokens)

class ASTNode:
    pass

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(ASTNode):
    def __init__(self, value):
        self.value = value

class Var(ASTNode):
    def __init__(self, name):
        self.name = name

class Assign(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        nodes = []
        while self.position < len(self.tokens):
            nodes.append(self.assignment())
        return nodes

    def assignment(self):
        name = self.tokens[self.position][1]
        self.position += 1
        self.eat('ASSIGN')
        value = self.expr()
        return Assign(name, value)

    def expr(self):
        node = self.term()
        while self.current_token() in ('PLUS', 'MINUS'):
            op = self.current_token()
            self.position += 1
            node = BinOp(node, op, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current_token() in ('MULT', 'DIV'):
            op = self.current_token()
            self.position += 1
            node = BinOp(node, op, self.factor())
        return node

    def factor(self):
        token = self.tokens[self.position]
        self.position += 1
        if token[0] == 'NUMBER':
            return Num(int(token[1]))
        elif token[0] == 'ID':
            return Var(token[1])
        elif token[0] == 'LPAREN':
            node = self.expr()
            self.eat('RPAREN')
            return node

    def eat(self, token_type):
        if self.tokens[self.position][0] == token_type:
            self.position += 1
        else:
            raise SyntaxError(f'Expected {token_type}')

    def current_token(self):
        return self.tokens[self.position][0]

# Ejemplo de uso del parser
parser = Parser(tokens)
ast = parser.parse()
print("\nÁrbol de sintaxis abstracta (AST):")
for node in ast:
    print(vars(node))

# Función auxiliar para imprimir el AST de manera más legible
def print_ast(node, level=0):
    indent = '  ' * level
    if isinstance(node, Assign):
        print(f"{indent}Assign(name={node.name}, value=")
        print_ast(node.value, level + 1)
        print(f"{indent})")
    elif isinstance(node, BinOp):
        print(f"{indent}BinOp(left=")
        print_ast(node.left, level + 1)
        print(f"{indent}, op='{node.op}', right=")
        print_ast(node.right, level + 1)
        print(f"{indent})")
    elif isinstance(node, Num):
        print(f"{indent}Num(value={node.value})")
    elif isinstance(node, Var):
        print(f"{indent}Var(name={node.name})")

print("\nAST Legible:")
for node in ast:
    print_ast(node)