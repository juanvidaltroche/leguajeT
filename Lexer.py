import re

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