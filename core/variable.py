import collections
import re


def is_pointer(variable_declaration):
    return True if re.search(r"\*", variable_declaration) else False


def is_array(variable_declaration):
    return True if re.search(r"\[.*]", variable_declaration) else False


class Variable:
    def __init__(self, full_declaration, line_appeared, var_name, var_type, value=None, linked_variable=None):
        self.full_declaration = full_declaration
        self.line_appeared = line_appeared
        self.var_name = var_name
        self.var_type = var_type
        self.value = value
        self.linked_variable = linked_variable
