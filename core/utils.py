from typing import List

from core.variable import Variable


def replace_var_list(var_list: List[Variable]):
    new_list = []
    for var in var_list:
        new_list.append(var.var_name)
    return new_list

