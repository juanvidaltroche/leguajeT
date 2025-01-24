import re

# =========================
# ANALIZADOR LÉXICO (LEXER)
# =========================
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
                    tokens.append((token_name, match.group(0)))
                    position = match.end()
                    break

            if not match:
                raise SyntaxError(f"Unexpected character at position {position}: {text[position]}")

        return tokens

# =========================
# ANALIZADOR SINTÁCTICO (PARSER)
# =========================
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
        # Handle simple arithmetic expressions (number [+|- number]*)
        left = self.match("NUMBER")
        while self.current_token() and self.current_token()[0] in ("PLUS", "MINUS"):
            operator = self.match(self.current_token()[0])
            right = self.match("NUMBER")
            left = (operator[1], left, right)
        return left

    def parse(self):
        return self.parse_expression()

# =========================
# REGLAS PARA EL LÉXICO
# =========================
lexer_rules = [
    ("NUMBER", r"\d+"),          # Números enteros
    ("PLUS", r"\+"),            # Operador suma
    ("MINUS", r"-"),            # Operador resta
    ("WHITESPACE", r"\s+"),     # Espacios en blanco (se ignorarán más adelante)
]

# =========================
# EJEMPLO DE USO
# =========================
if __name__ == "__main__":
    code = "42 + 23 - 5"

    # Instanciar y ejecutar el Lexer
    lexer = Lexer(lexer_rules)
    tokens = lexer.tokenize(code)
    tokens = [t for t in tokens if t[0] != "WHITESPACE"]  # Eliminar espacios en blanco
    print("Tokens:", tokens)

    # Instanciar y ejecutar el Parser
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)
