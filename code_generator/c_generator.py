import random
from code_generator.var_genetor import *

gen_variables_funcs = [gen_var, gen_var_with_value, gen_buffer, gen_pbuffer]
start_context_pattern = r'(int|short|char|long|double|float|byte|void)\s+([a-zA-Z0-9_]+)\s*(\(.*\))'
func_types = ["char", "unsigned char", "signed char", "int", "byte", "unsigned int", "signed int", "short int",
              "unsigned short int", "signed short int", "long int", "singed long int", "unsigned long int",
              "long long int", "signed long long int", "unsigned long long int", "float", "double", "long double",
              "wchar_t", "void"]

types = func_types[:-1]


# генерирует n неповторяющихся значений от min до max
def gen_n_rands(n, min_v, max_v):
    rands = []
    for index in range(n):
        cur_rng = rng(min_v, max_v)
        while cur_rng in rands:
            cur_rng = rng(min_v, max_v)
        rands.append(cur_rng)
    return rands


def gen_cond(indent, params):
    code = indent + "if(file.isopen()) {\n" + \
           indent + "\tcout << \"Hello World\" << endl;\n" + \
           indent + "\tprintf(\"random_code\");\n" + \
           indent + "}\n"
    return code


def gen_try_catch(indent, params):
    code = indent + "try {\n" + \
           indent + "\tmd = GetNetworkResource();\n" + \
           indent + "\tprintf(\"random_code\");\n" + \
           indent + "}\n" + \
           indent + "catch (const networkIOException& e) {\n" + \
           indent + "\tcerr << e.what();\n" + \
           indent + "}\n"
    return code


def gen_try_empty_catch(indent, params):
    code = indent + "try {\n" + \
           indent + "\tmd = GetNetworkResource();\n" + \
           indent + "\tprintf(\"random_code\");\n" + \
           indent + "}\n" + \
           indent + "catch (const networkIOException& e) {\n" + \
           indent + "\n" + \
           indent + "}\n" + \
           indent + "catch (const networkIOException& e) {\n" + \
           indent + "\n" + \
           indent + "}\n" + \
           indent + "catch (const networkIOException& e) {\n" + \
           indent + "\tcerr << e.what();\n" + \
           indent + "}\n"
    return code


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
random_code_generators = [gen_cond, gen_try_catch, gen_try_empty_catch, gen_buff_error]


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
