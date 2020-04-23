import re
from typing import List
from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class DataStorageManagementHandler(BaseHandler):

    vulnerability_name = 'Пренебрежение безопасным хранением данных'

    """
    - BOOL SetFileSecurity(LPCTSTR lpFileName, SECURITY_INFORMATION SecurityInformation, 
      PSECURITY_DESCRIPTOR pSecurityDescriptor); - устанавливает защиту объекта файла или каталога.
      
    - BOOL SetKernelObjectSecurity(HANDLE Handle, SECURITY_INFORMATION SecurityInformation,
      PSECURITY_DESCRIPTOR SecurityDescriptor); - устанавливает защиту объекта ядра.
      
    - BOOL SetServiceObjectSecurity(SC_HANDLE hService, SECURITY_INFORMATION dwSecurityInformation, 
      PSECURITY_DESCRIPTOR lpSecurityDescriptor); - устанавливает дескриптор безопасности объекта службы.
    
    - int chmod(char *pathname,int pmode); - изменяет разрешенный доступ для файла <pathname>.
    
    - int fchmod(int fildes, mode_t mode); - изменяет разрешенный доступ.
    
    - int fchown(int fd, uid_t owner, gid_t group); - изменяет владельца файла.
    
    - int fcntl(int fd, int cmd, ... /* arg */ ); - манипуляции над файловым дескриптором.
    
    - int setgroups(int size, gid_t list[]); - устанавливает список дополнительных идентификаторов групп. 
    """

    def __init__(self):
        self.pattern = r'(SetFileSecurity|SetKernelObjectSecurity|SetServiceObjectSecurity|chmod|fchmod|fchown|' \
                       r'fcntl|setgroups)'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                matches = re.finditer(self.pattern, processed_line)
                for match in matches:
                    self.output.append(f"Предупреждение в методе <{context.name}>!\n"
                                       f"Использование функции, регулирующей настройки безопасности системы или файлов "
                                       f"<{match.group(0)}>, которая может привести к проблеме "
                                       f"ненадежного хранения данных (строка {cur_line_number})\n")
        return self.output
