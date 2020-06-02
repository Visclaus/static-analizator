import copy
import os
import re
import main
from code_generator.var_genetor import *
from core.main_code_parser import find_contexts
from core.variable import is_pointer, is_array
from utils.constants import *
from utils.initial_parse import clean_code

vars_generators = [gen_var, gen_var_with_value, gen_buffer, gen_pointer]
params_generators = [gen_var, gen_pointer]


def pre_clean(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


class CodeGenerator:
    tests_count = 1
    generation_folder = "../generated_tests/"
    cur_test_funcs = []
    mutexes = []
    max_mutex_cnt = 4
    max_func_cnt = 2
    max_func_params_cnt = 4
    tests_lines_cnt = []
    default_indent = '\t'
    line_number = 1
    cur_condition_level = 1
    cur_tc_level = 1
    max_level = 1

    def generate_condition(self, indent, params):
        code = ""
        if self.cur_condition_level > 0:
            self.cur_condition_level -= 1
            declaration = indent + "if(" + rand_value(params)[0] + " " + rand_value(cond) + " " + str(
                rng(0, 500)) + ") {\n"
            self.line_number += 1
            body = ""
            for index in range(5):
                body += rand_value(self.random_code_generators)(self, self.default_indent + indent, params)
            code = declaration + body + indent + "}\n"
            self.line_number += 1
        else: self.random_code_generators = self.random_code_generators_no_rec
        return code

    def generate_try_catch(self, indent, params):
        code = ""
        if self.cur_tc_level > 0:
            self.cur_tc_level -= 1
            try_declaration = indent + "try {\n"
            self.line_number += 1
            try_body = ""
            for index in range(2):
                try_body += rand_value(self.random_code_generators)(self, self.default_indent + indent, params)
            catch_declaration = indent + "catch (Exception_" + str(rng(1, 20)) + " err) {\n"
            self.line_number += 1

            catch_body = ""
            if rng(0, 1) == 1:
                for index in range(2):
                    catch_body += rand_value(self.random_code_generators)(self, self.default_indent + indent, params)
            else:
                catch_body = "\n"
                self.line_number += 1

                for vuln_name in self.gen_report_map:
                    if "Пренебрежение обработкой исключений" in vuln_name[0]:
                        vuln_name[0] += f"\nСтрока {self.line_number}\n"
                        vuln_name[1] += 1

            code = try_declaration + try_body + indent + "}\n" + catch_declaration + catch_body + indent + "}\n"
            self.line_number += 2
        else:
            self.random_code_generators = self.random_code_generators_no_rec
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
        cur_func_dict = rand_value(funcs)
        cur_func = list(cur_func_dict.keys())[0]
        n = list(cur_func_dict.values())[0]
        is_nice = False
        chosen_param_list = []
        if "printf" in cur_func:
            for i in self.gen_report_map:
                if "Ошибка форматной строки" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
        while not is_nice:
            chosen_param_list = []
            for p in gen_n_rands(n, 0, len(params) - 1):
                if is_pointer(params[p][1]) or is_array(params[p][1]):
                    for i in self.gen_report_map:
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
        cur_func_dict = rand_value(funcs)
        cur_func = list(cur_func_dict.keys())[0]
        n = list(cur_func_dict.values())[0]
        chosen_param_list = [params[param][0] for param in gen_n_rands(n, 0, len(params) - 1)]
        code = indent + cur_func + ", ".join(chosen_param_list) + ");\n"
        for i in self.gen_report_map:
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
        cur_func_dict = rand_value(funcs)
        cur_func = list(cur_func_dict.keys())[0]
        if cur_func == "errno":
            code = indent + "cout<<" + cur_func + ";\n"
            for i in self.gen_report_map:
                if "Утечка информации" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
            self.line_number += 1
            return code
        n = list(cur_func_dict.values())[0]
        chosen_param_list = [params[param][0] for param in gen_n_rands(n, 0, len(params) - 1)]
        code = indent + cur_func + ", ".join(chosen_param_list) + ");\n"
        for i in self.gen_report_map:
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
        cur_func_dict = rand_value(funcs)
        cur_func = list(cur_func_dict.keys())[0]
        n = list(cur_func_dict.values())[0]
        chosen_param_list = [params[param][0] for param in gen_n_rands(n, 0, len(params) - 1)]
        code = indent + cur_func + ", ".join(chosen_param_list) + ");\n"
        if cur_func == "chmod(":
            for i in self.gen_report_map:
                if "Некорректный доступ к файлам" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
        for i in self.gen_report_map:
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
        cur_func_dict = rand_value(funcs)
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
            for i in self.gen_report_map:
                if "Небезопасное хранение данных" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
        chosen_param_list = [params[param][0] for param in gen_n_rands(n, 0, len(params) - 1)]
        code = indent + cur_func + ", ".join(chosen_param_list) + ");\n"
        for i in self.gen_report_map:
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
                    for i in self.gen_report_map:
                        if "Переполнение буфера" in i[0]:
                            i[0] += f"\nСтрока {self.line_number}\n"
                            i[1] += 1
                    is_nice = True
                chosen_param_list.append(params[p][0])
        code = indent + "printf(Format %s and %s, " + ", ".join(chosen_param_list) + ");\n"
        for i in self.gen_report_map:
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
            sample_code += rand_value(self.iover_generators)(self, indent, params)
        code = "".join(chosen_var_list) + sample_code + indent + chosen_var_list[0].split()[1] + " = " + \
               chosen_var_list[1].split()[1] + \
               " + " + chosen_var_list[2].split()[1] + ";\n"
        for i in self.gen_report_map:
            if "Переполнение целых чисел" in i[0]:
                i[0] += f"\nСтрока {self.line_number}\n"
                i[1] += 1
        self.line_number += 1
        return code

    def free_error(self, indent, params):
        var_type = rand_value(constants.types)
        var_name = "var_" + str(rng(1, 2000))
        while var_name in params:
            var_name = "var_" + str(rng(1, max_val))
        code = indent + var_type + " *" + var_name + " = new " + var_type + ";\n"
        params.append((var_name, code))

        for i in self.gen_report_map:
            if "Ошибка высвобождения памяти" in i[0]:
                i[0] += f"\nСтрока {self.line_number}\n"
                i[1] += 1
        self.line_number += 1
        return code

    def race_error(self, indent, params):
        code = ""
        for index in range(rng(2, 5)):
            for i in range(rng(2, 3)):
                code += rand_value(self.random_code_generators)(self, indent, params)
            chosen_param_list = [params[param][0] for param in gen_n_rands(3, 0, len(params) - 1)]
            code += indent + "std::thread t" + str(index) + "(" + rand_value(self.cur_test_funcs) + ", " + ", ".join(
                chosen_param_list) + ");\n"
            for i in self.gen_report_map:
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
        cur_func_dict = rand_value(funcs)
        cur_func = list(cur_func_dict.keys())[0]
        if cur_func == "uniform_real_distribution(":
            code = indent + "std::uniform_real_distribution<> dis(" + str(rng(1, 3)) + ", " + str(rng(1, 9)) + ");\n"
            for i in self.gen_report_map:
                if "Случайные числа криптографического характера" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
            self.line_number += 1
            return code
        if cur_func == "srand(":
            code = indent + cur_func + str(rng(3, 100)) + ");\n"
            for i in self.gen_report_map:
                if "Случайные числа криптографического характера" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
            self.line_number += 1
            return code
        else:
            code = indent + cur_func + ");\n"
            for i in self.gen_report_map:
                if "Случайные числа криптографического характера" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
            self.line_number += 1
            return code

    def readers_error(self, indent, params):
        code = ""
        params_1 = [(param[0], param[1].replace("\t", "")) for param in params]
        for index in range(rng(2, 5)):
            for i in range(rng(2, 3)):
                code += rand_value(self.random_code_generators)(self, indent, params)
            chosen_param_list = [params_1[param][0] for param in gen_n_rands(4, 0, len(params_1) - 1)]
            code += indent + "std::thread t" + str(index) + "(" + rand_value(self.cur_test_funcs) + ', ' + ", ".join(
                chosen_param_list) + ");\n"
            for i in self.gen_report_map:
                if "Читатели Писатели" in i[0]:
                    i[0] += f"\nСтрока {self.line_number}\n"
                    i[1] += 1
            self.line_number += 1
        return code

    def sql_error(self, indent, params):
        funcs = ["execute(", "executeQuery("]
        cur_func = rand_value(funcs)
        sample_text = ""
        for _ in range(3):
            sample_text += rand_value(sample_words) + "'"
        random = rng(0, 1)
        if random == 0:
            code = indent + cur_func + "\"" + sample_text + "\");\n"
        else:
            code = indent + cur_func + rand_value(params)[0] + ");\n"
        for i in self.gen_report_map:
            if "SQL инъекции" in i[0]:
                i[0] += f"\nСтрока {self.line_number}\n"
                i[1] += 1
        self.line_number += 1
        return code

    def generate_variables(self, file, generated_vars, min_range=6, max_range=7):
        for index in range(rng(min_range, max_range)):
            code = rand_value(vars_generators)(self.default_indent, generated_vars)
            file.write(code)
            self.line_number += 1

    def generate_mutex_usage(self, file):
        chosen_mutex = rand_value(self.mutexes)
        if rng(0, 1) == 1:
            file.write("\t" + chosen_mutex + ".lock();\n")
            self.line_number += 1

    def generate_random_code(self, file, generated_vars, cnt=3):
        for index in range(rng(1, cnt)):
            file.write(rand_value(self.random_code_generators)(self, self.default_indent, generated_vars))

    def generate_func_params(self, generated_vars):
        for _ in range(rng(1, self.max_func_params_cnt)):
            rand_value(params_generators)(self.default_indent, generated_vars)

    def gen_function(self, vulnerabilities, file):
        self.cur_condition_level = self.max_level
        self.cur_tc_level = self.max_level
        self.random_code_generators = self.random_code_generators_rec
        generated_vars = []
        func_type = rand_value(func_types)
        func_name = "function_" + str(rng(0, 20))
        self.generate_func_params(generated_vars)
        file.write(
            func_type + " " + func_name + "(" + ", ".join([param[1][1:-2] for param in generated_vars]) + ") {\n")
        if '12' in vulnerabilities:
            self.generate_mutex_usage(file)
        self.generate_variables(file, generated_vars)
        self.generate_random_code(file, generated_vars)
        file.write("}\n")
        self.line_number += 2
        return func_name

    def gen_vuln_function(self, vuln_generators, file):
        self.cur_condition_level = self.max_level
        self.cur_tc_level = self.max_level
        self.random_code_generators = self.random_code_generators_rec
        generated_vars = []
        self.generate_func_params(generated_vars)
        file.write("int main(" + ", ".join([param[1][1:-2] for param in generated_vars]) + ") {\n")
        self.generate_variables(file, generated_vars)
        for vuln_generator in vuln_generators:
            for _ in range(rng(1, 3)):
                file.write(rand_value(self.random_code_generators)(self, self.default_indent, generated_vars))
            file.write(vuln_generator(self, self.default_indent, generated_vars))
        file.write("}\n")
        self.line_number += 2

    def declare_mutexes(self, file):
        mutex_cnt = rng(1, self.max_mutex_cnt)
        mutex_index_list = gen_n_rands(mutex_cnt, 0, 10)
        for index in mutex_index_list:
            mutex_name = "testMutex" + str(index)
            file.write("mutex " + mutex_name + ";\n")
            self.line_number += 1
            self.mutexes.append(mutex_name)
        file.write('\n')
        self.line_number += 1

    def gen_code(self, vulnerabilities, tests_count):
        self.tests_count = tests_count
        pre_clean(self.generation_folder)
        generators = [self.generator_map[i] for i in vulnerabilities]
        for test_index in range(self.tests_count):
            self.line_number = 1
            self.cur_test_funcs = []
            generated_test_file = open(self.generation_folder + str(test_index + 1) + '.cpp', 'w')

            if '12' in vulnerabilities:
                self.declare_mutexes(generated_test_file)

            for _ in range(rng(1, self.max_func_cnt)):
                self.cur_test_funcs.append(self.gen_function(vulnerabilities, generated_test_file))

            self.gen_vuln_function(generators, generated_test_file)
            self.tests_lines_cnt.append(self.line_number)
            generated_test_file.close()

    def check_generated_code(self, vulnerabilities):
        statistic_file = open('common_report.cpp', 'w', encoding="utf-8")
        statistic_file.write("{0}ОТЧЕТ{0}\n".format('-' * 10))
        statistic_file.write("Количество сгенерированных тестов: {0}\n".format(self.tests_count))

        for test_index in range(self.tests_count):
            for vulnerability in vulnerabilities:
                handler = main.handlers_list[self.tester_map[vulnerability]]()
                code = clean_code(self.generation_folder + str(test_index + 1) + '.cpp')
                output = handler.parse((find_contexts(code)))

                handler_info = output[-1] + "\n"
                match = re.search(r'(\d+)', handler_info)
                cur_found_vuln_cnt = int(match.group(1))

                for index in self.found_report_map:
                    if self.tester_map[vulnerability] in index[0]:
                        index[1] += cur_found_vuln_cnt

        statistic_file.write("Статистика сгенерированных уязвимостей:\n")
        total_gen_cnt = 0
        for vulnerability in vulnerabilities:
            cur_gen_vuln_cnt = 0
            cur_vuln_name = self.tester_map[vulnerability]
            for key, value in self.gen_report_map:
                if cur_vuln_name in key:
                    cur_gen_vuln_cnt += value
            statistic_file.write(cur_vuln_name + ": " + str(cur_gen_vuln_cnt) + "\n")
            total_gen_cnt += cur_gen_vuln_cnt
        statistic_file.write("Всего: {0}\n".format(total_gen_cnt))

        statistic_file.write("\nСтатистика найденных уязвимостей:\n")
        total_found_cnt = 0
        for vulnerability in vulnerabilities:
            cur_vuln_name = self.tester_map[vulnerability]
            for key, value in self.found_report_map:
                if cur_vuln_name in key:
                    statistic_file.write(cur_vuln_name + ": " + str(value) + "\n")
                    total_found_cnt += value
        statistic_file.write("Всего: {0}\n".format(total_found_cnt))
        statistic_file.write(
            "\nНайдено: {0} % сгенерированных ошибок".format(str(total_found_cnt * 100 / total_gen_cnt)))

    generator_map = {
        '1': buff_error,
        '2': c_intr_error,
        '3': data_leak,
        '4': storage_error,
        '5': generate_try_catch,
        '6': file_error,
        '7': format_error,
        '8': iover_error,
        '9': free_error,
        '10': race_error,
        '11': rng_error,
        '12': readers_error,
        '13': sql_error
    }

    tester_map = {
        '1': "Переполнение буфера",
        '2': "Внедрение команд",
        '3': "Утечка информации",
        '4': "Небезопасное хранение данных",
        '5': "Пренебрежение обработкой исключений",
        '6': "Некорректный доступ к файлам",
        '7': "Ошибка форматной строки",
        '8': "Переполнение целых чисел",
        '9': "Ошибка высвобождения памяти",
        '10': "Состояние гонки",
        '11': "Случайные числа криптографического характера",
        '12': "Читатели Писатели",
        '13': "SQL инъекции"
    }

    gen_report_map = [["Переполнение буфера", 0], ["Внедрение команд", 0], ["Утечка информации", 0],
                      ["Небезопасное хранение данных", 0], ["Пренебрежение обработкой исключений", 0],
                      ["Некорректный доступ к файлам", 0], ["Ошибка форматной строки", 0],
                      ["Переполнение целых чисел", 0],
                      ["Ошибка высвобождения памяти", 0], ["Состояние гонки", 0],
                      ["Случайные числа криптографического характера", 0], ["Читатели Писатели", 0],
                      ["SQL инъекции", 0]]

    found_report_map = copy.deepcopy(gen_report_map)

    random_code_generators = [generate_try_catch, buff_error, c_intr_error, data_leak,
                              storage_error,
                              file_error, format_error, iover_error, free_error, rng_error, sql_error]

    random_code_generators_rec = [generate_condition, generate_try_catch, buff_error, c_intr_error, data_leak,
                                  storage_error,
                                  file_error, format_error, iover_error, free_error, rng_error, sql_error]

    random_code_generators_no_rec = [buff_error, c_intr_error, data_leak, storage_error,
                                     file_error, format_error, iover_error, free_error, rng_error, sql_error]

    iover_generators = [generate_condition, generate_try_catch, buff_error, c_intr_error, data_leak, storage_error,
                        file_error, format_error, free_error, rng_error, sql_error]


if __name__ == '__main__':
    # """
    #
    # Здесь происходит генерация тестового кода, ниже задан список соответсвия узявимости к ее номеру.
    #
    # 1. Переполнение буфера
    # 2. Внедрение команд
    # 3. Утечка информации
    # 4. Небезопасное хранение данных
    # 5. Пренебрежение обработкой исключений
    # 6. Некорректный доступ к файлам
    # 7. Ошибка форматной строки
    # 8. Переполнение целых чисел
    # 9. Ошибка высвобождения памяти
    # 10. Состояние гонки
    # 11. Случайные числа криптографического характера
    # 12. Читатели Писатели
    # 13. SQL инъекции
    #
    # """
    #
    # generator = CodeGenerator()
    # print('Какие уязвимости сгенерировать?(при нескольких значениях перечислить через запятую)\n')
    # task_for_generation = input().split(',')
    # if task_for_generation[0] == '-1':
    #     task_for_generation = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
    # print("Выбранные уязвимости:")
    # for index, task in enumerate(task_for_generation):
    #     print(f"{index + 1}) {generator.tester_map[task]}:")
    # print('Сколько тестов сгенерировать?\n')
    # tests_cnt = int(input())
    # generator.gen_code(task_for_generation, tests_cnt)
    # generator.check_generated_code(task_for_generation)
    # func_params = []
    generator = CodeGenerator()
    generator.cur_test_funcs = ['function_1', 'function_2']
    func_params = []
    for index in range(rng(20, 30)):
        rand_value(vars_generators)('\t', func_params)
    for _ in range(5):
        print(generator.iover_error('\t', func_params))
