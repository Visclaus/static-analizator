import re
from collections import namedtuple
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class IntegerOverflowHandler(BaseHandler):
    vulnerability_name = 'Переполнение целых чисел'
    Limit = namedtuple('Limit', 'min max')
    Variable = namedtuple('Variable', 'type value')
    int_types = ["int", "short", "char", "long", "byte"]
    regex_arithmetic = r"^\s*([\w:<>]*)\s*=\s*([\w:<>]+|\d)\s*(\+|\-|\*|\/)?\s*([\w:<>]+|\d).*;"
    limits = {'int': Limit(-2 ** 31, 2 ** 31 - 1),
              'byte': Limit(-2 ** 15, 2 ** 15 - 1),
              'short': Limit(-2 ** 15, 2 ** 15 - 1),
              'char': Limit(-2 ** 7, 2 ** 7 - 1),
              'long': Limit(-2 ** 63, 2 ** 63 - 1)}

    def __init__(self):
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        """
        Проверяет переполнение объявленных переменных, учавствующих в арифметических операциях
        """
        for context in contexts:
            variables = {}
            declared_vars = context.variables.copy()
            int_vars = []
            for i in declared_vars:
                if i.var_type in self.int_types:
                    int_vars.append(i)

            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                arithmetic_matches = re.finditer(self.regex_arithmetic, processed_line, re.IGNORECASE)
                for matchNum, match in enumerate(arithmetic_matches):
                    left = None
                    right = None
                    if match.group(2).isdigit():
                        left = int(match.group(2))
                    else:
                        for i in int_vars:
                            if i.var_name == match.group(2): left = int(i.value)
                    if match.group(4).isdigit():
                        right = int(match.group(4))
                    else:
                        for ind in int_vars:
                            if ind.var_name == match.group(4): right = int(ind.value)
                    if match.group(3) == '*':
                        tmp = left * right
                    elif match.group(3) == '+':
                        tmp = left + right
                    elif match.group(3) == '-':
                        tmp = left - right
                    else:
                        tmp = left // right
                    tmp_var = None
                    for k in int_vars:
                        if k.var_name == match.group(1):
                            k.value = tmp
                            tmp_var = k
                    try:
                        assert (self.limits[tmp_var.var_type].min <= int(tmp_var.value) <=
                                self.limits[tmp_var.var_type].max)
                    except AssertionError:
                        error_details = ""
                        self.output.append(f"Угроза в методе {context.name}!\n"
                                           f"Переполнение целых чисел ({cur_line_number}) у переменной {error_details}\n")
        return self.output
