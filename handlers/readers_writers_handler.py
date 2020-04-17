from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class ReadersWritersHandler(BaseHandler):
    def __init__(self):
        self.vulnerability_name = 'Readers Writers'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        warning = ""
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
                    for key in var_usage:
                        if len(var_usage[key]) > 1:
                            thread
                            warning = f"WARNING in function {context.name}\n"
                            warning += "Threads:\n"
                            for thread in var_usage[key]:
                                warning += f"\"{thread.thread_name} line ({thread.line_appeared})\"\n"
                            warning += f"are using the same variable \"{key}\" as runnable parameter, it may cause readers writers problem!\n"
                self.output.append(warning)
        return self.output
