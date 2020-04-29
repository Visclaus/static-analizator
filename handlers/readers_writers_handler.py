from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class ReadersWritersHandler(BaseHandler):
    vulnerability_name = 'Читатели - Писатели'

    def __init__(self):
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        for context in contexts:
            if len(context.threads) != 0:
                declared_threads = context.threads
                # part for detecting same variables
                vars_to_threads = []  # list of dicts - List[{var_name: List[Threads]}]
                var_in_threads = []  # list of variables - List[Variable]
                # creating list of all used params
                for thread in declared_threads:
                    for parameter in thread.parameter_list:
                        if parameter not in var_in_threads:
                            var_in_threads.append(parameter)
                # filling list of params - threads
                for index, var in enumerate(var_in_threads):
                    t_list = []
                    dict_tmp = {var.var_name: t_list}
                    vars_to_threads.append(dict_tmp)
                    for thread in declared_threads:
                        for parameter in thread.parameter_list:
                            if var == parameter:
                                vars_to_threads[index][var.var_name].append(thread)
                # checking where same parameters has usage in several threads
                thread_with_same_vars =[]
                for var_usage in vars_to_threads:
                    warning = ""
                    for key in var_usage:
                        if len(var_usage[key]) > 1:
                            warning = f"Предупреждение в методе <{context.name}>!\n"
                            warning += "Потоки:\n"
                            for thread in var_usage[key]:
                                warning += f"\"<{thread.thread_name}> (строка {thread.line_appeared})\"\n"
                            warning += f"используют одну и ту же переменную <{key}> " \
                                       f"в качестве параметра для исполняемой функции, " \
                                       f"это может привести к проблеме Читатели - Писатели!\n"
                    self.output.append(warning)
        return self.output
