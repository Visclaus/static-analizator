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
                for key in line:
                    matches = re.finditer(self.pattern, key, re.IGNORECASE)
                    for _ in matches:
                        self.output.append(f"WARNING in function {context.name}! "
                                           f"Usage of non crypto-safe Random Generator (line {line[key]})")
        return self.output
