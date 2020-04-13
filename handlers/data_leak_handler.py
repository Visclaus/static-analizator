import re

from core import base_parser
from core.base_parser import BaseParser


class DataLeak(BaseParser):
    def __init__(self):
        self.output = []
        self.vuln_name = 'Data Leak'
        self.pattern = [r'(GetLastError|SHGetFolderPath|SHGetFolderPathAndSubDir|SHGetSpecialFolderPath|GetEnvironmentStrings|GetEnvironmentVariable|\*printf|errno|getenv|strerror|perror)']

    def parse(self, cpp_code):
        line_counter = 0
        for line in cpp_code:
            line_counter += 1
            # just searching for unsafe functions;
            # unsafety functions
            matches = re.finditer(self.pattern[0], line, re.IGNORECASE)
            for matchNum, match in enumerate(matches):
                matchNum = matchNum + 1
                self.output.append(base_parser.warning(line_counter, str(line).strip(), self.vuln_name, 'WARNING', 'Receiving data that can affect application security. Possible Data leak'))

        return self.output
