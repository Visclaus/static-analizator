import re
from collections import namedtuple
from typing import List

from core import base_handler
from core.base_handler import BaseHandler
from core.function_context import FunctionContext

Limit = namedtuple('Limit', 'min max')
Variable = namedtuple('Variable', 'type value')
regex_declaration = r"^\s*[extern\s]+?[unsigned|signed\s]*[const\s+]?(int|short|char|long|byte)[\s*]([\w:<>]*)\s?=\s?(\d*).*;"
regex_arithmetic = r"^\s*([\w:<>]*)\s*=\s*([\w:<>]*|\d*)\s*(\+|\-|\*|\/)?\s*([\w:<>]*|\d*).*;"
# LP64 standard
limits = {'int': Limit(-2 ** 31, 2 ** 31 - 1),
          'byte': Limit(-2 ** 15, 2 ** 15 - 1),
          'short': Limit(-2 ** 15, 2 ** 15 - 1),
          'char': Limit(-2 ** 7, 2 ** 7 - 1),
          'long': Limit(-2 ** 63, 2 ** 63 - 1)}


class IntegerOverflowHandler(BaseHandler):
    def __init__(self):
        self.vulnerability_name = 'Integer overflow'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        variables = {}
        for context in contexts:
            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                matches = re.finditer(regex_declaration, processed_line, re.IGNORECASE)
                for matchNum, match in enumerate(matches):
                    variables[match.group(2)] = Variable(match.group(1), int(match.group(3)))
                arithmetic_matches = re.finditer(regex_arithmetic, processed_line, re.IGNORECASE)
                for matchNum, match in enumerate(arithmetic_matches):
                    if match.group(2).isdigit() or match.group(2) in variables.keys():
                        if match.group(3) is None:
                            if match.group(1) not in variables.keys():
                                variables[match.group(1)] = Variable('int', 0)
                            variables[match.group(1)] = variables[match.group(1)]._replace(
                                value=int(match.group(2)) if match.group(2).isdigit() else variables[
                                    match.group(2)].value)
                        else:
                            left = int(match.group(2)) if match.group(2).isdigit() else variables[match.group(2)].value
                            right = int(match.group(4)) if match.group(4).isdigit() else variables[match.group(4)].value
                            if match.group(3) == '*':
                                tmp = left * right
                            elif match.group(3) == '+':
                                tmp = left + right
                            elif match.group(3) == '-':
                                tmp = left - right
                            else:
                                tmp = left // right
                            variables[match.group(1)] = variables[match.group(1)]._replace(value=tmp)
                        try:
                            assert (limits[variables[match.group(1)].type].min <= variables[match.group(1)].value <=
                                    limits[
                                        variables[match.group(1)].type].max)
                        except AssertionError:
                            error_details = '{} of type {}'.format(match.group(1), variables[match.group(1)].type)
                            self.output.append(f"WARNING in function {context.name}! "
                                               f"Integer overflow ({cur_line_number}) for {error_details}")
        return self.output
