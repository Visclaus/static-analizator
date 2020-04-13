import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class CommandsIntroductionHandler(BaseHandler):
    def __init__(self):
        self.vulnerability_name = 'Introduction of Commands'
        self.pattern = r'(system|popen|execlp|execvp|ShellExecute)'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            for line in context.source_code:
                for key in line:
                    matches = re.finditer(self.pattern, key, re.IGNORECASE)
                    for match in matches:
                        self.output.append(f"WARNING in function {context.name}! "
                                           f"Usage of non safe function \"{match.group(1)}\" (line {line[key]}), which may cause execution of commands commands")

        return self.output
