import re
from typing import List
from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class IncorrectFileAccessHandler(BaseHandler):
    vulnerability_name = 'Некорректный доступ к файлам'

    """
    - ofstream.open(const char *fname); - открывает поток вывода в файл <fname>.
    
    - ifstream.open(const char *fname); - открывает поток ввода в файл <fname>.  
    
    - int mkdir(const char *path); - создает директорию по указанному пути.
    
    - int rmdir(const char *path); - удаляет директорию по указанному пути.
    
    - char *mktemp(char *fname); - создает уникальное имя файла и сам файл.
    
    - int utime(char *fname, struct utimbuf *t); - изменяет время последней модификации файла <fname>.
    """

    def __init__(self):

        self.pattern = r'(^mkdir|^mktemp|^rmdir|^utime|^chmod)'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        total_errors = 0
        for context in contexts:
            streams = list(filter(lambda v: 1 if v.var_type == "ofstream" or v.var_type == "ifstream" else 0,
                                  context.variables))
            streams = [v.var_name for v in streams]
            for line_number, line in context.source_code.items():
                matches = re.finditer(r"(ifstream|ofstream)\s*([\w]*[\w\d_]*)\.open\(.*\)", line)
                for match in matches:
                    total_errors += 1
                    self.output.append(f"{total_errors}) Предупреждение в методе <{context.name}>!\n"
                                       f"Использование функции открытия потока ввода/вывода <{match.group(1)}> "
                                       f"(строка {line_number}). Проверьте доступность открываемого файла")
                if len(streams) > 0:
                    matches_1 = re.finditer(r"(" + "|".join(streams) + r")\.open", line)
                    for _ in matches_1:
                        total_errors += 1
                        self.output.append(f"{total_errors}) Предупреждение в методе <{context.name}>!\n"
                                           f"Использование функции открытия потока ввода/вывода <open> "
                                           f"(строка {line_number}). Проверьте доступность открываемого файла")
                matches_2 = re.finditer(self.pattern, line)
                for match in matches_2:
                    total_errors += 1
                    self.output.append(f"{total_errors}) Предупреждение в методе <{context.name}>!\n"
                                       f"Использование функции <{match.group(0)}>, которая осуществляет доступ к файлам"
                                       f" (line {line_number}). Отсутствие проверки существования файла может "
                                       f"привести к ошибке")
        self.output.append(self.vulnerability_name + ": " + str(total_errors))
        return self.output
