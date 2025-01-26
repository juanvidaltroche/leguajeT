if __name__ == "__main__":
    # Código fuente
    code = """
    a = 10
    b = 20
    c = a + b * 2
    print c
    """

    # Reglas del lexer
    rules = [
        ("NUMBER", r"\\d+"),
        ("IDENTIFIER", r"[a-zA-Z_]\\w*"),
        ("ASSIGN", r"="),
        ("PLUS", r"\\+"),
        ("MINUS", r"-"),
        ("MULTIPLY", r"\\*"),
        ("DIVIDE", r"/"),
        ("LPAREN", r"\\("),
        ("RPAREN", r"\\)"),
        ("PRINT", r"print"),
        ("WHITESPACE", r"\\s+"),
    ]

    # Fases del compilador
    lexer = Lexer(rules)
    tokens = lexer.tokenize(code)
    print("Tokens:", tokens)

    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)

    generator = CodeGenerator()
    generator.generate(ast)
    print("Código generado:")
    print("\\n".join(generator.instructions))
