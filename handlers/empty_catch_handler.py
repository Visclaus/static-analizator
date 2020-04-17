import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class EmptyCatchHandler(BaseHandler):
    def __init__(self):
        self.vulnerability_name = 'Empty Catch Block'
        self.pattern = r'\s*catch\s*\(.*\)\s*'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            for line in context.source_code:
                for key in line:
                    matches = re.finditer(self.pattern, key, re.IGNORECASE)
                    #как проверить следующую линию кода на то что она пустая?
                    for _ in matches:
                        self.output.append(f"WARNING in function {context.name}! (line {line[key]}) "
                                           f"No handling of exception! Ignoring an exception can cause the program to "
                                           f"overlook unexpected states and conditions\n")
        return self.output
