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
                for key in line:
                    matches = re.finditer(self.pattern, key, re.IGNORECASE)
                    for _ in matches:
                        self.output.append(f"WARNING in function {context.name}! "
                                           f"Usage of security related functions (line {line[key]}). Possible bad data storage management")
        return self.output
