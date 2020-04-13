from typing import List

from core.variable import Variable


class Thread:
    def __init__(self, full_declaration, line_appeared, thread_name, runnable_function, parameter_list: List[Variable]):
        self.full_declaration = full_declaration
        self.line_appeared = line_appeared
        self.thread_name = thread_name
        self.runnable_function = runnable_function
        self.parameter_list = parameter_list
