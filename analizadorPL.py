import re

# Definición de tokens
TOKENS = [
    ('NUMBER', r'\d+'),           # Números enteros
    ('PLUS', r'\+'),              # Operador suma
    ('MINUS', r'-'),              # Operador resta
    ('MULTIPLY', r'\*'),          # Operador multiplicación
    ('DIVIDE', r'/'),             # Operador división
    ('LPAREN', r'\('),            # Paréntesis izquierdo
    ('RPAREN', r'\)'),            # Paréntesis derecho
    ('SKIP', r'[ \t]+'),          # Espacios en blanco (ignorar)
    ('MISMATCH', r'.'),           # Cualquier otro carácter no válido
]

# Función para generar tokens
def lexer(input_text):
    tokens = []
    while input_text:
        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(input_text)
            if match:
                value = match.group(0)
                if token_type != 'SKIP':  # Ignorar espacios
                    tokens.append((token_type, value))
                input_text = input_text[match.end():]  # Avanzar en el texto
                break
        else:
            raise SyntaxError(f"Carácter no válido: {input_text[0]}")
    return tokens

class ASTNode:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type  # Tipo de nodo (NUMBER, PLUS, MINUS, etc.)
        self.value = value  # Valor (solo para números)
        self.left = left  # Hijo izquierdo
        self.right = right  # Hijo derecho

    def __repr__(self):
        if self.type == 'NUMBER':
            return f"ASTNode({self.type}, {self.value})"
        else:
            return f"ASTNode({self.type}, left={self.left}, right={self.right})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.next_token()

    # Avanzar al siguiente token
    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = None

    # Verificar si el token actual coincide con el tipo esperado
    def expect(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.next_token()
        else:
            raise SyntaxError(f"Se esperaba {token_type}, pero se encontró {self.current_token}")

    # Regla para Factor
    def factor(self):
        if self.current_token and self.current_token[0] == 'NUMBER':
            value = int(self.current_token[1])
            node = ASTNode('NUMBER', value=value)
            self.next_token()
            return node
        elif self.current_token and self.current_token[0] == 'LPAREN':
            self.expect('LPAREN')
            node = self.expr()  # Procesar la expresión dentro del paréntesis
            self.expect('RPAREN')
            return node
        else:
            raise SyntaxError("Factor inválido")

    # Regla para Term
    def term(self):
        node = self.factor()
        while self.current_token and self.current_token[0] in ('MULTIPLY', 'DIVIDE'):
            op = self.current_token[1]
            self.next_token()
            right = self.factor()
            node = ASTNode(op, left=node, right=right)
        return node

    # Regla para Expr
    def expr(self):
        node = self.term()
        while self.current_token and self.current_token[0] in ('PLUS', 'MINUS'):
            op = self.current_token[1]
            self.next_token()
            right = self.term()
            node = ASTNode(op, left=node, right=right)
        return node

    # Iniciar el análisis
    def parse(self):
        return self.expr()
    


# Visualizar el AST
def print_ast(node, level=0):
    indent = "  " * level
    if node.type == 'NUMBER':
        print(f"{indent}NUMBER({node.value})")
    else:
        print(f"{indent}{node.type}")
        print_ast(node.left, level + 1)
        print_ast(node.right, level + 1)
# Evaluar el AST
def evaluate_ast(node):
    if node.type == 'NUMBER':
        return node.value
    elif node.type == '+':
        return evaluate_ast(node.left) + evaluate_ast(node.right)
    elif node.type == '-':
        return evaluate_ast(node.left) - evaluate_ast(node.right)
    elif node.type == '*':
        return evaluate_ast(node.left) * evaluate_ast(node.right)
    elif node.type == '/':
        return evaluate_ast(node.left) / evaluate_ast(node.right)
    else:
        raise ValueError(f"Operación no soportada: {node.type}")






# Ejemplo de uso
input_text = "(1+2)*(4-3)"
tokens = lexer(input_text)
parser = Parser(tokens)
ast = parser.parse()

# Mostrar el AST
print(ast)
print_ast(ast)
result = evaluate_ast(ast)
print(f"Resultado de la evaluación: {result}")

