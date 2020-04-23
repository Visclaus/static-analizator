import random
from code_generator.var_genetor import *
from code_generator.constants import *

gen_variables_funcs = [gen_var, gen_var_with_value, gen_buffer, gen_pointer]


# генерирует рандомный cout
def gen_cout(indent, params):
    sample_text = ""
    param = r_v(params)
    for _ in range(3):
        sample_text += r_v(sample_words) + " "
    code = indent + "cout<<\"" + sample_text + "\"<<" + param + ";\n"
    return code


# генерирует if statement с рандомным содержанием
def gen_cond(indent, params):
    cur_generators = random_code_generators.copy()
    cur_generators.remove(gen_cond)
    own_indent = "\t"
    declaration = indent + "if(" + r_v(params) + " " + r_v(cond) + " " + str(rng(0, 500)) + ") {\n"
    body = ""
    for index in range(2):
        body += r_v(cur_generators)(own_indent + indent, params)
    code = declaration + body + indent + "}\n"
    return code


# генерирует блок try-catch с рандомным содержанием
def gen_try_catch(indent, params):
    cur_generators = random_code_generators.copy()
    # cur_generators.remove(gen_try_catch)
    own_indent = "\t"
    try_declaration = indent + "try {\n"
    try_body = ""
    for index in range(3):
        try_body += r_v(cur_generators)(own_indent + indent, params)
    catch_declaration = indent + "catch (Exception_" + str(rng(1, 20)) + " err) {\n"
    catch_body = ""
    if rng(0, 1) == 1:
        for index in range(2):
            catch_body += r_v(cur_generators)(own_indent + indent, params)
    else:
        catch_body = "\n"
    code = try_declaration + try_body + indent + "}\n" + catch_declaration + catch_body + indent + "}\n"
    return code


# генерирует ошибку переполнения буфера
def buff_error(indent, params):
    funcs = [
        {"strcpy(": 2},
        {"printf(Overflow %s and %s, ": 2},
        {"memcpy(": 3},
        {"strcat(": 2},
        {"gets(": 1},
        {"sprintf(": 3},
        {"vsprintf(": 3},
        {"strncpy(": 3},
        {"scanf(%s, ": 1},
    ]
    cur_func_dict = r_v(funcs)
    cur_func = list(cur_func_dict.keys())[0]
    n = list(cur_func_dict.values())[0]
    chosen_param_list = [params[param] for param in gen_n_rands(n, 0, len(params) - 1)]
    code = indent + cur_func + ", ".join(chosen_param_list) + ");\n"
    return code


# генерирует ошибку встраивания команд
def c_intr_error(indent, params):
    funcs = [
        {"system(": 1},
        {"popen(": 2},
        {"execlp(": 3},
        {"execvp(": 2},
        {"ShellExecute(": 6},
    ]
    cur_func_dict = r_v(funcs)
    cur_func = list(cur_func_dict.keys())[0]
    n = list(cur_func_dict.values())[0]
    chosen_param_list = [params[param] for param in gen_n_rands(n, 0, len(params) - 1)]
    code = indent + cur_func + ", ".join(chosen_param_list) + ");\n"
    return code


# генерирует ошибку утечки информации
def data_leak(indent, params):
    funcs = [
        {"GetLastError(": 0},
        {"SHGetFolderPath(": 5},
        {"GetEnvironmentStrings(": 0},
        {"GetEnvironmentVariable(": 1},
        {"errno": 0},
        {"getenv(": 1},
        {"strerror(": 1},
        {"perror(": 1}
    ]
    cur_func_dict = r_v(funcs)
    cur_func = list(cur_func_dict.keys())[0]
    if cur_func == "errno":
        code = indent + "cout<<" + cur_func + ";\n"
        return code
    n = list(cur_func_dict.values())[0]
    chosen_param_list = [params[param] for param in gen_n_rands(n, 0, len(params) - 1)]
    code = indent + cur_func + ", ".join(chosen_param_list) + ");\n"
    return code


def storage_error(indent, params):
    funcs = [
        {"SetFileSecurity(": 3},
        {"SetKernelObjectSecurity(": 3},
        {"SetServiceObjectSecurity(": 3},
        {"chmod(": 2},
        {"fchmod(": 2},
        {"fchown(": 3},
        {"fcntl(": 3},
        {"setgroups(": 2}
    ]
    cur_func_dict = r_v(funcs)
    cur_func = list(cur_func_dict.keys())[0]
    n = list(cur_func_dict.values())[0]
    chosen_param_list = [params[param] for param in gen_n_rands(n, 0, len(params) - 1)]
    code = indent + cur_func + ", ".join(chosen_param_list) + ");\n"
    return code


# сюда можно добавить любой из объявленных генераторов
random_code_generators = [gen_cout, gen_cond, gen_try_catch, buff_error, c_intr_error, data_leak, storage_error]


class CodeGenerator:

    def gen_function(self, vulnerability):
        indent = "\t"
        file = open('../tests/a.cpp', 'w')

        # Генерация сигнатуры функции
        func_type = r_v(func_types)
        func_name = "function_" + str(rng(0, 20))
        generated_vars = []
        func_params = []
        gen_params_funcs = gen_variables_funcs.copy()
        gen_params_funcs.remove(gen_var_with_value)
        gen_params_funcs.remove(gen_buffer)
        for index in range(rng(1, 4)):
            func_params.append(r_v(gen_params_funcs)(indent, generated_vars))
        file.write(func_type + " " + func_name + "(" + ", ".join([param[1:-2] for param in func_params]) + ") {\n")

        # Генерация переменных
        file.write(gen_buffer(indent, generated_vars))
        for index in range(rng(6, 7)):
            code = r_v(gen_variables_funcs)(indent, generated_vars)
            file.write(code)
        file.write(gen_cout(indent, generated_vars))

        # Генерация произвольного кода
        for index in range(rng(2, 5)):
            file.write(r_v(random_code_generators)(indent, generated_vars))

        # Генерация уязвимости
        if vulnerability == "buff":
            file.write(buff_error(indent, generated_vars))

        # Генерация произвольного кода
        for index in range(rng(2, 5)):
            file.write(r_v(random_code_generators)(indent, generated_vars))

        # Конец функции
        file.write("}")


if __name__ == '__main__':
    gen = CodeGenerator()
    gen.gen_function("buff")
