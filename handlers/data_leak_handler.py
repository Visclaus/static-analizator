import re
from typing import List
from core.base_handler import BaseHandler
from core.function_context import FunctionContext


# TODO: можно добавить поиск вывода исключений в конструкциях try-catch
class DataLeakHandler(BaseHandler):
    vulnerability_name = 'Утечка информации'

    """
    - DWORD GetLastError(); - возваращет код последней ошибки, вызывающего потока.
    
    - HRESULT SHGetFolderPath(HWND hwndOwner, int nFolder, HANDLE hToken, DWORD dwFlags, LPTSTR pszPath); - возвращает 
      путь к определённой системной директории, тип которой указан в идентификаторе CSIDL.
      
    - LPVOID GetEnvironmentStrings(); - возвраащет переменные окружения для текущего процесса.
    
    - string GetEnvironmentVariable (string variable); - возвращает из текущего процесса значение переменной среды.
    
    - errno - макрос, который возвращает последний номер ошибки.
    
    - char *getenv(const char *name); - возвращает указатель на информацию об окружении, ассоциированную с <name> 
      в таблице информации окружения. Окружение программы может включать такие вещи, как имена путей и устройств.
      
    - char *strerror(int num); - возвращает указатель на сообщение об ошибке, связанное с номером ошибки <num>.
    
    - void perror(const char *str); - помещает значение глобальной переменной errno в строку и записывает эту строку в
      поток stderr.
    """

    def __init__(self):
        self.pattern = r'(GetLastError|SHGetFolderPath|GetEnvironmentStrings|GetEnvironmentVariable|errno|getenv|' \
                       r'strerror|perror)'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                matches = re.finditer(self.pattern, processed_line)
                for match in matches:
                    if match.group(0) == "errno":
                        self.output.append(f"Предупреждение в методе <{context.name}>!\n"
                                           f"Использование макроса <{match.group(0)}>, который может привести к утечке "
                                           f"системных данных или к расскрытию важной информации (строка {cur_line_number})\n")
                    else:
                        self.output.append(f"Предупреждение в методе <{context.name}>!\n"
                                           f"Использование функции <{match.group(0)}>, которая может привести к утечке "
                                           f"системных данных или к расскрытию важной информации (строка {cur_line_number})\n")

        return self.output
