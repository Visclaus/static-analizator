#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import _tkinter
import os
from os.path import basename
from tkinter import *
from tkinter import Menu, messagebox
from tkinter.filedialog import askopenfilenames

from PIL import Image, ImageTk

FONT = ('Source Code Pro', 12)
BUTTON_WIDTH = 10
BUTTON_HEIGHT = 1


def create_check_button(parent: Frame, text: str, height: int, width: int, anchor, value: int = 0):
    value = IntVar(value=value)
    ch_button = Checkbutton(parent, variable=value, text=text, height=height, width=width, anchor=anchor)
    ch_button.pack()
    return value, ch_button


def create_listbox(parent: Widget, select_mode, border_width: int, action=None):
    listbox = Listbox(parent, width=30, selectmode=select_mode, exportselection=False, borderwidth=border_width)
    listbox.pack(fill=BOTH, expand=TRUE)
    listbox.bind('<<ListboxSelect>>', action)
    return listbox


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


def create_scroll_box(frame, item, orient=HORIZONTAL):
    scrollbar = Scrollbar(frame, orient=orient)
    scrollbar.config(command=item.xview if orient == HORIZONTAL else item.yview)
    scrollbar.pack(side=BOTTOM if orient == HORIZONTAL else RIGHT, fill=X if orient == HORIZONTAL else Y)
    item.config(xscrollcommand=scrollbar.set if orient == HORIZONTAL else NONE,
                yscrollcommand=scrollbar.set if orient == VERTICAL else NONE)
    item.pack(expand=YES, side=TOP if orient == HORIZONTAL else LEFT, fill=BOTH)
    return scrollbar


class Form(object):
    def __init__(self, title: str, geometry: str, font: (str, int)):
        self.root = Tk()
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
    phyton = sys.executable
    os.execl(phyton, phyton, *sys.argv)


def upload_chosen_tests():
    """
    Returns the list of paths to chosen tests
    :return: List[path_to_file]
    """
    programs = []
    try:
        programs = list(askopenfilenames(title='Import Tests(s) to analyze', initialdir=os.getcwd(),
                                         filetypes=[("CPP", ".cpp")]))
    except IOError:
        messagebox.showwarning("Warning", "Folder 'tests' doesn't exist")
    return programs


def upload_default_tests():
    """
    Returns the list of paths to default tests
    :return: List[path_to_file]
    """
    tests = []
    try:
        tests = [os.getcwd() + '/tests/' + file for file in os.listdir(os.getcwd() + '/tests') if
                 file.endswith(".cpp")]
    except IOError:
        from tkinter import messagebox
        messagebox.showwarning("Warning", "Folder 'tests' doesn't exist")
    except Exception as e:
        from tkinter import messagebox
        messagebox.showwarning("Warning", e.args)
    return tests


def get_selected_tests(listbox: Listbox):
    try:
        programs = [listbox.get(idx) for idx in listbox.curselection()]
        if not len(programs):
            raise _tkinter.TclError
        return programs
    except _tkinter.TclError:
        from tkinter import messagebox
        messagebox.showwarning("Warning", "No Test Selected")
        return ()


