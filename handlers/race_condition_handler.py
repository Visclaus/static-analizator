from core.base_parser import BaseParser
from core.parse_utils import *


class RaceConditionHandler(BaseParser):
    def __init__(self, analyzer_context):
        super().__init__(analyzer_context)
        self.vulnerability_name = 'Race Condition'
        self.output = []

    def parse(self, source_code):
        declared_threads = self.analyzer_context.declared_threads

        # part for detecting same runnables
        funcs_to_threads = [[], []]
        func_in_threads = []
        # creating list of all runnables
        for thread in declared_threads:
            if thread.runnable_function not in func_in_threads:
                func_in_threads.append(thread.runnable_function)
        # filling list of func - threads
        for index, func in enumerate(func_in_threads):
            for thread in declared_threads:
                if func == thread.runnable_function:
                    funcs_to_threads[index].append(thread)

        # checking where function is used more than one time as runnable
        for func_usage in funcs_to_threads:
            if len(func_usage) > 1:
                print("Threads:\n")
                cur_func = func_usage[0].runnable_function
                for thread in func_usage:
                    print(f"\"{thread.thread_name} line ({thread.line_appeared})\"\n")
                print(f"are using the same runnable function \"{cur_func}\", it may cause race condition!")

        # part for detecting same variables
        vars_to_threads = []  # list of dicts - List[{var_name: List[Threads]}]
        var_in_threads = []   # list of variables - List[Variable]
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
        for var_usage in vars_to_threads:
            for key in var_usage:
                if len(var_usage[key]) > 1:
                    print("Threads:\n")
                    for thread in var_usage[key]:
                        print(f"\"{thread.thread_name} line ({thread.line_appeared})\"\n")
                    print(f"are using the same variable \"{key}\" as runnable parameter, it may cause race condition!\n")
