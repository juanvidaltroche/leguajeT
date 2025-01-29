import re
from tkinter import Tk, Label, Entry, Button, Text, END, messagebox

# Definición de tokens
TOKENS = [
    ('NUMERO', r'\d+'),           # Números enteros
    ('SUMA', r'\+'),              # Operador suma
    ('RESTA', r'-'),              # Operador resta
    ('MULTIPLICACION', r'\*'),    # Operador multiplicación
    ('DIVISION', r'/'),           # Operador división
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

# Clase para representar nodos del AST
class ASTNode:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type  # Tipo de nodo (NUMERO, SUMA, RESTA, etc.)
        self.value = value  # Valor (solo para números)
        self.left = left  # Hijo izquierdo
        self.right = right  # Hijo derecho

    def __repr__(self):
        if self.type == 'NUMERO':
            return f"ASTNode({self.type}, {self.value})"
        else:
            return f"ASTNode({self.type}, left={self.left}, right={self.right})"

# Clase para el parser
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
        if self.current_token and self.current_token[0] == 'NUMERO':
            value = int(self.current_token[1])
            node = ASTNode('NUMERO', value=value)
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
        while self.current_token and self.current_token[0] in ('MULTIPLICACION', 'DIVISION'):
            op = self.current_token[1]
            self.next_token()
            right = self.factor()
            node = ASTNode(op, left=node, right=right)
        return node

    # Regla para Expr
    def expr(self):
        node = self.term()
        while self.current_token and self.current_token[0] in ('SUMA', 'RESTA'):
            op = self.current_token[1]
            self.next_token()
            right = self.term()
            node = ASTNode(op, left=node, right=right)
        return node

    # Iniciar el análisis
    def parse(self):
        return self.expr()

# Función para evaluar el AST
def evaluate_ast(node):
    if node.type == 'NUMERO':
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

# Función para mostrar el AST en texto
def ast_to_text(node, level=0):
    indent = "  " * level
    if node.type == 'NUMERO':
        return f"{indent}NUMERO({node.value})\n"
    else:
        text = f"{indent}{node.type}\n"
        text += ast_to_text(node.left, level + 1)
        text += ast_to_text(node.right, level + 1)
        return text

# Funciones para la interfaz gráfica
def tokenize():
    input_text = entry.get()
    try:
        tokens = lexer(input_text)
        result_text.delete(1.0, END)
        result_text.insert(END, "Tokens:\n")
        for token in tokens:
            result_text.insert(END, f"{token}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def generate_ast():
    input_text = entry.get()
    try:
        tokens = lexer(input_text)
        parser = Parser(tokens)
        ast = parser.parse()
        result_text.delete(1.0, END)
        result_text.insert(END, "Árbol de Sintaxis Abstracta (AST):\n")
        result_text.insert(END, ast_to_text(ast))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def evaluate():
    input_text = entry.get()
    try:
        tokens = lexer(input_text)
        parser = Parser(tokens)
        ast = parser.parse()
        result = evaluate_ast(ast)
        result_text.delete(1.0, END)
        result_text.insert(END, f"Resultado de la evaluación: {result}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Crear la ventana principal
root = Tk()
root.title("Analizador Léxico y Sintáctico")

# Crear y colocar los widgets
Label(root, text="Ingrese una expresión:").grid(row=0, column=0, padx=10, pady=10)
entry = Entry(root, width=40)
entry.grid(row=0, column=1, padx=10, pady=10)

Button(root, text="Tokenizar", command=tokenize).grid(row=1, column=0, padx=10, pady=10)
Button(root, text="Generar AST", command=generate_ast).grid(row=1, column=1, padx=10, pady=10)
Button(root, text="Evaluar", command=evaluate).grid(row=1, column=2, padx=10, pady=10)

result_text = Text(root, height=20, width=60)
result_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)


# Iniciar la aplicación
root.mainloop()