import re

from code_generator.var_genetor import *
from utils.constants import *

v_funcs = [gen_var, gen_var_with_value, gen_buffer, gen_pointer, gen_stream]
p_funcs = [gen_var, gen_pointer]


# генерирует рандомный cout
def gen_cout(indent, params, a_f):
    sample_text = ""
    param = r_v(params)
    for _ in range(3):
        sample_text += r_v(sample_words) + " "
    code = indent + "cout<<\"" + sample_text + "\"<<" + param + ";\n"
    return code


# генерирует if statement с рандомным содержанием
def gen_cond(indent, params, a_f):
    cur_generators = random_code_generators.copy()
    cur_generators.remove(gen_cond)
    own_indent = "\t"
    declaration = indent + "if(" + r_v(params) + " " + r_v(cond) + " " + str(rng(0, 500)) + ") {\n"
    body = ""
    for index in range(2):
        body += r_v(cur_generators)(own_indent + indent, params, a_f)
    code = declaration + body + indent + "}\n"
    return code


# генерирует блок try-catch с рандомным содержанием
def gen_try_catch(indent, params, a_f):
    cur_generators = random_code_generators.copy()
    own_indent = "\t"
    try_declaration = indent + "try {\n"
    try_body = ""
    for index in range(3):
        try_body += r_v(cur_generators)(own_indent + indent, params, a_f)
    catch_declaration = indent + "catch (Exception_" + str(rng(1, 20)) + " err) {\n"
    catch_body = ""
    if rng(0, 1) == 1:
        for index in range(2):
            catch_body += r_v(cur_generators)(own_indent + indent, params, a_f)
    else:
        catch_body = "\n"
    code = try_declaration + try_body + indent + "}\n" + catch_declaration + catch_body + indent + "}\n"
    return code


# генерирует ошибку переполнения буфера
def buff_error(indent, params, a_f):
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
def c_intr_error(indent, params, a_f):
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
def data_leak(indent, params, a_f):
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


def storage_error(indent, params, a_f):
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


def file_error(indent, params, a_f):
    funcs = [
        {"mkdir(": 1},
        {"mktemp(": 1},
        {"rmdir(": 1},
        {"chmod(": 2},
        {"utime(": 2},
        {"open": 0}
    ]
    cur_func_dict = r_v(funcs)
    cur_func = list(cur_func_dict.keys())[0]
    n = list(cur_func_dict.values())[0]
    if cur_func == "open":
        code = indent + r_v(params) + ".open(\"D://" + r_v(sample_words) + "\");\n"
        return code
    chosen_param_list = [params[param] for param in gen_n_rands(n, 0, len(params) - 1)]
    code = indent + cur_func + ", ".join(chosen_param_list) + ");\n"
    return code


def format_error(indent, params, a_f):
    chosen_param_list = [params[param] for param in gen_n_rands(2, 0, len(params) - 1)]
    code = indent + "printf(Format %s and %s, " + ", ".join(chosen_param_list) + ");\n"
    return code


def iover_error(indent, params, a_f):
    cur_generators = random_code_generators.copy()
    cur_generators.remove(iover_error)
    chosen_var_list = []
    for _ in range(3):
        chosen_var_list.append(gen_integer_with_value(indent, params))
    sample_code = ""
    for index in range(1):
        sample_code += r_v(cur_generators)(indent, params, a_f)
    code = "".join(chosen_var_list) + sample_code + indent + chosen_var_list[0].split()[1] + " = " + \
           chosen_var_list[1].split()[1] + \
           " + " + chosen_var_list[2].split()[1] + ";\n"
    return code


def free_error(indent, params, a_f):
    var_type = r_v(constants.types)
    var_name = "var_" + str(rng(1, max_val))
    while var_name in params:
        var_name = "var_" + str(rng(1, max_val))
    params.append(var_name)
    code = indent + var_type + " *" + var_name + " = new " + var_type + ";\n"
    return code


def race_error(indent, params, a_f):
    code = ""
    for index in range(rng(2, 5)):
        for i in range(rng(2, 3)):
            code += r_v(random_code_generators)(indent, params, a_f)
        chosen_param_list = [params[param] for param in gen_n_rands(3, 0, len(params) - 1)]
        code += indent + "std::thread t" + str(index) + "(" + r_v(a_f) + ", " + ", ".join(chosen_param_list) + ");\n"
    return code


