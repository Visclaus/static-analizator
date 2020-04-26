import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class SQLInjectionHandler(BaseHandler):
    vulnerability_name = 'SQL инъекции'

    def __init__(self):
        self.pattern = r'(executeQuery|execute)(\(.*\))'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                matches = re.finditer(self.pattern, processed_line)
                for match in matches:
                    tmp = match.group(2)[1:-1]
                    if tmp[0] == '\"':  # check if parameter is literally string like "test string"
                        if re.search(r'[^\\]\'', tmp) is not None:
                            self.output.append(f"Угроза в методе <{context.name}>!\n"
                                               f"Тело sql запроса <{tmp[1:-1]}>, используемое в функции <{match.group(1)}> (строка {cur_line_number}) "
                                               f"имеет неэкранированный символ(ы) <'>\nЭто может привести к sql инъекции")
                    else:
                        self.output.append(f"Предупреждение в методе <{context.name}>!\n"
                                           f"Проверьте тело sql запроса <{tmp}>, используемое в функции <{match.group(1)}> (строка {cur_line_number}) "
                                           f"на наличие неэкранированного символа <'>'\nЭто может привести к sql инъекции")
        return self.output
