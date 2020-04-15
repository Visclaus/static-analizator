import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class DataStorageManagementHandler(BaseHandler):
    def __init__(self):
        self.vulnerability_name = 'Bad Data Storage Management'
        self.pattern = r'(SetFileSecurity|SetKernelObjectSecurity|SetSecurityDescriptorDacl|SetServiceObjectSecurity|' \
                       r'SetUserObjectSecurity|SECURITY_DESCRIPTOR|ConvertStringSecurityDescriptorToSecurityDescriptor|chmod|fchmod|chown|fchown|fcntl|setgroups|acl_\*)'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                matches = re.finditer(self.pattern, processed_line, re.IGNORECASE)
                for _ in matches:
                    self.output.append(f"WARNING in function {context.name}! "
                                       f"Usage of security related functions (line {cur_line_number}). Possible bad data storage management")

        return self.output
