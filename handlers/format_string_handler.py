import re

from core import base_parser
from core.base_parser import BaseParser


class FormatStringHandler(BaseParser):
    def __init__(self, analyzer_context):
        super().__init__(analyzer_context)
        self.output = []
        self.vulne_name = 'Format String'
        self.pattern = [
            r'(printf[(][a-zA-Z0-9_]*)([)])']  # TODO: improve to parse cases with whitespaces, maybe find another regex for this vuln

    def parse(self, source_code):
        cur_line_number = 0
        for line in source_code:
            cur_line_number += 1
            matches = re.finditer(self.pattern[0], line, re.IGNORECASE)
            for match in matches:
                self.output.append(base_parser.warning(cur_line_number, str(line), self.vulnerability_name, 'CRITICAL',
                                                       'Possible format string vulnerable'))

        return self.output


if __name__ == "__main__":
    with open("tests/format_test.cpp") as file:
        parser = FormatStringHandler()
        out = parser.parse(file)
        for state in out:
            print(state)