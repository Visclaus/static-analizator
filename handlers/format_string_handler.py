import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class FormatStringHandler(BaseHandler):
    vulnerability_name = 'Ошибка форматной строки'

    def __init__(self):
        self.pattern = r'(printf\(.*)\)'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        total_errors = 0
        for context in contexts:
            for line_number, line in context.source_code.items():
                matches = re.finditer(self.pattern, line, re.IGNORECASE)
                for _ in matches:
                    total_errors += 1
                    self.output.append(f"Предупреждение в методе <{context.name}>!\n"
                                       f"Возможна ошибка форматной строки (строка {line_number})\n")
        self.output.append(self.vulnerability_name + ": " + str(total_errors))
        return self.output
