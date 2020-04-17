from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class RaceConditionHandler(BaseHandler):
    def __init__(self):
        self.vulnerability_name = 'Race Condition'
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        warning = ""
        for context in contexts:
            if len(context.threads) != 0:
                declared_threads = context.threads
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
                        warning = f"WARNING in function {context.name}\n"
                        warning += "Threads:\n"
                        cur_func = func_usage[0].runnable_function
                        for thread in func_usage:
                            warning += f"\"{thread.thread_name} line ({thread.line_appeared})\"\n"
                        warning += f"are using the same runnable function \"{cur_func}\", it may cause race condition!\n"
                        self.output.append(warning)
        return self.output
