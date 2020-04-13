import re

from core import base_parser
from core.base_parser import BaseParser


class DataStorageManagementParser(BaseParser):
    def __init__(self):
        self.output = []
        self.vuln_name = 'Bad Data Storage Management'
        self.pattern = [r'(SetFileSecurity|SetKernelObjectSecurity|SetSecurityDescriptorDacl|SetServiceObjectSecurity|SetUserObjectSecurity|SECURITY_DESCRIPTOR|ConvertStringSecurityDescriptorToSecurityDescriptor|chmod|fchmod|chown|fchown|fcntl|setgroups|acl_\*)']

    def parse(self, cpp_code):
        line_counter = 0
        for line in cpp_code:
            line_counter += 1

            # unsafety functions
            matches = re.finditer(self.pattern[0], line, re.IGNORECASE)
            for matchNum, match in enumerate(matches):
                matchNum = matchNum + 1
                self.output.append(base_parser.warning(line_counter, str(line).strip(), self.vuln_name, 'WARNING', 'Usage of security related functions. Possible bad data storage management'))

        return self.output
