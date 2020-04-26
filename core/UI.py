#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
from os.path import basename
from queue import Queue, Empty
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames
from core.create_utils import *
from core.multithreading import create_workers, create_jobs
from core.select_utils import *

FONT = ("Helvetica", 12)
BUTTON_WIDTH = 13
BUTTON_HEIGHT = 1
MAIN_COLOR = "white"


def fill_listbox(listbox: Listbox, items: tuple or list):
    for item in items:
        listbox.insert(END, item)


def write_to_text(text_field: Text, text: str or list or tuple, option: str = NONE):
    text_field.configure(state=NORMAL)
    if option == 'CLEAR':
        text_field.delete('1.0', END)
    if isinstance(text, (list, tuple)):
        for line in text:
            text_field.insert(END, str(line) + '\n')
    else:
        text_field.insert(END, text)
    text_field.configure(state=DISABLED)


class Form(object):
    def __init__(self, title: str, geometry: str, font: (str, int)):
        self.root = Tk()
        self.root.iconbitmap(os.getcwd() + "\\resources\\icon.ico")
        self.root.configure(bg=MAIN_COLOR)
        self.root.update()
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.resizable(width=True, height=True)
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        self.root.protocol('WM_DELETE_WINDOW', self.exit)
        self.font = font

    def error(self, message):
        self.root.withdraw()
        messagebox.showerror("Error", message)

    def start(self):
        try:
            self.root.mainloop()
        except Exception as e:
            self.error(e.args)

    def exit(self):
        try:
            self.root.destroy()
        except Exception as e:
            self.error(e.args)


def restart_program():
    executable = sys.executable
    os.execl(executable, executable, *sys.argv)


def find_vulnerabilities(programs: tuple or list, vulnerabilities: tuple or list, handler):
    """
    :param programs: список путей к файлам, которые будут анализироваться
    :param vulnerabilities: список выбранных уязвимостей, которые будут искаться \
    (их названия согласно декларации в классе)
    :param handler: лямба функция, которая объявлена в main.py при вызове start_main
    :return:
    """

    def get_vuln_out(cur_p):
        vuln_out = []
        for vulnerability in vulnerabilities:
            if handler(vulnerability, cur_p):
                vuln_out.append((vulnerability, handler(vulnerability, cur_p)))
        return dict(vuln_out)

    if not (programs and vulnerabilities):
        return 0
    try:
        queue = Queue()
        create_workers(len(programs), show_vulns, queue)
        job_args = []
        for program in programs:
            if get_vuln_out(program):
                job_args.append((program, get_vuln_out(program), open(program, 'r').read().splitlines()))
        create_jobs(job_args, queue)
    except Empty:
        from tkinter import messagebox
        messagebox.showinfo("Информация!", "Уязвимости не были обнаружены!")


def show_vulns(queue):
    def get_rank(var):
        count = 1
        var //= 10
        while var > 0:
            var //= 10
            count += 1
        return count

    v_form = None
    try:
        program, content, program_code = queue.get(block=True)
        queue.task_done()

        v_form = Form(program + ' - анализ', '1100x700+410+180', FONT)

        code_frame = Frame(v_form.root, bg=MAIN_COLOR, width=1100, height=400, borderwidth=2)
        vuln_frame = Frame(v_form.root,
                           relief="ridge", bg=MAIN_COLOR, width=300, height=270)
        loc_frame = Frame(v_form.root,
                          relief="ridge", bg=MAIN_COLOR, width=1100, height=270)

        code_lbl = Label(code_frame, text='Исходный код:', font=v_form.font, anchor='w', bg=MAIN_COLOR)
        loc_lbl = Label(loc_frame, text='Местоположение:', font=v_form.font, anchor='w', bg=MAIN_COLOR)
        v_lbl = Label(vuln_frame, text='Найденные уязвимости:', font=v_form.font, width=28,
                      anchor='w', bg=MAIN_COLOR)

        code_extra_frame = Frame(code_frame, bg=MAIN_COLOR)
        code_lb = create_code_listbox(code_extra_frame, EXTENDED, 1, font=("Helvetica", 11), bg="#EEEDF1")
        create_scroll_box(code_extra_frame, code_lb, VERTICAL)

        pr_len = len(program)
        max_rank = get_rank(pr_len)
        tmp_list = []
        for index, line in enumerate(program_code):
            cur_rank = get_rank(index + 1)
            cur_indent = 2 + (max_rank - cur_rank) * 2
            tmp_list.append(f"{index + 1}" + ' ' * cur_indent + "|  " + line.replace("\t", "   "))
        fill_listbox(code_lb, tmp_list)

        code_extra_frame.grid(row=1, column=0, columnspan=2, sticky=E, padx=10, pady=10)
        code_lbl.grid(row=0, column=0, sticky=NW, padx=10, pady=(5, 0))

        loc_extra_frame = Frame(loc_frame, bg=MAIN_COLOR)
        where_tb = Text(loc_extra_frame, borderwidth=1, width=80, height=15, relief="groove", wrap=WORD,
                        state='disabled', font=FONT, bg="#EEEDF1")
        create_scroll_box(loc_extra_frame, where_tb, VERTICAL)
        loc_lbl.grid(row=0, column=0, sticky=NW, padx=10, pady=(5, 0))
        loc_extra_frame.grid(row=1, column=0, sticky=EW, padx=10)

        code_frame.grid_propagate(0)
        vuln_frame.grid_propagate(0)
        loc_frame.grid_propagate(0)

        found_lb = Listbox(vuln_frame, font=FONT, width=70, height=40, selectmode=SINGLE, exportselection=False, bg="#EEEDF1", borderwidth=1)
        found_lb.bind('<<ListboxSelect>>', lambda event: write_to_text(where_tb,
                                                                       content[
                                                                           found_lb.get(
                                                                               found_lb.curselection())],
                                                                       'CLEAR'))

        fill_listbox(found_lb, content.keys())

        v_lbl.grid(row=0, column=0, sticky=W)
        found_lb.grid(row=1, column=0, sticky=EW)

        code_frame.grid(row=0, column=0, columnspan=2, sticky=EW, pady=(0, 10))
        vuln_frame.grid(row=1, column=0, pady=(0, 5), padx=(10, 0), sticky=W)
        loc_frame.grid(row=1, column=1, pady=(0, 5), sticky=W)

        v_form.start()
    except Exception as e:
        from tkinter import messagebox
        v_form.error(e.args)
        v_form.exit()


