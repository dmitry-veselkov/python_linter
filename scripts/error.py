class Error:
    def __init__(self, style: str, key: str, line_number: int):
        self.key = key
        self.line_number = line_number
        self.style = style
