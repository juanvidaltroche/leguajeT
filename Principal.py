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



# Programa principal
if __name__ == "__main__":
    code = """
    a = 10
    b = 20
    c = 0
    c = a + b * 2
    print c
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
    print("lexer:", lexer)
    print("\n")
    print("tokens:", tokens)
    print("\n")
    print("parser:", parser)
    print("\n")
    print("AST:", ast)

   


