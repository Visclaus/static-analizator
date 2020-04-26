import re
from typing import List

from core.function_variable import FunctionVariable
from core.thread import Thread
from core.variable import Variable
from core.function_context import FunctionContext


def find_contexts(source_code):
    initial_contexts = get_initial_contexts(source_code)
    for context in initial_contexts:
        context.variables = get_declared_variables(context.source_code)
        context.threads = get_declared_threads(context.source_code, context.variables)
    return initial_contexts


def get_initial_contexts(source_code):
    f_decl = \
        r"(char|unsigned char|signed char|int|byte|unsigned int|signed int|short int|unsigned short int|" \
        r"signed short int|long int|singed long int|unsigned long int|long long int|signed long long int|" \
        r"unsigned long long int|float|double|long double|wchar_t|short|long|void)\s*" \
        r"(\**\s+)?" \
        r"(\w+)\s*" \
        r"(\(.*\))"
    found_contexts = []
    cur_context = None
    open_br = 0
    close_br = 0
    for cur_line_number, line in enumerate(source_code):
        cur_line_number += 1
        match = re.match(f_decl, line)
        if match is not None:
            open_br += 1
            cur_context = FunctionContext()
            cur_context.return_type = match.group(1) + match.group(2).rstrip() if match.group(2) is not None else match.group(1)
            cur_context.name = match.group(3)
            cur_context.parameters = get_context_parameters(line)
            cur_context.source_code.append({line: cur_line_number})

        elif cur_context is not None:

            if re.match(r'}', line) is None:
                if re.match(r'.*{', line) is not None:
                    open_br += 1
                cur_context.source_code.append({line: cur_line_number})

            if re.match(r'}', line):
                close_br += 1
                if open_br != close_br:
                    cur_context.source_code.append({line: cur_line_number})

                elif open_br == close_br:
                    cur_context.source_code.append({line: cur_line_number})
                    found_contexts.append(cur_context)
                    cur_context = None
                    open_br = 0
                    close_br = 0
    return found_contexts


def get_declared_variables(source_code):
    variable_regexp = \
        r"^\s*" \
        r"(extern\s+)?" \
        r"(const\s+)?" \
        r"(char|unsigned char|signed char|int|byte|short|long|ofstream|ifstream" \
        r"|unsigned int|signed int|short int|unsigned short int|signed short int|long int|singed long int" \
        r"|unsigned long int|long long int|signed long long int|unsigned long long int|float|double|long double|wchar_t)\s+" \
        r"(\*+)?" \
        r"([\w]*[\w\d_]*)\s*" \
        r"(\[.+])?\s*" \
        r"(=.+)?" \
        r"(\s*;)"
    found_variables = []
    for line in source_code:
        cur_line_number = list(line.values())[0]
        processed_line = list(line.keys())[0]
        matches = re.finditer(variable_regexp, processed_line, re.MULTILINE)
        for match in matches:
            var = Variable(match.group(0).strip(), cur_line_number, match.group(5), match.group(3))
            if match.group(7) is not None:
                var.value = match.group(7)[1:].strip()
            found_variables.append(var)
    variable_regexp_1 = \
        r"^\s*" \
        r"([\w]*[\w\d_]*)\s*" \
        r"(=.+)+" \
        r"(\s*;)"
    for line in source_code:
        processed_line = list(line.keys())[0]
        matches = re.finditer(variable_regexp_1, processed_line, re.MULTILINE)
        for match in matches:
            for var in found_variables:
                if match.group(1) == var.var_name:
                    var.value = match.group(2)[1:].strip()
    return found_variables


def get_declared_threads(source_code, declared_variables):
    """
    Function to get a list of all declared threads
    :param declared_variables:
    :param source_code: analyzed source code
    :return: list of Threads
    :rtype: List[Thread]
    """
    thread_regexp = r'^\s*std::thread\s+([a-zA-Z0-9_:<>]*)\(([a-zA-Z0-9_:<>]*)(,\s?[a-zA-Z0-9_:<>]*|,\s?"[a-zA-Z0-9_:<>]*"*)*\)'
    found_threads = []  # List of threads in code
    for line in source_code:
        cur_line_number = list(line.values())[0]
        processed_line = list(line.keys())[0]
        matches = re.finditer(thread_regexp, processed_line)
        for match in matches:
            cur_thread_params = get_parameters(match.group(0), declared_variables)
            found_threads.append(
                Thread(match.group(0), cur_line_number, match.group(1), match.group(2), cur_thread_params))
    return found_threads


def get_parameters(raw_parameters, declared_variables) -> List[Variable]:
    """
    Function to get a list of parameters from called function or thread declaration
    This parameters are linked with declared variable
    :param declared_variables:
    :param raw_parameters: source code with parameters to parse: "(param1, param2, param3, ...)"
    :return: list of Variables
    :rtype: List[Variable]
    """
    tmp = re.search(r"\(.*\)", raw_parameters).group(0)[1:-1]
    parameters_list = re.split(r",", tmp)
    v_parameters_list = []
    for index, parameter in enumerate(parameters_list):
        for var in declared_variables:
            if re.sub(r'\[.*\]', '', parameter.strip()) == var.var_name:
                v_parameters_list.append(var)
                break
    return v_parameters_list

def get_p(string, line_appeared):
    tmp = re.search(r"\(.*\)", string).group(0)[1:-1]
    parameters_list = re.split(r",", tmp)
    for param in parameters_list:
        tmp_1 = param.split()
        variable = Variable(param, line_appeared, tmp_1[1], tmp_1[0])

def get_context_parameters(raw_parameters):
    reg_exp = \
        r"(char|unsigned char|signed char|int|byte|unsigned int|signed int|short int|unsigned short int|" \
        r"signed short int|long int|singed long int|unsigned long int|long long int|signed long long int|" \
        r"unsigned long long int|float|double|long double|wchar_t|short|long)\s+" \
        r"(\*)*" \
        r"([a-zA-Z0-9_]+)\s*" \
        r"(\[.*\])*"
    tmp = re.search(r"\(.*\)", raw_parameters).group(0)[1:-1]
    v_parameters_list = []
    if tmp != '':
        parameters_list = re.split(r",\s*", tmp)
        for parameter in parameters_list:
            match = re.match(reg_exp, parameter)
            v_parameters_list.append(FunctionVariable(match.group(1), match.group(3)))
    return v_parameters_list
