import re
from typing import List

from core.base_handler import BaseHandler
from core.function_context import FunctionContext


class ReadersWritersHandler(BaseHandler):
    vulnerability_name = 'Читатели Писатели'

    def __init__(self):
        self.output = []
        self.total_errors = 0

    def check_mutex(self, context: FunctionContext, thread):
        mutex_cnt = len(FunctionContext.global_mutexes)
        mutex_locked = [0 for _ in range(mutex_cnt)]
        mutex_unlocked = [0 for _ in range(mutex_cnt)]
        context_beginning = None
        for line_number, line in context.source_code.items():
            context_beginning = line_number + 1
            break
        for line_number, line in context.source_code.items():
            for index, mutex in enumerate(FunctionContext.global_mutexes):
                if re.match(r'' + mutex + r'\.lock\s*\(.*\);', line):
                    mutex_locked[index] += 1
                    continue
            for index, mutex in enumerate(FunctionContext.global_mutexes):
                if re.match(r'' + mutex + r'\.unlock\s*\(.*\);', line):
                    mutex_unlocked[index] += 1
        for index in range(mutex_cnt):
            if mutex_locked[index] == mutex_unlocked[index]:
                continue
            elif mutex_locked[index] > mutex_unlocked[index]:
                self.total_errors += 1
                return f"{self.total_errors - 1}) Отсутствует освобождение блока синхронизации " \
                       f"(семафор - {FunctionContext.global_mutexes[index]}) в исполняемой функции <{context.name}> " \
                       f"(строка {context_beginning}) потока <{thread.thread_name}>"
            elif mutex_locked[index] < mutex_unlocked[index]:
                self.total_errors += 1
                return f"{self.total_errors - 1}) Отсутстввует захват блока синхронизации " \
                       f"(семафор - {FunctionContext.global_mutexes[index]}) в исполняемой функции <{context.name}> " \
                       f"(строка {context_beginning}) потока <{thread.thread_name}>"
        is_no_mutex = True
        for index, _ in enumerate(mutex_locked):
            if mutex_locked[index] != 0 and mutex_unlocked[index] != 0:
                is_no_mutex = False
        if is_no_mutex:
            self.total_errors += 1
            return f"{self.total_errors}) Отсутстввует блок синхронизации " \
                   f"в исполняемой функции <{context.name}> (строка {context_beginning}) потока <{thread.thread_name}>"

        return ""

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
                thread_with_same_vars = []
                for var_usage in vars_to_threads:
                    warning = ""
                    for key in var_usage:
                        if len(var_usage[key]) > 1:
                            self.total_errors += 1
                            warning = "---Анализ параметров потоков---\n"
                            warning += f"{self.total_errors}) Предупреждение в методе <{context.name}>!\n"
                            warning += "Потоки:\n"
                            for thread in var_usage[key]:
                                warning += f"\"<{thread.thread_name}> (строка {thread.line_appeared})\"\n"
                            warning += f"используют одну и ту же переменную <{key}> " \
                                       f"в качестве параметра для исполняемой функции, " \
                                       f"это может привести к проблеме Читатели - Писатели!\n"
                    self.output.append(warning)
                    self.output.append("---Анализ объектов синхронизации в исполняемых функциях потоков, "
                                       "использующих одни и теже переменные---\n")
                    thread_list = list(var_usage.items())[0][1]
                    for thread in thread_list:
                        for c in contexts:
                            if c.name == thread.runnable_function:
                                self.output.append(self.check_mutex(c, thread))
                                self.output.append("\n")
        self.output.append(self.vulnerability_name + ": " + str(self.total_errors))
        self.total_errors = 0
        return self.output
