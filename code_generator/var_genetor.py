from typing import List
from utils import constants
from code_generator.rng_utils import *

max_val = 2000


def gen_buffer(indent, generated_vars: List[tuple]):
    var_type = rand_value(constants.types)
    var_name = "var_" + str(rng(1, max_val))
    while var_name in [gen_vars[0] for gen_vars in generated_vars]:
        var_name = "var_" + str(rng(1, max_val))
    code = indent + var_type + " " + var_name + "[" + str(rng(1, 50)) + "];\n"
    generated_vars.append((var_name, code))
    return code


def gen_pointer(indent, generated_vars: List[tuple]):
    var_type = rand_value(constants.types)
    var_name = "var_" + str(rng(1, max_val))
    while var_name in [gen_vars[0] for gen_vars in generated_vars]:
        var_name = "var_" + str(rng(1, max_val))
    code = indent + var_type + " *" + var_name + ";\n"
    generated_vars.append((var_name, code))
    return code


def gen_var(indent, generated_vars: List[tuple]):
    var_type = rand_value(constants.types)
    var_name = "var_" + str(rng(1, max_val))
    while var_name in [gen_vars[0] for gen_vars in generated_vars]:
        var_name = "var_" + str(rng(1, max_val))
    code = indent + var_type + " " + var_name + ";\n"
    generated_vars.append((var_name, code))
    return code


def gen_var_with_value(indent, generated_vars: List[tuple]):
    var_type = rand_value(constants.types)
    var_name = "var_" + str(rng(1, max_val))
    while var_name in [gen_vars[0] for gen_vars in generated_vars]:
        var_name = "var_" + str(rng(1, max_val))
    code = indent + var_type + " " + var_name + " = " + str(rng(1, 30)) + ";\n"
    generated_vars.append((var_name, code))
    return code


def gen_stream(indent, generated_vars: List[tuple]):
    var_type = rand_value(constants.stream_types)
    var_name = "var_" + str(rng(1, max_val))
    while var_name in [gen_vars[0] for gen_vars in generated_vars]:
        var_name = "var_" + str(rng(1, max_val))
    code = indent + var_type + " " + var_name + ".open(\"D://" + rand_value(constants.sample_words) + "\");\n"
    generated_vars.append((var_name, code))
    return code


def gen_integer_with_value(indent, generated_vars: List[tuple]):
    var_type = rand_value(constants.int_types)
    var_name = "var_" + str(rng(1, max_val))
    while var_name in [gen_vars[0] for gen_vars in generated_vars]:
        var_name = "var_" + str(rng(1, max_val))
    max_over = constants.integer_limits[var_type].max
    code = indent + var_type + " " + var_name + " = " + str(rng(int(max_over/2), max_over)) + ";\n"
    generated_vars.append((var_name, code))
    return code


if __name__ == '__main__':
    for _ in range(10):
        print(gen_integer_with_value("", []))
