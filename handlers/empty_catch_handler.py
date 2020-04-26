import re
from typing import List
from core.base_handler import BaseHandler
from core.function_context import FunctionContext


def is_empty(catch_body: List[str]):
    for line in catch_body:
        tmp = line.replace("", "")
        if tmp == "": continue
        else: return False
    return True


class EmptyCatchHandler(BaseHandler):
    vulnerability_name = 'Пренебрежение обработкой ошибок'

    def __init__(self):
        self.pattern = r'catch\s*' \
                       r'\(.*\)\s*\{'
        self.output = []

    def analyze_catch(self, cur_line_number, global_line_number, context):
        body = []
        close_br = 0
        open_br = 1
        dict_lines = context.source_code
        while cur_line_number < len(dict_lines):
            cur_line = list(dict_lines[cur_line_number].keys())[0]
            if re.match(self.pattern, cur_line) is not None:
                return self.analyze_catch(cur_line_number + 1, global_line_number + 1, context)

            if re.match(r'}', cur_line) is None:
                if re.match(r'.*{', cur_line) is not None:
                    open_br += 1
                body.append(cur_line)

            if re.match(r'}', cur_line):
                close_br += 1
                if open_br != close_br:
                    body.append(cur_line)
                elif is_empty(body):
                    self.output.append(f"Предупреждение в методе <{context.name}>!\n"
                                       f"Отстутсвует обработка исключения или ошибки!  (строка {global_line_number - len(body)})\n")
                    return cur_line_number
                elif not is_empty(body):
                    return cur_line_number
            global_line_number += 1
            cur_line_number += 1

    def parse(self, contexts: List[FunctionContext]):
        index = 0
        prev_index = 0
        for context in contexts:
            prev_index += index
            index = 0
            while index < len(context.source_code):
                processed_line = list(context.source_code[index].keys())[0]
                if re.match(self.pattern, processed_line) is not None:
                    index = self.analyze_catch(index + 1, index + prev_index + 1, context)
                else:
                    index += 1
        return self.output
