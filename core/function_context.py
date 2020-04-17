from typing import List

from core.base_context import BaseContext
from core.variable import Variable


class FunctionContext(BaseContext):
    def __init__(self):
        self.return_type = None
        self.parameters = []
        self.variables: List[Variable] = []
        self.threads = []
        self.source_code = []
