import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class CommandsIntroductionHandler(BaseHandler):

    vulnerability_name = 'Внедрение команд'

    """
    - int system (const char* command); - выполняет системную команду.
    
    - FILE *popen(const char *command, const char *type); - создает дочерний процесс, которому можно передать команду.
    
    - int execlp(const char *file, const char *arg, ...); - выполнение исполняемого файла по пути <file> с передачей 
      параметра в <arg>.
      
    - int execvp(const char *file, char *const argv[]); - тоже что и execlp, но параметры передаются в <argv>.
    
    - HINSTANCE ShellExecute(HWND hwnd, LPCSTR lpOperation, LPCSTR lpFile, LPCSTR lpParameters, LPCSTR lpDirectory, INT nShowCmd); - 
      выполняет команду <lpOperation> над указанным файлом <lpFile>.
    """

    def __init__(self):
        self.pattern = r'(system|popen|execlp|execvp|ShellExecute)'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                matches = re.finditer(self.pattern, processed_line, re.IGNORECASE)
                for match in matches:
                    self.output.append(f"Предупреждение в методе <{context.name}>!\n"
                                       f"Использование функции <{match.group(1)}>, в которую может быть внедрена"
                                       f" вредоносная команда (строка {cur_line_number}) "
                                       f"Убедитесь в наличии проверки этой угрозы!\n")

        return self.output
