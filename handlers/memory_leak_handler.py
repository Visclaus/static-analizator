from typing import List

from core import main_code_parser
from core.base_handler import BaseHandler
from core.variable import *
from core.function_context import FunctionContext


class BufferOverflowHandler(BaseHandler):
    def __init__(self):
        self.vulnerability_name = 'Buffer Overflow'
        self.pattern = r'(strcpy|printf|strcat|memcpy|gets|sprintf|vsprintf|strncpy|scanfs|sscanf|snscanf|strlen)\((.*)\)'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            declared_variables = context.variables
            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                matches = re.finditer(self.pattern, processed_line, re.IGNORECASE)
                for match in matches:
                    parameters = main_code_parser.get_parameters(match.group(0), declared_variables)
                    for parameter in parameters:
                        declaration = parameter.full_declaration
                        is_p = is_pointer(declaration)
                        is_a = is_array(declaration)
                        if parameter.var_name in list(map(lambda x: x.var_name, declared_variables)) and (is_a or is_p):
                            self.output.append(
                                f"WARNING in function {context.name}! "
                                f"Usage of buffer \"{declaration}\" (line {parameter.line_appeared}) "
                                f"in unsafe function {match.group(1)} (line {cur_line_number}).\n"
                                f"It may cause overflow of the buffer!\n")

        return self.output