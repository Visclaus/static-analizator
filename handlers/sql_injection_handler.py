import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class SQLInjectionHandler(BaseHandler):
    def __init__(self):
        self.vulnerability_name = 'SQL Injection'
        self.pattern = r'(executeQuery|execute)(\(.*\))'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                matches = re.finditer(self.pattern, processed_line)
                for match in matches:
                    tmp = match.group(2)[1:-1]
                    if tmp[0] == '\"':  # check if parameter is literally string like "test string"
                        if re.search(r'[^\\]\'', tmp) is not None:
                            self.output.append(f"WARNING in function {context.name}! "
                                               f"The body of your sql query ({tmp[1:-1]}), which is used in method \"{match.group(1)}\" (line{cur_line_number}) "
                                               f"has unescaped character(s) - '\nIt's may cause sql injection vulnerability")
                    else:
                        self.output.append(f"WARNING in function {context.name}! "
                                           f"Check the body of your sql query ({tmp}), which is used in method \"{match.group(1)}\" (line{cur_line_number}) "
                                           f"for having unescaped character(s) - '\nIt's may cause sql injection vulnerability")
        return self.output
