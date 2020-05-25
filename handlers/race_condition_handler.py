from typing import List
from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class RaceConditionHandler(BaseHandler):
    vulnerability_name = 'Состояние гонки'

    def __init__(self):
        self.output = []

    def parse(self, contexts: List[FunctionContext]):
        total_errors = 0
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
                        total_errors += 1
                        warning = f"{total_errors}) Предупреждение в методе <{context.name}>!\n"
                        warning += "Потоки:\n"
                        cur_func = func_usage[0].runnable_function
                        for thread in func_usage:
                            warning += f"\"<{thread.thread_name}> (строка {thread.line_appeared})\"\n"
                        warning += f"используют одну и туже исполняемую функцию <{cur_func}>, " \
                                   f"это может вызвать состояние гонки!\n"
                        self.output.append(warning)
        self.output.append(self.vulnerability_name + ": " + str(total_errors))
        return self.output
