from typing import List
from core import main_code_parser
from core.base_handler import BaseHandler
from core.variable import *
from core.function_context import FunctionContext


class BufferOverflowHandler(BaseHandler):

    vulnerability_name = 'Переполнение буфера'

    def __init__(self):
        self.pattern = r"(strcpy|printf|strcat|memcpy|gets|sprintf|vsprintf|strncpy|scanf)" \
                       r"\(.*\)"
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            declared_variables = context.variables
            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                matches = re.finditer(self.pattern, processed_line)
                for match in matches:
                    used_variables = main_code_parser.get_parameters(match.group(0), declared_variables)
                    for used_variable in used_variables:
                        declaration = used_variable.full_declaration
                        if is_pointer(declaration) or is_array(declaration):
                            self.output.append(
                                f"Предупреждение в методе <{context.name}>!\n"
                                f"Использование буфера <{declaration[:-1]}> (строка {used_variable.line_appeared}) "
                                f"в небезопасной функции <{match.group(1)}> (строка {cur_line_number}).\n"
                                f"Это может стать причиной переполнения буфера. "
                                f"Убедитесь в наличии проверки этой угрозы!\n")

        return self.output
