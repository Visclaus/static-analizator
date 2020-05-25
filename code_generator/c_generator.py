import os
import re
import main
from code_generator.var_genetor import *
from core.main_code_parser import find_contexts
from core.variable import is_pointer, is_array
from utils.constants import *
from utils.initial_parse import clean_code

v_funcs = [gen_var, gen_var_with_value, gen_buffer, gen_pointer]
p_funcs = [gen_var, gen_pointer]


class CodeGenerator:
    cur_available_funcs = []
    mutexes = []
    final_output = [["Переполнение буфера", 0], ["Внедрение команд", 0], ["Утечка информации", 0],
                    ["Небезопасное хранение данных", 0], ["Пренебрежение обработкой исключений", 0],
                    ["Некорректный доступ к файлам", 0], ["Ошибка форматной строки", 0], ["Переполнение целых чисел", 0],
                    ["Ошибка высвобождения памяти", 0], ["Состояние гонки", 0],
                    ["Случайные числа криптографического характера", 0], ["Читатели Писатели", 0],
                    ["SQL инъекции", 0]]
    final_output_for_test = [["Переполнение буфера", 0], ["Внедрение команд", 0], ["Утечка информации", 0],
                    ["Небезопасное хранение данных", 0], ["Пренебрежение обработкой исключений", 0],
                    ["Некорректный доступ к файлам", 0], ["Ошибка форматной строки", 0],
                    ["Переполнение целых чисел", 0],
                    ["Ошибка высвобождения памяти", 0], ["Состояние гонки", 0],
                    ["Случайные числа криптографического характера", 0], ["Читатели Писатели", 0],
                    ["SQL инъекции", 0]]
    line_number = 1

    # генерирует рандомный cout
    # def gen_cout(self, indent, params):
    #     sample_text = ""
    #     param = r_v(params)
    #     for _ in range(3):
    #         sample_text += r_v(sample_words) + " "
    #     code = indent + "cout<<\"" + sample_text + "\"<<" + param + ";\n"
    #     return code

    # генерирует if statement с рандомным содержанием
    def gen_cond(self, indent, params):
        own_indent = "\t"
        declaration = indent + "if(" + r_v(params)[0] + " " + r_v(cond) + " " + str(rng(0, 500)) + ") {\n"
        self.line_number += 1
        body = ""
        for index in range(2):
            body += r_v(self.cond_generators)(self, own_indent + indent, params)
        code = declaration + body + indent + "}\n"
        self.line_number += 1
        return code

    # генерирует блок try-catch с рандомным содержанием
    def gen_try_catch(self, indent, params):
        own_indent = "\t"
        try_declaration = indent + "try {\n"
        self.line_number += 1
        try_body = ""
        for index in range(3):
            try_body += r_v(self.catch_generators)(self, own_indent + indent, params)
        catch_declaration = indent + "catch (Exception_" + str(rng(1, 20)) + " err) {\n"
        self.line_number += 1
        catch_body = ""
        if rng(0, 1) == 1:
            for index in range(2):
                catch_body += r_v(self.catch_generators)(self, own_indent + indent, params)
        else:
            catch_body = "\n"
            for i in self.final_output:
                if "Пренебрежение обработкой исключений" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
            self.line_number += 1
        code = try_declaration + try_body + indent + "}\n" + catch_declaration + catch_body + indent + "}\n"
        self.line_number += 2
        return code

    # генерирует ошибку переполнения буфера
    def buff_error(self, indent, params):
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
        is_nice = False
        chosen_param_list = []
        if "printf" in cur_func:
            for i in self.final_output:
                if "Ошибка форматной строки" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
        while not is_nice:
            chosen_param_list = []
            for p in gen_n_rands(n, 0, len(params) - 1):
                if is_pointer(params[p][1]) or is_array(params[p][1]):
                    for i in self.final_output:
                        if "Переполнение буфера" in i[0]:
                            i[0] += f"\nСтрока {self.line_number}\n"
                            i[1] += 1
                    is_nice = True
                chosen_param_list.append(params[p][0])
        code = indent + cur_func + ", ".join(chosen_param_list) + ");\n"
        self.line_number += 1
        return code

    # генерирует ошибку встраивания команд
    def c_intr_error(self, indent, params):
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
        chosen_param_list = [params[param][0] for param in gen_n_rands(n, 0, len(params) - 1)]
        code = indent + cur_func + ", ".join(chosen_param_list) + ");\n"
        for i in self.final_output:
            if "Внедрение команд" in i[0]:
                i[0] += f"\nСтрока {self.line_number}\n"
                i[1] += 1
        self.line_number += 1
        return code

    # генерирует ошибку утечки информации
    def data_leak(self, indent, params):
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
            for i in self.final_output:
                if "Утечка информации" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
            self.line_number += 1
            return code
        n = list(cur_func_dict.values())[0]
        chosen_param_list = [params[param][0] for param in gen_n_rands(n, 0, len(params) - 1)]
        code = indent + cur_func + ", ".join(chosen_param_list) + ");\n"
        for i in self.final_output:
            if "Утечка информации" in i[0]:
                i[0] += f"\nСтрока {self.line_number}\n"
                i[1] += 1
        self.line_number += 1
        return code

    def storage_error(self, indent, params):
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
        chosen_param_list = [params[param][0] for param in gen_n_rands(n, 0, len(params) - 1)]
        code = indent + cur_func + ", ".join(chosen_param_list) + ");\n"
        if cur_func == "chmod(":
            for i in self.final_output:
                if "Некорректный доступ к файлам" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
        for i in self.final_output:
            if "Небезопасное хранение данных" in i[0]:
                i[0] += f"\nСтрока {self.line_number}\n"
                i[1] += 1
        self.line_number += 1
        return code

    def file_error(self, indent, params):
        funcs = [
            {"mkdir(": 1},
            {"mktemp(": 1},
            {"rmdir(": 1},
            {"chmod(": 2},
            {"utime(": 2}
            # {"open": 0}
        ]
        cur_func_dict = r_v(funcs)
        cur_func = list(cur_func_dict.keys())[0]
        n = list(cur_func_dict.values())[0]
        # if cur_func == "open":
        #     code = indent + r_v(params)[0] + ".open(\"D://" + r_v(sample_words) + "\");\n"
        #     for i in self.final_output:
        #         if "Некорректный доступ к файлам" in i[0]:
        #             i[0] += f"\nСтрока {self.line_number}\n"
        #             i[1] += 1
        #     self.line_number += 1
        #     return code
        if cur_func == "chmod(":
            for i in self.final_output:
                if "Небезопасное хранение данных" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
        chosen_param_list = [params[param][0] for param in gen_n_rands(n, 0, len(params) - 1)]
        code = indent + cur_func + ", ".join(chosen_param_list) + ");\n"
        for i in self.final_output:
            if "Некорректный доступ к файлам" in i[0]:
                i[0] += f"\nСтрока {self.line_number}\n"
                i[1] += 1
        self.line_number += 1
        return code

    def format_error(self, indent, params):
        is_nice = False
        chosen_param_list = []
        while not is_nice:
            chosen_param_list = []
            for p in gen_n_rands(2, 0, len(params) - 1):
                if is_pointer(params[p][1]) or is_array(params[p][1]):
                    for i in self.final_output:
                        if "Переполнение буфера" in i[0]:
                            i[0] += f"\nСтрока {self.line_number}\n"
                            i[1] += 1
                    is_nice = True
                chosen_param_list.append(params[p][0])
        code = indent + "printf(Format %s and %s, " + ", ".join(chosen_param_list) + ");\n"
        for i in self.final_output:
            if "Ошибка форматной строки" in i[0]:
                i[0] += f"\nСтрока {self.line_number}\n"
                i[1] += 1
        self.line_number += 1
        return code

    def iover_error(self, indent, params):
        chosen_var_list = []
        for _ in range(3):
            chosen_var_list.append(gen_integer_with_value(indent, params))
            self.line_number += 1
        sample_code = ""
        for index in range(1):
            sample_code += r_v(self.iover_generators)(self, indent, params)
        code = "".join(chosen_var_list) + sample_code + indent + chosen_var_list[0].split()[1] + " = " + \
               chosen_var_list[1].split()[1] + \
               " + " + chosen_var_list[2].split()[1] + ";\n"
        for i in self.final_output:
            if "Переполнение целых чисел" in i[0]:
                i[0] += f"\nСтрока {self.line_number}\n"
                i[1] += 1
        self.line_number += 1
        return code

    def free_error(self, indent, params):
        var_type = r_v(constants.types)
        var_name = "var_" + str(rng(1, max_val))
        while var_name in params:
            var_name = "var_" + str(rng(1, max_val))
        code = indent + var_type + " *" + var_name + " = new " + var_type + ";\n"
        params.append((var_name, code))

        for i in self.final_output:
            if "Ошибка высвобождения памяти" in i[0]:
                i[0] += f"\nСтрока {self.line_number}\n"
                i[1] += 1
        self.line_number += 1
        return code

    def race_error(self, indent, params):
        code = ""
        for index in range(rng(2, 5)):
            for i in range(rng(2, 3)):
                code += r_v(self.random_code_generators)(self, indent, params)
            chosen_param_list = [params[param][0] for param in gen_n_rands(3, 0, len(params) - 1)]
            code += indent + "std::thread t" + str(index) + "(" + r_v(self.cur_available_funcs) + ", " + ", ".join(
                chosen_param_list) + ");\n"
            for i in self.final_output:
                if "Состояние гонки" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
            self.line_number += 1
        return code

    def rng_error(self, indent, params):
        funcs = [
            {"srand(": 1},
            {"rand(": 0},
            {"uniform_real_distribution(": 0}
        ]
        cur_func_dict = r_v(funcs)
        cur_func = list(cur_func_dict.keys())[0]
        if cur_func == "uniform_real_distribution(":
            code = indent + "std::uniform_real_distribution<> dis(" + str(rng(1, 3)) + ", " + str(rng(1, 9)) + ");\n"
            for i in self.final_output:
                if "Случайные числа криптографического характера" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
            self.line_number += 1
            return code
        if cur_func == "srand(":
            code = indent + cur_func + str(rng(3, 100)) + ");\n"
            for i in self.final_output:
                if "Случайные числа криптографического характера" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
            self.line_number += 1
            return code
        else:
            code = indent + cur_func + ");\n"
            for i in self.final_output:
                if "Случайные числа криптографического характера" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
            self.line_number += 1
            return code

    def readers_error(self, indent, params):
        code = ""
        for index in range(rng(2, 5)):
            for i in range(rng(2, 3)):
                code += r_v(self.random_code_generators)(self, indent, params)
            chosen_param_list = [params[param][0] for param in gen_n_rands(4, 0, len(params) - 1)]
            code += indent + "std::thread t" + str(index) + "(" + r_v(self.cur_available_funcs) + ", " + ", ".join(
                chosen_param_list) + ");\n"
            for i in self.final_output:
                if "Читатели Писатели" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
            self.line_number += 1
        return code

    def sql_error(self, indent, params):
        funcs = ["execute(", "executeQuery("]
        cur_func = r_v(funcs)
        sample_text = ""
        for _ in range(3):
            sample_text += r_v(sample_words) + "'"
        random = rng(0, 1)
        if random == 0:
            code = indent + cur_func + "\"" + sample_text + "\");\n"
        else:
            code = indent + cur_func + r_v(params)[0] + ");\n"
        for i in self.final_output:
            if "SQL инъекции" in i[0]:
                i[0] += f"\nСтрока {self.line_number}\n"
                i[1] += 1
        self.line_number += 1
        return code

    def gen_sample_function(self, vulnerabilities, file):
        indent = "\t"
        # Генерация сигнатуры функции
        func_type = r_v(func_types)
        func_name = "function_" + str(rng(0, 20))
        generated_vars = []
        func_params = []
        for index in range(rng(1, 4)):
            func_params.append(r_v(p_funcs)(indent, generated_vars))
        file.write(func_type + " " + func_name + "(" + ", ".join([param[1:-2] for param in func_params]) + ") {\n")
        self.line_number += 1
        # Генерация переменных
        if "Читатели Писатели" in vulnerabilities:
            mutex = r_v(self.mutexes)
            if rng(0, 1) == 1:
                file.write("\t" + mutex + ".lock();\n")
                self.line_number += 1
        if "Переполнение буфера" in vulnerabilities:
            file.write(gen_buffer(indent, generated_vars))
            self.line_number += 1
        for index in range(rng(6, 7)):
            code = r_v(v_funcs)(indent, generated_vars)
            file.write(code)
            self.line_number += 1
        # Генерация произвольного кода
        for index in range(rng(1, 2)):
            file.write(r_v(self.random_code_generators)(self, indent, generated_vars))

        # Конец функции
        file.write("}\n")
        self.line_number += 1
        return func_name

    def gen_function(self, vuln_generators, file):
        indent = "\t"
        func_type = "int"
        func_name = "main"
        generated_vars = []
        func_params = []
        for index in range(rng(1, 4)):
            func_params.append(r_v(p_funcs)(indent, generated_vars))
        file.write(func_type + " " + func_name + "(" + ", ".join([param[1:-2] for param in func_params]) + ") {\n")
        self.line_number += 1
        for index in range(rng(6, 7)):
            code = r_v(v_funcs)(indent, generated_vars)
            file.write(code)
            self.line_number += 1
        for generator in vuln_generators:
            for index in range(rng(2, 3)):
                #file.write(r_v(self.random_code_generators)(self, indent, generated_vars))
                file.write(generator(self, indent, generated_vars))
        file.write("}\n")
        self.line_number += 1
        return func_name

    def gen_code(self, vulnerabilities: List[str], test_numbers):
        folder = "../generated_tests"
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        for index in range(test_numbers):
            self.line_number = 1
            file = open('../generated_tests/' + "+".join(vulnerabilities)[0] + str(index + 1) + '.cpp', 'w')
            generators = []
            for vuln in vulnerabilities:
                generators.append(self.name_generator[vuln])
            if "Читатели Писатели" in vulnerabilities:
                mutex_cnt = rng(1, 3)
                for i in range(mutex_cnt):
                    mutex_name = "testMutex" + str(r_v(gen_n_rands(mutex_cnt, 0, 10)))
                    file.write("mutex " + mutex_name + ";\n")
                    self.line_number += 1
                    self.mutexes.append(mutex_name)
            for i in range(rng(1, 3)):
                self.cur_available_funcs.append(self.gen_sample_function(vulnerabilities, file))
            self.gen_function(generators, file)
            self.cur_available_funcs = []
            file.write(str(self.line_number))
            file.close()
            # review_file = open('../generated_tests/' + "+".join(vulnerabilities)[0] + str(index + 1) + 'обзор.cpp', 'w',
            #                    encoding="utf-8")
            # review_file.write("Сгенерированные и найденные ошибки:\n\n")
            # for vulnerability in vulnerabilities:
            #     for key, value in self.final_output:
            #         if vulnerability in key:
            #             review_file.write("Сгенерированные:\n")
            #             review_file.write(key + ": " + str(value) + "\n")
            # review_file.write("\nНайденные:\n")
            # for vulnerability in vulnerabilities:
            #     to_write = main.handlers_list[vulnerability]().parse((find_contexts(
            #         clean_code('../generated_tests/' + "+".join(vulnerabilities) + str(index + 1) + '.cpp'))))[
            #                    -1] + "\n"
            #     review_file.write(to_write)
            for vulnerability in vulnerabilities:
                to_write = main.handlers_list[vulnerability]().parse((find_contexts(
                    clean_code('../generated_tests/' + "+".join(vulnerabilities)[0] + str(index + 1) + '.cpp'))))[
                               -1] + "\n"
                m = re.search(r'(\d+)', to_write)
                tmp_cnt = int(m.group(1))
                for i in self.final_output_for_test:
                    if vulnerability in i[0]:
                        i[1] += tmp_cnt
        stat_file = open('общая_статистика.cpp', 'w',
                               encoding="utf-8")
        stat_file.write("Статистика сгенерированных уязвимостей:\n")
        for vulnerability in vulnerabilities:
            cur_vuln_cnt = 0
            for key, value in self.final_output:
                if vulnerability in key:
                    cur_vuln_cnt += value
            stat_file.write(vulnerability + ": " + str(cur_vuln_cnt) + "\n")

        stat_file.write("\nСтатистика найденных уязвимостей:\n")
        for vulnerability in vulnerabilities:
            for key, value in self.final_output_for_test:
                if vulnerability in key:
                    stat_file.write(vulnerability + ": " + str(value) + "\n")

    random_code_generators = [gen_cond, gen_try_catch, buff_error, c_intr_error, data_leak, storage_error,
                              file_error, format_error, iover_error, free_error, rng_error, sql_error]

    catch_generators = [gen_cond, buff_error, c_intr_error, data_leak, storage_error,
                        file_error, format_error, iover_error, free_error, rng_error, sql_error]

    cond_generators = [gen_try_catch, buff_error, c_intr_error, data_leak, storage_error,
                       file_error, format_error, iover_error, free_error, rng_error, sql_error]

    iover_generators = [gen_cond, gen_try_catch, buff_error, c_intr_error, data_leak, storage_error,
                        file_error, format_error, free_error, rng_error, sql_error]

    name_generator = {
        "Переполнение буфера": buff_error,
        "Внедрение команд": c_intr_error,
        "Утечка информации": data_leak,
        "Небезопасное хранение данных": storage_error,
        "Пренебрежение обработкой исключений": gen_try_catch,
        "Некорректный доступ к файлам": file_error,
        "Ошибка форматной строки": format_error,
        "Переполнение целых чисел": iover_error,
        "Ошибка высвобождения памяти": free_error,
        "Состояние гонки": race_error,
        "Случайные числа криптографического характера": rng_error,
        "Читатели Писатели": readers_error,
        "SQL инъекции": sql_error
    }


if __name__ == '__main__':
    gen = CodeGenerator()
    gen.gen_code(["Переполнение буфера", "Внедрение команд", "Утечка информации", "Небезопасное хранение данных",
                  "Пренебрежение обработкой исключений"], 1)
