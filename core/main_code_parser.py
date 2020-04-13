import re
from typing import List

from core.function_variable import FunctionVariable
from core.thread import Thread
from core.variable import Variable
from core.function_context import FunctionContext

variable_regexp = r"^\s*(extern\s+)?(unsigned\s+|signed\s+)?(const\s+)?(int|short|char|long|double|float|byte|string)\s+" \
                  r"(\*)?([a-zA-Z0-9_:<>]*)\s*(\[.+])?\s*(=.+)?(\s*;)"

thread_regexp = r'^\s*std::thread\s+([a-zA-Z0-9_:<>]*)\(([a-zA-Z0-9_:<>]*)(,\s?[a-zA-Z0-9_:<>]*|,\s?"[a-zA-Z0-9_:<>]*"*)*\)'


def find_contexts(source_code):
    initial_contexts = get_initial_contexts(source_code)
    for context in initial_contexts:
        context.variables = get_declared_variables(context.source_code)
        context.threads = get_declared_threads(context.source_code, context.variables)
    return initial_contexts


def get_initial_contexts(source_code):
    # пока что распознает только простые типы параметров и возвращаемых значений без указателей массивов и т.д.
    start_context_pattern = r'(int|short|char|long|double|float|byte|void)\s+([a-zA-Z0-9_]+)\s*(\(.*\))'
    end_context_pattern = r'}'
    found_contexts = []
    cur_context = None
    cur_context_open_bracers = 0
    cur_context_close_bracers = 0
    for cur_line_number, line in enumerate(source_code):
        cur_line_number += 1
        match = re.match(start_context_pattern, line)
        open_bracer_matches = re.finditer(r'\{', line)
        close_bracer_matches = re.finditer(r'\}', line)
        for _ in open_bracer_matches:
            cur_context_open_bracers += 1

        for _ in close_bracer_matches:
            cur_context_close_bracers += 1

        if match is not None:
            cur_context = FunctionContext()
            cur_context.return_type = match.group(1)
            cur_context.name = match.group(2)
            cur_context.parameters = get_context_parameters(line)
            cur_context.source_code.append({line: cur_line_number})
        elif cur_context is not None:
            if re.match(end_context_pattern, line) is None:
                cur_context.source_code.append({line: cur_line_number})
            elif cur_context_open_bracers == cur_context_close_bracers:
                cur_context.source_code.append({line: cur_line_number})
                found_contexts.append(cur_context)
                cur_context = None
                cur_context_open_bracers = 0
                cur_context_close_bracers = 0
                continue
    return found_contexts


def get_declared_variables(source_code):
    variables = []
    for line in source_code:
        for key in line:
            matches = re.finditer(variable_regexp, key, re.MULTILINE)
            for match in matches:
                var = Variable(match.group(0), line[key], match.group(6), match.group(4))
                if match.group(8) is not None:
                    tmp = match.group(8)[1:]
                    var.value = tmp.replace(' ', '')
                variables.append(var)
    return variables


def get_declared_threads(source_code, declared_variables):
    """
    Function to get a list of all declared threads
    :param source_code: analyzed source code
    :return: list of Threads
    :rtype: List[Thread]
    """
    threads = []  # List of threads in code
    for line in source_code:
        for key in line:
            matches = re.finditer(thread_regexp, key)
            for match in matches:
                cur_thread_params = get_parameters(match.group(0), declared_variables)
                threads.append(
                    Thread(match.group(0), line[key], match.group(1), match.group(2), cur_thread_params))
    return threads


def get_parameters(raw_parameters, declared_variables) -> List[Variable]:
    """
    Function to get a list of parameters from function or thread declaration
    This parameters are linked with some declared variable
    :param raw_parameters: source code with parameters to parse: "(param1, param2, param3, ...)"
    :return: list of Variables
    :rtype: List[Variable]
    """
    tmp = re.search(r"\(.*\)", raw_parameters).group(0)[1:-1]
    parameters_list = re.split(r",*\s", tmp)
    v_parameters_list = []
    declared_variables = declared_variables
    for index, parameter in enumerate(parameters_list):
        for var in declared_variables:
            if parameter == var.var_name:
                v_parameters_list.append(var)
                break
    return v_parameters_list


def get_context_parameters(raw_parameters):
    tmp = re.search(r"\(.*\)", raw_parameters).group(0)[1:-1]
    v_parameters_list = []
    if tmp != '':
        parameters_list = re.split(r",\s*", tmp)
        for parameter in parameters_list:
            # пока что распознает только простые типы параметров без указателей массивов и т.д.
            match = re.match(r'(int|short|char|long|double|float|byte|string)\s+\**([a-zA-Z0-9_]+)', parameter)
            v_parameters_list.append(FunctionVariable(match.group(1), match.group(2)))
    return v_parameters_list


class AnalyzedCode:
    def __init__(self, source_code):
        self.contexts = find_contexts(source_code)
