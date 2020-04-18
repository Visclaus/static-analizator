import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class RandomGeneratorHandler(BaseHandler):

    vulnerability_name = 'Non crypto-safe random generation'

    def __init__(self):
        self.pattern = [r'srand\((.*?)\)', r'rand\(\)|uniform_real_distribution']
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        """
        1)Находит использование функции генерации srand(), в случаях когда она инициализирована const числовым значением
        2)Находит использование небезопасных функций генерации rand() и uniform_real_distribution
        """
        for context in contexts:
            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                srand_matches = re.finditer(self.pattern[0], processed_line, re.IGNORECASE)
                for match in srand_matches:
                    if match.group(1).isdigit():
                        self.output.append(f"WARNING in function {context.name}! "
                                           f"Usage of srand() generator initialized with constant seed value - "
                                           f"{match.group(1)} (at line {cur_line_number})")
                rand_matches = re.finditer(self.pattern[1], processed_line, re.IGNORECASE)
                for match in rand_matches:
                    self.output.append(f"WARNING in function {context.name}! "
                                       f"Usage of non crypto-safe {match.group(0)} (line {cur_line_number})")
        return self.output
