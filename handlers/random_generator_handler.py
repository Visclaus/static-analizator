import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class RandomGeneratorHandler(BaseHandler):
    vulnerability_name = 'Случайные числа крипто-го качества'

    """
    void srand(unsigned seed); - используется для установки начала последовательности, генерируемой функ­цией rand().
    
    int rand (void); - вовращает псевдо-случайное челочисленное число в интервале от 0 до RAND_MAX.
    
    uniform_real_distribution - класс используемый для генерации равномернораспределенного нецелочисленного числа
     равномерно распределенного на интервале [a, b)
    """

    def __init__(self):
        self.pattern = [r'srand\((.*?)\)', r'rand\(\)|uniform_real_distribution']
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        """
        1)Находит использование функции генерации srand(), в случаях когда она инициализирована const числовым значением
        2)Находит использование небезопасных функций генерации rand() и uniform_real_distribution
        """
        for context in contexts:
            for line_number, line in context.source_code.items():
                srand_matches = re.finditer(self.pattern[0], line, re.IGNORECASE)
                for match in srand_matches:
                    if match.group(1).isdigit():
                        self.output.append(f"Угроза в методе <{context.name}>!\n"
                                           f"Использование функции <srand>, которая инициализирована константным значением - "
                                           f"{match.group(1)} (строка {line_number})")
                rand_matches = re.finditer(self.pattern[1], line, re.IGNORECASE)
                for match in rand_matches:
                    self.output.append(f"Предупреждение в методе {context.name}!\n"
                                       f"Использования не крипто-безопасной функции генерации <{match.group(0)}> (строка {line_number})")
        return self.output
