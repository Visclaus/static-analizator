import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class FormatStringHandler(BaseHandler):
    def __init__(self):
        self.vulnerability_name = 'Format String'
        self.pattern = r'(printf[(][a-zA-Z0-9_]*)([)])'  # TODO: improve to parse cases with whitespaces, maybe find another regex for this vuln
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            for line in context.source_code:
                for key in line:
                    matches = re.finditer(self.pattern, key, re.IGNORECASE)
                    for _ in matches:
                        self.output.append(f"WARNING in function {context.name}! "
                                           f"Possible format string vulnerable (line {line[key]})")
        return self.output
