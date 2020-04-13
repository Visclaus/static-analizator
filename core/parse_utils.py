import re
import collections
from typing import List

from core.analyzer_context import AnalyzerContext
from core.thread import Thread
from core.variable import *

variable_regexp = r"^\s*(extern\s+)?(unsigned\s+|signed\s+)?(const\s+)?(int|short|char|long|double|float|byte|string)\s+" \
                  r"(\*)?([a-zA-Z0-9_:<>]*)(\[.+])?.*(;)"

thread_regexp = r'^\s*std::thread\s+([a-zA-Z0-9_:<>]*)\(([a-zA-Z0-9_:<>]*)(,\s?[a-zA-Z0-9_:<>]*|,\s?"[a-zA-Z0-9_:<>]*"*)*\)'  # сделать std optional
thread_params_regexp = r'\(([a-zA-Z0-9_:<>]*)(,\s?[a-zA-Z0-9_:<>]*|,\s?"[a-zA-Z0-9_:<>]*"*)*\)'


def get_declared_variables(source_code) -> List[Variable]:
    cur_line_number = 0
    variables = []  # List of variables in code
    for line in source_code:
        cur_line_number += 1
        matches = re.finditer(variable_regexp, line, re.MULTILINE)
        for match in matches:
            variables.append(Variable(match.group(0), cur_line_number, match.group(6), match.group(4)))
    return variables


def get_declared_threads(source_code, analyzer_context) -> List[Thread]:
    """
    Function to get a list of all declared threads
    :param analyzer_context: context of the application
    :param source_code: analyzed source code
    :return: list of Threads
    :rtype: List[Thread]
    """
    cur_line_number = 0
    threads = []  # List of threads in code
    for line in source_code:
        cur_line_number += 1
        matches = re.finditer(thread_regexp, line)
        for match in matches:
            cur_thread_params = get_parameters(match.group(0), analyzer_context)
            threads.append(Thread(match.group(0), cur_line_number, match.group(1), match.group(2), cur_thread_params))
    return threads


def get_parameters(raw_parameters: str, analyzer_context: AnalyzerContext) -> List[Variable]:
    """
    Function to get a list of parameters from function or thread declaration
    This parameters are linked with some declared variable
    :param analyzer_context: context of the application
    :param raw_parameters: source code with parameters to parse: "(param1, param2, param3, ...)"
    :return: list of Variables
    :rtype: List[Variable]
    """
    tmp = re.split(r"\(.*\)", raw_parameters)
    tmp = raw_parameters[1:-1]
    parameters_list = re.split(r",*\s", tmp)
    v_parameters_list = []
    declared_variables = analyzer_context.get_declared_variables()
    for index, parameter in enumerate(parameters_list):
        for var in declared_variables:
            if parameter == var.var_name:
                v_parameters_list.append(var)
                break
    return v_parameters_list


