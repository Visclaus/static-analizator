import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class DataLeakHandler(BaseHandler):
    def __init__(self):
        self.vulnerability_name = 'Data Leak'
        self.pattern = r'(GetLastError|SHGetFolderPath|SHGetFolderPathAndSubDir|SHGetSpecialFolderPath|GetEnvironmentStrings|GetEnvironmentVariable|\*printf|errno|getenv|strerror|perror)'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            for line in context.source_code:
                for key in line:
                    matches = re.finditer(self.pattern, key, re.IGNORECASE)
                    for _ in matches:
                        self.output.append(f"WARNING in function {context.name}! "
                                           f"Receiving data (line {line[key]}) that can affect application security. Possible Data leak")
        return self.output
