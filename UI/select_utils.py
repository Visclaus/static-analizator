import _tkinter
from tkinter import Listbox


def get_selected_t(listbox: Listbox):
    try:
        selected = [listbox.get(idx) for idx in listbox.curselection()]
        if not len(selected):
            raise _tkinter.TclError
        return selected
    except _tkinter.TclError:
        from tkinter import messagebox
        messagebox.showwarning("Предупреждение", "Тесты не выбраны!")
        return ()


def get_selected_p(chosen_programs, listbox: Listbox):
    try:
        programs_path = []
        selected = [listbox.get(idx) for idx in listbox.curselection()]
        for select in selected:
            for program in chosen_programs:
                if select in program: programs_path.append(program)
        if not len(programs_path):
            raise _tkinter.TclError
        return programs_path
    except _tkinter.TclError:
        from tkinter import messagebox
        messagebox.showwarning("Предупреждение", "Программы не выбраны!")
        return ()


def get_selected_v(check_buttons_array: tuple or list):
    try:
        vulnerabilities = [item[1].cget('text') for item in check_buttons_array if item[0].get()]
        if not len(vulnerabilities):
            raise _tkinter.TclError
        return vulnerabilities
    except _tkinter.TclError:
        from tkinter import messagebox
        messagebox.showwarning("Предупреждение", "Уязвимости не выбраны")
        return ()
