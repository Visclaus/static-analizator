from typing import List
from utils import constants
from code_generator.rng_utils import *

max_val = 20


def gen_buffer(indent, generated_vars: List[str]):
    var_type = r_v(constants.types)
    var_name = "var_" + str(rng(1, max_val))
    while var_name in generated_vars:
        var_name = "var_" + str(rng(1, max_val))
    generated_vars.append(var_name)
    code = indent + var_type + " " + var_name + "[" + str(rng(1, 50)) + "];\n"
    return code


def gen_pointer(indent, generated_vars: List[str]):
    var_type = r_v(constants.types)
    var_name = "var_" + str(rng(1, max_val))
    while var_name in generated_vars:
        var_name = "var_" + str(rng(1, max_val))
    generated_vars.append(var_name)
    code = indent + var_type + " *" + var_name + ";\n"
    return code


def gen_var(indent, generated_vars: List[str]):
    var_type = r_v(constants.types)
    var_name = "var_" + str(rng(1, max_val))
    while var_name in generated_vars:
        var_name = "var_" + str(rng(1, max_val))
    generated_vars.append(var_name)
    code = indent + var_type + " " + var_name + ";\n"
    return code


def gen_var_with_value(indent, generated_vars: List[str]):
    var_type = r_v(constants.types)
    var_name = "var_" + str(rng(1, max_val))
    while var_name in generated_vars:
        var_name = "var_" + str(rng(1, max_val))
    generated_vars.append(var_name)
    code = indent + var_type + " " + var_name + " = " + str(rng(1, 30)) + ";\n"
    return code


def gen_stream(indent, generated_vars: List[str]):
    var_type = r_v(constants.stream_types)
    var_name = "var_" + str(rng(1, max_val))
    while var_name in generated_vars:
        var_name = "var_" + str(rng(1, max_val))
    generated_vars.append(var_name)
    code = indent + var_type + " " + var_name + ".open(\"D://" + r_v(constants.sample_words) + "\");\n"
    return code


def gen_integer_with_value(indent, generated_vars: List[str]):
    var_type = r_v(constants.int_types)
    var_name = "var_" + str(rng(1, max_val))
    while var_name in generated_vars:
        var_name = "var_" + str(rng(1, max_val))
    generated_vars.append(var_name)
    max_over = constants.integer_limits[var_type].max
    code = indent + var_type + " " + var_name + " = " + str(rng(int(max_over/2), max_over)) + ";\n"
    return code


if __name__ == '__main__':
    for _ in range(10):
        print(gen_integer_with_value("", []))
