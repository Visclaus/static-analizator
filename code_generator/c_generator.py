import random
from code_generator.var_genetor import *

gen_variables_funcs = [gen_var, gen_var_with_value, gen_buffer, gen_pbuffer]
start_context_pattern = r'(int|short|char|long|double|float|byte|void)\s+([a-zA-Z0-9_]+)\s*(\(.*\))'
func_types = ["char", "unsigned char", "signed char", "int", "byte", "unsigned int", "signed int", "short int",
              "unsigned short int", "signed short int", "long int", "singed long int", "unsigned long int",
              "long long int", "signed long long int", "unsigned long long int", "float", "double", "long double",
              "wchar_t", "void"]

sample_words = ["Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "sed", "do", "eiusmod",
                "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua", "Ut", "enim", "ad", "minim",
                "veniam", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea",
                "commodo", "consequat.", "Duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate",
                "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur.", "Excepteur", "sint",
                "occaecat", "cupidatat", "non", "proident,", "sunt", "in", "culpa", "qui", "officia", "deserunt",
                "mollit", "anim", "id", "est", "laborum."
                ]
cond = ["==", "<", ">", "<=", ">=", "!="]
types = func_types[:-1]


# возвращает рандомный элемент указанного множества
def r_v(params):
    return params[rng(0, len(params) - 1)]


# генерирует n неповторяющихся значений от min до max
def gen_n_rands(n, min_v, max_v):
    rands = []
    for index in range(n):
        cur_rng = rng(min_v, max_v)
        while cur_rng in rands:
            cur_rng = rng(min_v, max_v)
        rands.append(cur_rng)
    return rands


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
    cur_generators = random_code_generators
    cur_generators.remove(gen_cond)
    own_indent = "\t"
    declaration = indent + "if(" + r_v(params) + " " + r_v(cond) + " " + str(rng(0, 500)) + ") {\n"
    body = ""
    for index in range(1):
        body += r_v(cur_generators)(own_indent + indent, params)
    code = declaration + body + indent + "}\n"
    return code


# генерирует блок try-catch с рандомным содержанием
def gen_try_catch(indent, params):
    cur_generators = random_code_generators
    cur_generators.remove(gen_try_catch)
    own_indent = "\t"
    try_declaration = indent + "try {\n"
    try_body = ""
    for index in range(1):
        try_body += r_v(cur_generators)(own_indent + indent, params)
    catch_declaration = indent + "catch (Exception_" + str(rng(1, 20)) + " err) {\n"
    catch_body = ""
    if rng(0, 1) == 1:
        for index in range(1):
            catch_body += r_v(cur_generators)(own_indent + indent, params)
    else:
        catch_body = "\n"
    code = try_declaration + try_body + indent + "}\n" + catch_declaration + catch_body + indent + "}\n"
    return code


# генерирует ошибку переполнения буфера
def gen_buff_error(indent, params):
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
    cur_func_dict = funcs[rng(0, len(funcs) - 1)]
    cur_func = list(cur_func_dict.keys())[0]
    n = list(cur_func_dict.values())[0]
    chosen_param_list = [params[param] for param in gen_n_rands(n, 0, len(params) - 1)]
    code = indent + cur_func + ", ".join(chosen_param_list) + ");\n"
    return code


def gen_cintro_error(indent, file, params):
    funcs = ["system", "popen", "execlp", "execvp", "ShellExecute"]
    file.write(
        indent + funcs[random.randint(0, len(funcs) - 1)] + "(" + params[random.randint(0, len(params) - 1)] + ", " +
        params[
            random.randint(0, len(params) - 1)] + ");\n")


def gen_data_leak(indent, file, params):
    funcs = ["GetLastError", "SHGetFolderPath", "SHGetFolderPathAndSubDir", "SHGetSpecialFolderPath",
             "GetEnvironmentStrings", "GetEnvironmentVariable", "*printf", "errno", "getenv", "strerror", "perror"]
    file.write(
        indent + funcs[random.randint(0, len(funcs) - 1)] + "(" + params[random.randint(0, len(params) - 1)] + ", " +
        params[
            random.randint(0, len(params) - 1)] + ");\n")


def gen_storage_error(indent, file, params):
    funcs = ["SetFileSecurity", "SetKernelObjectSecurity", "SetSecurityDescriptorDacl", "SetServiceObjectSecurity",
             "SetUserObjectSecurity", "SECURITY_DESCRIPTOR", "ConvertStringSecurityDescriptorToSecurityDescriptor",
             "chmod", "fchmod", "chown", "fchown", "fcntl", "setgroups", "acl_*"]
    file.write(
        indent + funcs[random.randint(0, len(funcs) - 1)] + "(" + params[random.randint(0, len(params) - 1)] + ", " +
        params[
            random.randint(0, len(params) - 1)] + ");\n")


# сюда можно добавить любой из объявленных генераторов
random_code_generators = [gen_cout, gen_cond, gen_try_catch, gen_buff_error]


class CodeGenerator:

    def gen_function(self, vulnerability):
        indent = "\t"
        file = open('../tests/a.cpp', 'w')

        # Генерация сигнатуры функции
        func_type = func_types[rng(0, len(types) - 1)]
        func_name = "function" + str(rng(0, 100))

        func_param_names = []
        func_params = []
        for index in range(rng(1, 4)):
            param_type = types[rng(0, len(types) - 1)]
            param_name = "param" + str(rng(0, 100))
            while param_name in func_param_names:
                param_name = "param" + str(rng(0, 100))
            func_param_names.append(param_name)
            func_params.append(param_type + " " + param_name)

        file.write(func_type + " " + func_name + "(" + ", ".join(func_params) + ") {\n")
        # Генерация переменных
        generated_vars = []
        name, code = gen_buffer(indent, generated_vars)
        generated_vars.append(name)
        file.write(code)
        for index in range(rng(3, 6)):
            name, code = gen_variables_funcs[rng(0, len(gen_variables_funcs) - 1)](indent, generated_vars)
            generated_vars.append(name)
            file.write(code)
        file.write(gen_cout(indent, generated_vars))
        # Генерация произвольного кода
        for index in range(rng(2, 5)):
            file.write(random_code_generators[rng(0, len(random_code_generators) - 1)](indent, generated_vars))

        # Генерация уязвимости
        if vulnerability == "buff":
            generated_vars.append(name)
            file.write(code)
            file.write(gen_buff_error(indent, generated_vars))

        # Генерация произвольного кода
        for index in range(rng(2, 5)):
            file.write(random_code_generators[rng(0, len(random_code_generators) - 1)](indent, generated_vars))

        # Конец функции
        file.write("}")


if __name__ == '__main__':
    gen = CodeGenerator()
    gen.gen_function("buff")
