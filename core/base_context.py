
class BaseContext:
    def __init__(self):
        self.name = ""  # func or class
        self.variables = []
        self.threads = []
        self.source_code = []

    def parse(self, cpp_code):
        pass