def start_vulnerabilities(queue, cur_code):
    vulnerabilities_form = None
    try:
        program, content = queue.get(block=True)
        queue.task_done()
        vulnerabilities_form = Form(program + ' Vulnerabilities', '1200x780', FONT)

        l1 = Label(vulnerabilities_form.root, text='Vulnerabilities found:', font=vulnerabilities_form.font, width=28,
                   anchor='w')
        l2 = Label(vulnerabilities_form.root, text='Where:', font=vulnerabilities_form.font, anchor='w')
        l3 = Label(vulnerabilities_form.root, text='Code:', font=vulnerabilities_form.font, anchor='w')

        found = Frame(vulnerabilities_form.root, borderwidth=2, relief="groove", width=28, height=20)
        code = Frame(vulnerabilities_form.root, borderwidth=2, relief="groove", width=178, height=20)
        where = Frame(vulnerabilities_form.root, borderwidth=2, relief="groove", width=150, height=20)
        code_lb = create_listbox(code, EXTENDED, 0)
        found_lb = create_listbox(found, SINGLE, 0,
                                  action=lambda event: write_to_text(where_tb,
                                                                     content[
                                                                         found_lb.get(
                                                                             found_lb.curselection())],
                                                                     'CLEAR'))
        where_tb = Text(where, borderwidth=0, relief="groove", wrap=WORD, state='disabled')

        create_scroll_box(where, where_tb, VERTICAL)
        fill_listbox(code_lb, [f"{index + 1}          " + line for index, line in enumerate(cur_code)])
        fill_listbox(found_lb, content.keys())
        create_scroll_box(code, code_lb, VERTICAL)

        l3.grid(column=0, row=0, padx=(8, 8), pady=(5, 2), sticky=(N, S, E, W))
        l1.grid(column=0, row=2, padx=(8, 8), pady=(5, 2), sticky=(N, S, E, W))
        l2.grid(column=1, row=2, padx=(8, 8), pady=(5, 2), sticky=(N, S, E, W))

        code.grid(column=0, columnspan=2, row=1, padx=(12, 12), pady=(0, 10), sticky=(N, S, E, W))
        found.grid(column=0, row=3, padx=(12, 2), pady=(0, 12), sticky=(N, S, E, W))
        where.grid(column=1, row=3, padx=(2, 12), pady=(0, 12), sticky=(N, S, E, W))

        vulnerabilities_form.root.columnconfigure(0, weight=1)
        vulnerabilities_form.root.columnconfigure(1, weight=20)
        vulnerabilities_form.root.rowconfigure(0, weight=0)
        vulnerabilities_form.root.rowconfigure(1, weight=1)

        vulnerabilities_form.start()
    except Exception as e:
        from tkinter import messagebox
        vulnerabilities_form.error(e.args)
        vulnerabilities_form.exit()


def find_vulnerabilities(programs: tuple or list, vulnerabilities: tuple or list, handler):
    if not (programs and vulnerabilities):
        return 0
    from core.multithreading import create_workers, create_jobs
    from queue import Queue, Empty
    try:
        queue = Queue()
        programs_code = []
        for program in programs:
            cur_code = open(program, 'r').read().splitlines()
            programs_code.append(cur_code)

        create_workers(len(programs), start_vulnerabilities, queue, programs_code)
        content = lambda get_program: dict(
            [(vulnerability, handler(vulnerability, get_program)) for vulnerability in vulnerabilities if
             handler(vulnerability, get_program)])
        create_jobs([(program, content(program)) for program in programs if content(program)], queue)
    except Empty:
        from tkinter import messagebox
        messagebox.showinfo("Info", "No vulnerabilities detected")


