from core import base_parser
from core.base_parser import BaseParser
from core.parse_utils import *


class SqlInjectionHandler(BaseParser):
    def __init__(self, analyzer_context):
        super().__init__(analyzer_context)
        self.vulnerability_name = 'Sql Injection'
        self.pattern = r'(executeQuery|execute)(\(.*\))'
        self.output = []

    def parse(self, source_code):
        """
        searches for using 'executeQuery' or 'execute'
        :param source_code:
        :return:
        """
        cur_line_number = 0
        for line in source_code:
            cur_line_number += 1
            matches = re.finditer(self.pattern, line)
            for match in matches:
                tmp = match.group(2)[1:-1]
                if tmp[0] == '\"':  # check if parameter is literally string like "test string"
                    if re.search(r'[^\\]\'', tmp) is not None:
                        self.output.append(
                            base_parser.warning(cur_line_number, str(line), self.vulnerability_name, 'WARNING',
                                                f"The body of your sql query ({tmp[1:-1]}), which is used in method \"{match.group(1)}\" "
                                                f"has unescaped character(s) - '\nIt's may cause sql injection vulnerability"))
                    else:
                        self.output.append(
                            base_parser.warning(cur_line_number, str(line), self.vulnerability_name, 'WARNING',
                                                f"Check the body of your sql query ({tmp}) ({tmp[1:-1]}), which is used in method \"{match.group(1)}\" "
                                                f"for having unescaped character(s) - '\nIt's may cause sql injection vulnerability"))
        return self.output
