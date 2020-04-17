import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class RandomGenHandler(BaseHandler):
    def __init__(self):
        self.vulnerability_name = 'Non crypto-safe RNG'
        self.pattern = r'rand\(\)|uniform_real_distribution'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                matches = re.finditer(self.pattern, processed_line, re.IGNORECASE)
                for _ in matches:
                    self.output.append(f"WARNING in function {context.name}! "
                                       f"Usage of non crypto-safe Random Generator (line {cur_line_number})")
        return self.output
