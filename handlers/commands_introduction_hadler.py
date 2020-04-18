import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class CommandsIntroductionHandler(BaseHandler):

    vulnerability_name = 'Introduction of Commands'

    def __init__(self):
        self.pattern = r'(system|popen|execlp|execvp|ShellExecute)'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        """
        Ищет использование системных функций
        """
        for context in contexts:
            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                matches = re.finditer(self.pattern, processed_line, re.IGNORECASE)
                for match in matches:
                    self.output.append(f"WARNING in function {context.name}! "
                                       f"Usage of non safe function \"{match.group(1)}\" (line {cur_line_number}), which may cause execution of commands commands")

        return self.output
