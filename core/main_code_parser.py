import re
from typing import List
from core import regexs_constants as rc
from core.function_context import FunctionContext
from core.thread import Thread
from core.variable import Variable


def find_contexts(source_code):
    """
    Метод для поиска и анализа контекстов в текущем файле.
    Контексты в данном случае - глобальные лексемы языка, такие как функции, структуры и классы.
    В данный момент реализован поиск функций.
    Изначально ведется разбиение всего кода на контексты, а затем анализ каждого из них, например, на наличие
    объявленных переменных поток и т.д.
    :rtype List[FunctionContext]
    """
    func_declarations = get_func_declarations(source_code)
    for func in func_declarations:
        func.variables = get_declared_variables(func.source_code)
        func.threads = get_declared_threads(func.source_code, func.variables)
    return func_declarations


def get_func_declarations(source_code):
    """
    Поиск сигнатур функций и формирование из них объектов.
    :rtype List[FunctionContext]
    """
    func_declarations = []
    cur_func = None
    open_br = 0
    close_br = 0

    for line_number, line in enumerate(source_code):
        line_number += 1

        open_bracer_matches = re.finditer(r"{", line)
        for _ in open_bracer_matches:
            open_br += 1

        close_bracer_matches = re.finditer(r"}", line)
        for _ in close_bracer_matches:
            close_br += 1

        func_match = re.match(rc.func_decl_regexp, line, re.MULTILINE)
        if func_match is not None:
            pointer = func_match.group(2)
            return_type = func_match.group(1) + pointer.rstrip() if pointer is not None else func_match.group(1)
            name = func_match.group(3)
            parameters = get_func_params(func_match.group(4), line_number)
            cur_func = FunctionContext(return_type, name, parameters)
            cur_func.source_code[line_number] = line

        elif cur_func is not None:
            if re.match(r"}", line) is not None:
                if open_br != close_br:
                    cur_func.source_code[line_number] = line

                elif open_br == close_br:
                    cur_func.source_code[line_number] = line
                    func_declarations.append(cur_func)
                    cur_func = None
                    close_br = 0
                    open_br = 0
            else:
                cur_func.source_code[line_number] = line

    return func_declarations


def get_func_params(params_in_bracket, line_number):
    """
    Поиск параметров функции.
    :rtype List[Variable]
    """
    parameters_list = []
    if params_in_bracket[1:-1] == "":
        return parameters_list
    raw_param_list = re.split(r",\s*", params_in_bracket[1:-1])
    for raw_parameter in raw_param_list:
        param_match = re.match(rc.func_param_regexp, raw_parameter)
        pointer = param_match.group(2)
        param_type = param_match.group(1) + pointer.rstrip() if pointer is not None else param_match.group(1)
        param_name = param_match.group(3)
        parameters_list.append(Variable(raw_parameter, line_number, param_name, param_type))
    return parameters_list


def get_declared_variables(source_code):
    """
    Поиск и инициализация всех объявленных переменных в функции.
    :rtype List[Variables]
    """
    variables_list = []
    for line_number, line in source_code.items():
        var_matches = re.finditer(rc.variable_regexp, line, re.MULTILINE)
        for match in var_matches:
            var = Variable(match.group(0).strip(), line_number, match.group(5), match.group(3))
            if match.group(7) is not None:
                var.value = match.group(7)[1:].strip()
            variables_list.append(var)

    for _, line in source_code.items():
        var_matches = re.finditer(rc.assignment_regexp, line, re.MULTILINE)
        for match in var_matches:
            v1 = None
            v2 = None
            for var in variables_list:
                if match.group(1) == var.var_name:
                    v1 = var
                if match.group(2) == var.var_name:
                    v2 = var
            if v1 is not None and v2 is not None:
                v1.value = v2.value
            if v1 is not None and v2 is None:
                v1.value = match.group(2)

    return variables_list


def get_declared_threads(source_code, declared_variables):
    """
    Поиск и инициализация всех объявленных потоков в функции.
    :rtype: List[Thread]
    """
    threads_list = []
    for line_number, line in source_code.items():
        matches = re.finditer(rc.thread_regexp, line)
        for match in matches:
            cur_thread_params = get_parameters(match.group(0), declared_variables)
            threads_list.append(
                Thread(match.group(0), line_number, match.group(2), match.group(3), cur_thread_params))
    return threads_list


def get_parameters(raw_parameters, declared_variables) -> List[Variable]:
    """
    Поиск уже объявленных переменных, которые используются, например, при вызове функции или объявлении потока.
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