def rng_error(indent, params, a_f):
    funcs = [
        {"srand(": 1},
        {"rand(": 0},
        {"uniform_real_distribution(": 0}
    ]
    cur_func_dict = r_v(funcs)
    cur_func = list(cur_func_dict.keys())[0]
    if cur_func == "uniform_real_distribution(":
        code = indent + "std::uniform_real_distribution<> dis(" + str(rng(1, 3)) + ", " + str(rng(1, 9)) + ");\n"
        return code
    if cur_func == "srand(":
        code = indent + cur_func + str(rng(3, 100)) + ");\n"
        return code
    else:
        code = indent + cur_func + ");\n"
        return code


def readers_error(indent, params, a_f):
    code = ""
    for index in range(rng(2, 5)):
        for i in range(rng(2, 3)):
            code += r_v(random_code_generators)(indent, params, a_f)
        chosen_param_list = [params[param] for param in gen_n_rands(4, 0, len(params) - 1)]
        code += indent + "std::thread t" + str(index) + "(" + r_v(a_f) + ", " + ", ".join(chosen_param_list) + ");\n"
    return code


def sql_error(indent, params, a_f):
    funcs = ["execute(", "executeQuery("]
    cur_func = r_v(funcs)
    sample_text = ""
    for _ in range(3):
        sample_text += r_v(sample_words) + "'"
    random = rng(0, 1)
    if random == 0:
        code = indent + cur_func + "\"" + sample_text + "\");\n"
    else:
        code = indent + cur_func + r_v(params) + ");\n"
    return code


random_code_generators = [gen_cout, gen_cond, gen_try_catch, buff_error, c_intr_error, data_leak, storage_error,
                          file_error, format_error, iover_error, free_error, rng_error, sql_error]

name_generator = {
    "buff": buff_error,
    "cintr": c_intr_error,
    "data_leak": data_leak,
    "dstor": storage_error,
    "catch": gen_try_catch,
    "fileacc": file_error,
    "formats": format_error,
    "integ": iover_error,
    "mem": free_error,
    "race": race_error,
    "rng": rng_error,
    "readers": readers_error,
    "sql": sql_error
}


class CodeGenerator:
    cur_available_funcs = []

    def gen_sample_function(self, file):
        indent = "\t"
        # Генерация сигнатуры функции
        func_type = r_v(func_types)
        func_name = "function_" + str(rng(0, 20))
        generated_vars = []
        func_params = []
        for index in range(rng(1, 4)):
            func_params.append(r_v(p_funcs)(indent, generated_vars))
        file.write(func_type + " " + func_name + "(" + ", ".join([param[1:-2] for param in func_params]) + ") {\n")
        # Генерация переменных
        file.write(gen_buffer(indent, generated_vars))
        for index in range(rng(6, 7)):
            code = r_v(v_funcs)(indent, generated_vars)
            file.write(code)
        file.write(gen_cout(indent, generated_vars, self.cur_available_funcs))
        # Генерация произвольного кода
        for index in range(rng(2, 5)):
            file.write(r_v(random_code_generators)(indent, generated_vars, self.cur_available_funcs))
        # Конец функции
        file.write("}\n")
        return func_name

    def gen_function(self, vuln_generators, file):
        indent = "\t"
        func_type = "int"
        func_name = "main"
        generated_vars = []
        func_params = []
        for index in range(rng(1, 4)):
            func_params.append(r_v(p_funcs)(indent, generated_vars))
        file.write(func_type + " " + func_name + "() {\n")
        for index in range(rng(6, 7)):
            code = r_v(v_funcs)(indent, generated_vars)
            file.write(code)
        for generator in vuln_generators:
            for index in range(rng(2, 3)):
                file.write(r_v(random_code_generators)(indent, generated_vars, self.cur_available_funcs))
            file.write(generator(indent, generated_vars, self.cur_available_funcs))
        file.write("}\n")
        return func_name

    def gen_code(self, vulnerabilities: List[str], test_numbers):
        for index in range(test_numbers):
            file = open('../generated_tests/' + "+".join(vulnerabilities) + str(index + 1) + '.cpp', 'w')
            self.cur_available_funcs = [self.gen_sample_function(file)]
            generators = []
            for vuln in vulnerabilities:
                generators.append(name_generator[vuln])
            self.gen_function(generators, file)
            self.cur_available_funcs = []


if __name__ == '__main__':
    gen = CodeGenerator()
    gen.gen_code(["readers", "mem", "catch"], 10)
