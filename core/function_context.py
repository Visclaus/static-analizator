from collections import OrderedDict
from typing import List
from core.variable import Variable


class FunctionContext:
    def __init__(self, return_type, name, parameters):
        self.return_type = return_type
        self.name = name
        self.parameters: List[Variable] = parameters
        self.variables: List[Variable] = []
        self.threads = []
        self.source_code = OrderedDict()
