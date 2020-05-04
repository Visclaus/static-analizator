import re
from typing import List
from core.base_handler import BaseHandler
from core.function_context import FunctionContext
from utils import constants


class IntegerOverflowHandler(BaseHandler):
    vulnerability_name = 'Переполнение целых чисел'

    def __init__(self):
        self.output = []
        self.regex_arithmetic = r"^\s*([\w:<>]*)\s*=\s*([\w:<>]+|\d)\s*(\+|\-|\*|\/)?\s*([\w:<>]+|\d).*;"

    def parse(self, contexts: List[FunctionContext]):
        """
        Проверяет переполнение объявленных переменных, учавствующих в арифметических операциях
        """
        total_errors = 0
        for context in contexts:
            declared_vars = context.variables.copy()
            int_vars = []
            for i in declared_vars:
                if i.var_type in constants.int_types:
                    int_vars.append(i)

            for line_number, line in context.source_code.items():
                arithmetic_matches = re.finditer(self.regex_arithmetic, line, re.IGNORECASE)
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
                        assert (constants.integer_limits[tmp_var.var_type].min <= int(tmp_var.value) <=
                                constants.integer_limits[tmp_var.var_type].max)
                    except AssertionError:
                        total_errors += 1
                        self.output.append(f"{total_errors}) Угроза в методе {context.name}!\n"
                                           f"Переполнение челочисленной переменной <{tmp_var.var_name}> типа "
                                           f"<{tmp_var.var_type}> (строка {line_number}) "
                                           f"Выход за границы типа!")
        self.output.append(self.vulnerability_name + ": " + str(total_errors))
        return self.output
