import random
from random import randint as rng

start_context_pattern = r'(int|short|char|long|double|float|byte|void)\s+([a-zA-Z0-9_]+)\s*(\(.*\))'

func_types = ["int", "short", "char", "long", "double", "float", "byte", "void"]
types = func_types[:-1]


def gen_cond_oper(indent, file):
    file.write(indent + "if(true) {\n" +
               indent + "\tcout << \"Hello World\" << endl;\n" +
               indent + "\tprintf(\"random_code\");\n" +
               indent + "}\n")


def gen_try_catch(indent, file):
    file.write(indent + "try {\n" +
               indent + "\tmd = GetNetworkResource();\n" +
               indent + "\tprintf(\"random_code\");\n" +
               indent + "}\n" +
               indent + "catch (const networkIOException& e) {\n" +
               indent + "\tcerr << e.what();\n" +
               indent + "}\n")


def gen_try_empty_catch(indent, file):
    file.write(indent + "try {\n" +
               indent + "\tmd = GetNetworkResource();\n" +
               indent + "\tprintf(\"random_code\");\n" +
               indent + "}\n" +
               indent + "catch (const networkIOException& e) {\n" +
               indent + "\n" +
               indent + "}\n")


def gen_buffer(indent, var_limit_a, file):
    var_type = types[random.randint(0, len(types) - 1)]
    var_name = "var" + str(random.randint(var_limit_a, 20))
    file.write(indent + var_type + " " + var_name + "[" + str(random.randint(1, 500)) + "];\n")
    return var_name


def gen_pbuffer(indent, var_limit_a, file):
    var_type = types[random.randint(0, len(types) - 1)]
    var_name = "var" + str(random.randint(var_limit_a, 20))
    file.write(indent + var_type + " *" + var_name + ";\n")
    return var_name


def gen_var(indent, var_limit_a, file):
    var_type = types[random.randint(0, len(types) - 1)]
    var_name = "var" + str(random.randint(var_limit_a, 20))
    file.write(indent + var_type + " " + var_name + ";\n")
    return var_name


def gen_var_with_value(indent, var_limit_a, file):
    var_name = "var" + str(random.randint(var_limit_a, 20))
    var_type = types[random.randint(0, len(types) - 1)]
    file.write(indent + var_type + " " + var_name + " = " + str(random.randint(1, 500)) + ";\n")
    return var_name


gen_variables_funcs = [gen_var, gen_var_with_value, gen_buffer, gen_pbuffer]


def gen_buff_error(indent, file, params):
    funcs = ["strcpy", "printf", "strcat", "memcpy", "gets", "sprintf", "vsprintf", "strncpy", "scanfs", "sscanf",
             "snscanf", "strlen"]
    cur_func = funcs[rng(0, len(funcs) - 1)]
    rng_1 = rng(0, len(params) - 1)
    rng_2 = rng(0, len(params) - 1)
    while rng_2 == rng_1:
        rng_2 = rng(1, len(params) - 1)
    file.write(indent + cur_func + "(" + params[rng_1] + ", " + params[rng_2] + ");\n")


def gen_cintro_error(indent, file, params):
    funcs = ["system", "popen", "execlp", "execvp", "ShellExecute"]
    file.write(
        indent + funcs[random.randint(0, len(funcs) - 1)] + "(" + params[random.randint(0, len(params) - 1)] + ", " +
        params[
            random.randint(0, len(params) - 1)] + ");\n")


def gen_data_leak(indent, file, vars):
    funcs = ["GetLastError", "SHGetFolderPath", "SHGetFolderPathAndSubDir", "SHGetSpecialFolderPath",
             "GetEnvironmentStrings", "GetEnvironmentVariable", "*printf", "errno", "getenv", "strerror", "perror"]
    file.write(
        indent + funcs[random.randint(0, len(funcs) - 1)] + "(" + vars[random.randint(0, len(vars) - 1)] + ", " + vars[
            random.randint(0, len(vars) - 1)] + ");\n")


def gen_storage_error(indent, file, vars):
    funcs = ["SetFileSecurity", "SetKernelObjectSecurity", "SetSecurityDescriptorDacl", "SetServiceObjectSecurity",
             "SetUserObjectSecurity", "SECURITY_DESCRIPTOR", "ConvertStringSecurityDescriptorToSecurityDescriptor",
             "chmod", "fchmod", "chown", "fchown", "fcntl", "setgroups", "acl_*"]
    file.write(
        indent + funcs[random.randint(0, len(funcs) - 1)] + "(" + vars[random.randint(0, len(vars) - 1)] + ", " + vars[
            random.randint(0, len(vars) - 1)] + ");\n")


class CodeGenerator:
    def __init__(self):
        self.func_limit_a = 1
        self.max_gen_limit = 20

    def gen_func(self, ):
        file = open('text.cpp', 'w')

        func_type = func_types[random.randint(0, len(types) - 1)]
        func_name = "function" + str(random.randint(self.func_limit_a, self.max_gen_limit))
        self.func_limit_a += 1

        params = []
        param_limit_a = 1
        for index in range(random.randint(1, 4)):
            param_type = types[random.randint(0, len(types) - 1)]
            param_name = "param" + str(random.randint(param_limit_a, self.max_gen_limit))
            param_limit_a += 1
            params.append(param_type + " " + param_name)

        file.write(func_type + " " + func_name + "(" + ", ".join(params) + ") {\n")

        generated_vars = []
        param_limit_a = 1
        indent = "\t"
        for index in range(random.randint(2, 5)):
            generated_vars.append(
                gen_variables_funcs[random.randint(0, len(gen_variables_funcs) - 1)](indent, param_limit_a, file))
            param_limit_a += 1
        gen_cond_oper(indent, file)
        gen_try_empty_catch(indent, file)
        gen_buff_error(indent, file, generated_vars)
        gen_try_catch(indent, file)

        file.write("}")


if __name__ == '__main__':
    gen = CodeGenerator()
    gen.gen_func()
