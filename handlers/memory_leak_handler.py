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
        for context in contexts:
            m_vars = []
            for var in context.variables:
                if var.value is not None:
                    if "new" in var.value:
                        m_vars.append(var)
            free_matches = []
            for line in context.source_code:
                processed_line = list(line.keys())[0]
                matches = re.finditer(self.pattern, processed_line, re.IGNORECASE)
                free_matches += matches
            for var in m_vars:
                if var.var_name not in list(map(lambda x: x.group(1)[1:-1].strip(), free_matches)):
                    self.output.append(f"Угроза в методе <{context.name}>!\n"
                                       f"Отсутствует высвобождение памяти для переменной <{var.var_name}> (строка {var.line_appeared})")

        return self.output
