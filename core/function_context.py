from core.base_context import BaseContext


class FunctionContext(BaseContext):
    def __init__(self):
        self.return_type = None
        self.parameters = []
        self.variables = []
        self.threads = []
        self.source_code = []
