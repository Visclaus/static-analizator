from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext
from core.variable import *


class MemoryLeakHandler(BaseHandler):
    vulnerability_name = 'Ошибка высвобождения памяти'

    def __init__(self):
        self.pattern = r'^\s*delete(\(.*\))'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        total_errors = 0
        for context in contexts:
            m_vars = []
            for var in context.variables:
                if var.value is not None:
                    if "new" in var.full_declaration:
                        m_vars.append(var)
            free_matches = []
            for _, line in context.source_code.items():
                matches = re.finditer(self.pattern, line, re.IGNORECASE)
                free_matches += matches
            for var in m_vars:
                if var.var_name not in list(map(lambda x: x.group(1)[1:-1].strip(), free_matches)):
                    total_errors += 1
                    self.output.append(f"{total_errors}) Угроза в методе <{context.name}>!\n"
                                       f"Отсутствует высвобождение памяти для переменной <{var.var_name}> (строка {var.line_appeared})")
        self.output.append(self.vulnerability_name + ": " + str(total_errors))
        return self.output
