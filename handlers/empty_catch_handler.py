import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class EmptyCatchHandler(BaseHandler):
    def __init__(self):
        self.vulnerability_name = 'Empty Catch Block'
        self.pattern = r'.*catch\s*\(.*\)\s*\{'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            is_catch_found = False
            cur_catch_body = []
            is_cur_empty = False
            v_line_found = 0
            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                if is_cur_empty:
                    is_cur_empty = False
                    is_catch_found = False
                    cur_catch_body = []
                    self.output.append(f"WARNING in function {context.name}! (line {v_line_found}) "
                                       f"No handling of exception! Ignoring an exception can cause the program to "
                                       f"overlook unexpected states and conditions\n")

                if is_catch_found:
                    if re.match(r'\}', processed_line) is not None:
                        for catch_line in cur_catch_body:
                            if catch_line.replace(" ", "") == "":
                                is_cur_empty = True
                            else:
                                is_cur_empty = False
                                break
                    else:
                        cur_catch_body.append(processed_line)
                if re.match(self.pattern, processed_line, re.IGNORECASE) is not None:
                    v_line_found = cur_line_number
                    is_catch_found = True
        return self.output
