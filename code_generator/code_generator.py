import random

start_context_pattern = r'(int|short|char|long|double|float|byte|void)\s+([a-zA-Z0-9_]+)\s*(\(.*\))'

types = ["int", "void", "double"]
numbers = ["0", "1", "2", "3", "4", "5", "6", 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]


def gen_buffer(file):
    var_type = types[random.randint(0, len(types) - 1)]
    var_name = "var" + str(random.randint(1, 500))
    file.write(var_type + " " + var_name + "[" + str(random.randint(1, 500)) + "];\n")
    return var_name


def gen_pbuffer(file):
    var_type = types[random.randint(0, len(types) - 1)]
    var_name = "var" + str(numbers[random.randint(0, len(numbers) - 1)])
    file.write(var_type + " *" + var_name + ";\n")
    return var_name


def gen_var(file):
    var_type = types[random.randint(0, len(types) - 1)]
    var_name = "var" + str(random.randint(1, 500))
    file.write(var_type + " " + var_name + ";\n")
    return var_name


def gen_var_with_value(file):
    var_name = "var" + str(random.randint(1, 500))
    var_type = types[random.randint(0, len(types) - 1)]
    file.write(var_type + " " + var_name + " = " + str(random.randint(1, 500)) + ";\n")
    return var_name


gen_variables_funcs = [gen_var, gen_var_with_value, gen_buffer, gen_pbuffer]


def gen_buf_error(file, vars):
    funcs = ['strcpy', "printf", "strcat", "memcpy", "gets", "sprintf", "vsprintf", "strncpy", "scanfs", "sscanf",
             "snscanf", "strlen"]
    file.write(funcs[random.randint(0, len(funcs) - 1)] + "(" + vars[random.randint(0, len(vars) - 1)] + ", " + vars[
        random.randint(0, len(vars) - 1)] + ");\n")


def gen_cintro_error(file, vars):
    funcs = ["system", "popen", "execlp", "execvp", "ShellExecute"]
    file.write(funcs[random.randint(0, len(funcs) - 1)] + "(" + vars[random.randint(0, len(vars) - 1)] + ", " + vars[
        random.randint(0, len(vars) - 1)] + ");\n")


def gen_data_leak(file, vars):
    funcs = ["GetLastError", "SHGetFolderPath", "SHGetFolderPathAndSubDir", "SHGetSpecialFolderPath",
             "GetEnvironmentStrings", "GetEnvironmentVariable", "*printf", "errno", "getenv", "strerror", "perror"]
    file.write(funcs[random.randint(0, len(funcs) - 1)] + "(" + vars[random.randint(0, len(vars) - 1)] + ", " + vars[
        random.randint(0, len(vars) - 1)] + ");\n")


def gen_storage_error(file, vars):
    funcs = ["SetFileSecurity", "SetKernelObjectSecurity", "SetSecurityDescriptorDacl", "SetServiceObjectSecurity",
             "SetUserObjectSecurity", "SECURITY_DESCRIPTOR", "ConvertStringSecurityDescriptorToSecurityDescriptor",
             "chmod", "fchmod", "chown", "fchown", "fcntl", "setgroups", "acl_*"]
    file.write(funcs[random.randint(0, len(funcs) - 1)] + "(" + vars[random.randint(0, len(vars) - 1)] + ", " + vars[
        random.randint(0, len(vars) - 1)] + ");\n")


def gen_code():
    f = open('text.txt', 'w')
    f.write(types[random.randint(0, len(types) - 1)] + " function" + str(1) + "(" + types[
        random.randint(0, len(types) - 1)] +
            " param" + str(random.randint(1, 500)) + ", " + types[random.randint(0, len(types) - 1)] +
            " param" + str(random.randint(1, 500)) + ")" +
            "{\n")
    generated_vars = []
    for index in range(random.randint(2, 5)):
        generated_vars.append(gen_variables_funcs[random.randint(0, len(gen_variables_funcs) - 1)](f))
    gen_buf_error(f, generated_vars)
    gen_cintro_error(f, generated_vars)
    gen_data_leak(f, generated_vars)
    gen_storage_error(f, generated_vars)

if __name__ == '__main__':
    gen_code()
