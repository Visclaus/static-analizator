import re

from core import base_parser
from core.base_parser import BaseParser


class IncorrectFileAccess(BaseParser):
    def __init__(self, analyzer_context):
        super().__init__(analyzer_context)
        self.output = []
        self.vulnerability_name = 'Incorrect File Access'
        self.pattern = [
            r'(CreateFile|OpenFile|access|chown|chgrp|chmod|link|unlink|mkdir|mknod|mktemp|rmdir|symlink|tempnam|tmpfile|unmount|utime)']

    def parse(self, cpp_code):
        line_counter = 0
        for line in cpp_code:
            line_counter += 1

            # unsafety functions
            matches = re.finditer(self.pattern[0], line, re.IGNORECASE)
            for matchNum, match in enumerate(matches):
                matchNum = matchNum + 1
                self.output.append(base_parser.warning(line_counter, str(line).strip(), self.vulnerability_name, 'WARNING',
                                                       'Usage of files related I/O functions. Possible Incorrect file access'))

        return self.output
