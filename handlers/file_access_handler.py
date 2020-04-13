import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class IncorrectFileAccessHandler(BaseHandler):
    def __init__(self):
        self.vulnerability_name = 'Incorrect File Access'
        self.pattern = r'(CreateFile|OpenFile|access|chown|chgrp|chmod|link|unlink|mkdir|mknod|mktemp|rmdir|symlink|tempnam|tmpfile|unmount|utime)'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            for line in context.source_code:
                for key in line:
                    matches = re.finditer(self.pattern, key, re.IGNORECASE)
                    for _ in matches:
                        self.output.append(f"WARNING in function {context.name}! "
                                           f"Usage of files related I/O functions (line {line[key]}). Possible Incorrect file access")
        return self.output
