class CodeGenerator:
    def __init__(self):
        self.instructions = []

    def generate_expression(self, expr):
        if isinstance(expr, tuple):
            operator, left, right = expr
            self.generate_expression(left)
            self.generate_expression(right)
            if operator == "+":
                self.instructions.append("ADD")
            elif operator == "-":
                self.instructions.append("SUB")
            elif operator == "*":
                self.instructions.append("MUL")
            elif operator == "/":
                self.instructions.append("DIV")
        else:
            self.instructions.append(f"PUSH {expr}")

    def generate(self, ast):
        for statement in ast:
            if statement[0] == "assign":
                _, identifier, expression = statement
                self.generate_expression(expression)
                self.instructions.append(f"STORE {identifier}")
            elif statement[0] == "print":
                _, identifier = statement
                self.instructions.append(f"LOAD {identifier}")
                self.instructions.append("PRINT")
