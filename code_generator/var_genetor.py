from random import randint as rng


types = ["int", "short", "char", "long", "double", "float", "byte"]


def gen_buffer(indent, generated_vars):
    var_type = types[rng(0, len(types) - 1)]
    var_name = "var" + str(rng(1, 20))
    while var_name in generated_vars:
        var_name = "var" + str(rng(1, 20))
    code = indent + var_type + " " + var_name + "[" + str(rng(1, 500)) + "];\n"
    return var_name, code


def gen_pbuffer(indent, generated_vars):
    var_type = types[rng(0, len(types) - 1)]
    var_name = "var" + str(rng(1, 20))
    while var_name in generated_vars:
        var_name = "var" + str(rng(1, 20))
    code = indent + var_type + " *" + var_name + ";\n"
    return var_name, code


def gen_var(indent, generated_vars):
    var_type = types[rng(0, len(types) - 1)]
    var_name = "var" + str(rng(1, 20))
    while var_name in generated_vars:
        var_name = "var" + str(rng(1, 20))
    code = indent + var_type + " " + var_name + ";\n"
    return var_name, code


def gen_var_with_value(indent, generated_vars):
    var_type = types[rng(0, len(types) - 1)]
    var_name = "var" + str(rng(1, 20))
    while var_name in generated_vars:
        var_name = "var" + str(rng(1, 20))
    code = indent + var_type + " " + var_name + " = " + str(rng(1, 500)) + ";\n"
    return var_name, code