class UI(object):

    def __init__(self, vulnerability_names):
        self.uploaded_tests = []
        self.default_tests = upload_default_tests()
        self.vulnerability_names = vulnerability_names

    def fill_programs_list(self, list_box: Listbox):
        self.uploaded_tests = upload_chosen_tests()
        fill_listbox(list_box, [basename(file) for file in self.uploaded_tests])

    def programs_to_analyze(self, listbox: Listbox):
        try:
            programs = []
            selected_programs = [listbox.get(idx) for idx in listbox.curselection()]
            for cur_program in selected_programs:
                for program in self.uploaded_tests:
                    if cur_program in program:
                        programs.append(program)
            if not len(programs):
                raise _tkinter.TclError
            return programs
        except _tkinter.TclError:
            from tkinter import messagebox
            messagebox.showwarning("Warning", "No Program Selected")
            return ()

    def start_main(self, handler):

        def vulnerabilities_to_find(check_buttons_array: tuple or list):
            try:
                vulnerabilities = [item[1].cget('text') for item in check_buttons_array if item[0].get()]
                if not len(vulnerabilities):
                    raise _tkinter.TclError
                return vulnerabilities
            except _tkinter.TclError:
                from tkinter import messagebox
                messagebox.showwarning("Warning", "No Vulnerability Selected")
                return ()

        main_form = None
        try:
            main_form = Form('Analyzer', '1178x652', FONT)
            main_form.root.focus_force()

            main_menu = Menu()
            file_menu = Menu(tearoff=0)
            file_menu.add_command(label="Open", command=lambda: self.fill_programs_list(manual_tests_lb))
            file_menu.add_command(label="New project", command=lambda: restart_program())
            file_menu.add_command(label="Exit", command=lambda: main_form.root.quit())
            main_menu.add_cascade(label="File", menu=file_menu)
            main_form.root.config(menu=main_menu)

            frame1 = Frame(main_form.root, borderwidth=4, relief="groove")
            frame2 = LabelFrame(main_form.root, text="Default tests", borderwidth=2, relief="groove", width=200)
            frame3 = LabelFrame(main_form.root, text="Chosen tests", borderwidth=2, relief="groove")
            frame4 = Frame(main_form.root)
            frame5 = Frame(main_form.root)

            def_tests_lb = create_listbox(frame2, EXTENDED, 0)
            manual_tests_lb = create_listbox(frame3, EXTENDED, 0)
            create_scroll_box(frame2, def_tests_lb, VERTICAL)
            create_scroll_box(frame3, manual_tests_lb, VERTICAL)
            vulnerability_check_list = tuple([create_check_button(frame1, text=vulnerability,
                                                                  height=1, width=30, anchor=W)
                                              for vulnerability in self.vulnerability_names])

            check_btn_1 = Button(frame2, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                 state=NORMAL if self.default_tests else DISABLED,
                                 font=main_form.font, text="Check",
                                 command=lambda: find_vulnerabilities(
                                     [os.getcwd() + '/tests/' + file for file in get_selected_tests(def_tests_lb)],
                                     vulnerabilities_to_find(vulnerability_check_list), handler))
            check_btn_1.pack(side=TOP)

            check_all_btn_1 = Button(frame2, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                     state=NORMAL if self.default_tests else DISABLED,
                                     font=main_form.font, text="Check all",
                                     command=lambda: find_vulnerabilities(self.default_tests,
                                                                          vulnerabilities_to_find(
                                                                              vulnerability_check_list),
                                                                          handler))
            check_all_btn_1.pack(side=TOP)

            check_btn_2 = Button(frame3, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                 state=NORMAL, font=main_form.font,
                                 text="Check",
                                 command=lambda: find_vulnerabilities(self.programs_to_analyze(manual_tests_lb),
                                                                      vulnerabilities_to_find(
                                                                          vulnerability_check_list),
                                                                      handler))
            check_btn_2.pack(side=TOP)

            check_all_btn_2 = Button(frame3, width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
                                     state=NORMAL, font=main_form.font,
                                     text="Check all",
                                     command=lambda: find_vulnerabilities(self.uploaded_tests,
                                                                          vulnerabilities_to_find(
                                                                              vulnerability_check_list),
                                                                          handler))
            check_all_btn_2.pack(side=TOP)
            load = Image.open(os.getcwd() + '/photo/logo.png')
            render = ImageTk.PhotoImage(load)
            img = Label(main_form.root, image=render)
            img.image = render

            frame1.grid(column=0, row=0, rowspan=2, columnspan=2, padx=20, pady=20, sticky=NW)
            frame2.grid(column=2, row=0, padx=(8, 8), pady=20, sticky=NW)
            frame3.grid(column=3, row=0, padx=(8, 12), pady=20, sticky=NW)
            frame4.grid(column=2, row=1, padx=(8, 12), pady=20, sticky=NW)
            frame5.grid(column=3, row=1, padx=(8, 12), pady=20, sticky=NW)
            img.grid(column=0, row=1, padx=(8, 12), pady=(5, 10), sticky=SE)

            main_form.root.columnconfigure(0, weight=0)
            main_form.root.columnconfigure(1, weight=1)
            main_form.root.columnconfigure(2, weight=10)
            main_form.root.columnconfigure(3, weight=10)
            main_form.root.columnconfigure(4, weight=10)
            main_form.root.rowconfigure(0, weight=1)
            main_form.root.rowconfigure(1, weight=0)

            fill_listbox(def_tests_lb, [basename(file) for file in self.default_tests])

            main_form.start()
        except Exception as e:
            from tkinter import messagebox
            main_form.error(e.args)
            main_form.exit()
