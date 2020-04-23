from typing import List
from core import main_code_parser
from core.base_handler import BaseHandler
from core.variable import *
from core.function_context import FunctionContext


class BufferOverflowHandler(BaseHandler):

    vulnerability_name = 'Переполнение буфера'

    """
    - char * strcpy ( char * destination, const char * source ); - Копирует строку <source> в буфер <destination>.
    
    - int printf ( const char * format, ... ); - Выводит строку указанную в формате в стандартный поток вывода.
    
    - char * strcat ( char * destination, const char * source ); - Добавляет к строке <destination> копию <source>
    
    - void * memcpy ( void * destination, const void * source, size_t num ); - копирует <num> байт из <source> в 
      <destination>
      
    - char * gets ( char * str ); - читает символы из потока ввода и записывает их в <str>
    
    - int sprintf ( char * str, const char * format, ... ); - аналогично <printf>, но вывод происходит в буфер <str>
    
    - int vsprintf (char * s, const char * format, va_list arg ); - аналогично <sprintf>, но принимает только один <arg>
    
    - char * strncpy ( char * destination, const char * source, size_t num ); - <strcpy>, но копирует только  <num> байт
    """

    def __init__(self):
        self.pattern = r"(strcpy|printf|strcat|memcpy|gets|sprintf|vsprintf|strncpy|scanf)" \
                       r"\(.*\)"
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            declared_variables = context.variables
            for line in context.source_code:
                cur_line_number = list(line.values())[0]
                processed_line = list(line.keys())[0]
                matches = re.finditer(self.pattern, processed_line)
                for match in matches:
                    used_variables = main_code_parser.get_parameters(match.group(0), declared_variables)
                    for used_variable in used_variables:
                        declaration = used_variable.full_declaration
                        if is_pointer(declaration) or is_array(declaration):
                            self.output.append(
                                f"Предупреждение в методе <{context.name}>!\n"
                                f"Использование буфера <{declaration[:-1]}> (строка {used_variable.line_appeared}) "
                                f"в небезопасной функции <{match.group(1)}> (строка {cur_line_number}).\n"
                                f"Это может стать причиной переполнения буфера. "
                                f"Убедитесь в наличии проверки этой угрозы!\n")

        return self.output
