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
        for context in contexts:
            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                matches = re.finditer(self.pattern, processed_line, re.IGNORECASE)
                for _ in matches:
                    self.output.append(f"Предупреждение в методе <{context.name}>!\n"
                                       f"Возможна ошибка форматной строки (строка {cur_line_number})\n")

        return self.output
