import re

from core import base_parser
from core.base_parser import BaseParser
from core.variable import *


class BufferOverflowHandler(BaseParser):
    def __init__(self, analyzer_context):
        super().__init__(analyzer_context)
        self.vulnerability_name = 'Buffer Overflow'
        self.pattern = r'(strcpy|printf|strcat|memcpy|gets|sprintf|vsprintf|strncpy|scanfs|sscanf|snscanf|strlen)\((.*)\)'
        self.output = []

    def parse(self, source_code):
        cur_line_number = 0
        declared_variables = self.analyzer_context.declared_variables
        for line in source_code:
            cur_line_number += 1
            matches = re.finditer(self.pattern, line, re.IGNORECASE)
            for match in matches:
                parameters = self.analyzer_context.get_parameters(match.group(0))
                for var in declared_variables:
                    for parameter in parameters:
                        if var.var_name == parameter.var_name and (
                                is_pointer(var.full_declaration) or is_array(var.full_declaration)):
                            self.output.append(
                                base_parser.warning(cur_line_number, str(line), self.vulnerability_name, 'WARNING',
                                                    f'Usage of buffer \"{var.full_declaration}\" (line {var.line_appeared}) in unsafe function {match.group(1)} (line {cur_line_number}).\nIt may cause overflow of the buffer!'))
        return self.output