def upload_chosen_p():
    """
    Возвращает список путей к выбранным программам
    :return: List[path_to_file]
    """
    programs = []
    try:
        programs = list(askopenfilenames(title='Открыть программы для анализа', initialdir=os.getcwd(),
                                         filetypes=[("CPP", ".cpp")]))
    except IOError:
        messagebox.showwarning("Предупреждение", "Папка \"tests\" не существует")
    return programs


def upload_default_t():
    """
    Возвращает список путей к стандартным тестам
    :return: List[path_to_file]
    """
    tests = []
    try:
        tests = [os.getcwd() + '/tests/' + file for file in os.listdir(os.getcwd() + '/tests') if
                 file.endswith(".cpp")]
    except IOError:
        from tkinter import messagebox
        messagebox.showwarning("Предупреждение", "Директория \"tests\" не существует")
    except Exception as e:
        from tkinter import messagebox
        messagebox.showwarning("Предупреждение", e.args)
    return tests


class UI(object):

    def __init__(self, vulnerability_names):
        self.vulnerability_names = vulnerability_names
        self.default_tests = upload_default_t()
        self.chosen_programs = []

    def fill_programs_list(self, list_box: Listbox):
        self.chosen_programs = upload_chosen_p()
        fill_listbox(list_box, [basename(file) for file in self.chosen_programs])

    def start_main(self, handler):
        main_form = None
        try:
            main_form = Form('', '1110x500+400+200', FONT)
            main_form.root.focus_force()

            main_menu = Menu()
            file_menu = Menu(tearoff=0)
            file_menu.add_command(label="Открыть", command=lambda: self.fill_programs_list(programs_listb))
            file_menu.add_command(label="Перезапуск", command=lambda: restart_program())
            file_menu.add_command(label="Выход", command=lambda: main_form.root.quit())
            main_menu.add_cascade(label="Файл", menu=file_menu)
            main_form.root.config(menu=main_menu)

            v_frame = Frame(main_form.root, borderwidth=2, relief="groove", bg="#BDDDC2", width=300, height=390)

            t_frame = LabelFrame(main_form.root, font=("Helvetica", 11), text="Стандартные тесты", borderwidth=3,
                                 relief="groove", bg="#EEEDF1", width=340, height=390)
            p_frame = LabelFrame(main_form.root, font=("Helvetica", 11), text="Программы", borderwidth=3,
                                 relief="groove", bg="#EEEDF1", width=340, height=390)
            b_frame1 = Frame(t_frame, pady=7, bg="#EEEDF1")
            b_frame2 = Frame(p_frame, pady=7, bg="#EEEDF1")

            tests_listb = create_listbox(t_frame, EXTENDED, 0)
            programs_listb = create_listbox(p_frame, EXTENDED, 0)

            create_scroll_box(t_frame, tests_listb, VERTICAL)
            create_scroll_box(p_frame, programs_listb, VERTICAL)

            v_to_check = [create_check_button(v_frame, bg="#BDDDC2", text=vulnerability, height=1, width=30, anchor=W)
                          for vulnerability in self.vulnerability_names]

            l1 = lambda: find_vulnerabilities(
                [os.getcwd() + '/tests/' + file for file in get_selected_t(tests_listb)],
                get_selected_v(v_to_check), handler)
            l2 = lambda: find_vulnerabilities(self.default_tests, get_selected_v(v_to_check), handler)
            l3 = lambda: find_vulnerabilities(get_selected_p(self.chosen_programs, programs_listb),
                                              get_selected_v(v_to_check), handler)
            l4 = lambda: find_vulnerabilities(self.chosen_programs, get_selected_v(v_to_check), handler)

            check1 = create_button(b_frame1, "Проверить", self, l1)
            check2 = create_button(b_frame2, "Проверить", self, l3)
            check_all1 = create_button(t_frame, "Проверить все", self, l2)
            check_all2 = create_button(p_frame, "Проверить все", self, l4)

            version_lbl = Label(main_form.root, text='Версия: 1.0.0', font=FONT, anchor='w', bg=MAIN_COLOR)

            v_frame.grid(row=0, column=0, padx=(40, 0), pady=(40, 0), sticky=N)
            t_frame.grid(row=0, column=1, padx=(50, 20), pady=(40, 0), sticky=N)
            p_frame.grid(row=0, column=2, pady=(40, 0), sticky=N)
            version_lbl.grid(row=1, column=2, pady=(30, 0), sticky=SE)

            check_all1.pack(side=TOP)
            check1.pack(side=TOP)
            check_all2.pack(side=TOP)
            check2.pack(side=TOP)

            b_frame1.pack()
            b_frame2.pack()

            v_frame.pack_propagate(0)
            t_frame.pack_propagate(0)
            p_frame.pack_propagate(0)

            fill_listbox(tests_listb, [basename(file) for file in self.default_tests])

            main_form.start()
        except Exception as e:
            from tkinter import messagebox
            main_form.error(e.args)
            main_form.exit()
