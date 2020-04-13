import re

from core import base_parser
from core.base_parser import BaseParser


class CommandsIntroductionHandler(BaseParser):
    def __init__(self, analyzer_context):
        super().__init__(analyzer_context)
        self.output = []
        self.vulnerability_name = 'Introduction of Commands'
        self.pattern = r'(system|popen|execlp|execvp|ShellExecute)'

    def parse(self, source_code):
        cur_line_number = 0
        for line in source_code:
            cur_line_number += 1
            matches = re.finditer(self.pattern, line, re.IGNORECASE)
            for match in matches:
                self.output.append(base_parser.warning(cur_line_number, str(line), self.vulnerability_name, 'WARNING',
                                                       f'Usage of not safe  function "{match.group(1)}", which may cause execution of commands commands'))

        return self.output
