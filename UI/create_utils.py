from tkinter import *

FONT = ("Helvetica", 12)
BUTTON_WIDTH = 13
BUTTON_HEIGHT = 1
MAIN_COLOR = "#DDC2BD"


def create_check_button(parent: Frame, bg, text: str, height: int, width: int, anchor, value: int = 0):
    value = IntVar(value=value)
    ch_button = Checkbutton(parent, bg=bg, font=("Helvetica", 12), activebackground=bg, variable=value, text=text, height=height,
                            width=width, anchor=anchor, fg="black")
    ch_button.pack()
    return value, ch_button


def create_button(parent: Widget, text, ui, func):
    return Button(parent, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, state=NORMAL if ui.default_tests
    else DISABLED, font=FONT, text=text, bd=2, anchor=W,
                  command=func)


def create_listbox(parent: Widget, select_mode, border_width: int, action=None, font=FONT):
    listbox = Listbox(parent, font=font, width=20, selectmode=select_mode, exportselection=False,
                      borderwidth=border_width)
    listbox.pack(fill=Y)
    listbox.bind('<<ListboxSelect>>', action)
    return listbox


def create_scroll_box(frame, item, orient=HORIZONTAL):
    scrollbar = Scrollbar(frame, orient=orient)
    scrollbar.config(command=item.xview if orient == HORIZONTAL else item.yview)
    scrollbar.pack(side=BOTTOM if orient == HORIZONTAL else RIGHT, fill=X if orient == HORIZONTAL else Y)
    item.config(xscrollcommand=scrollbar.set if orient == HORIZONTAL else NONE,
                yscrollcommand=scrollbar.set if orient == VERTICAL else NONE)
    item.pack(side=TOP if orient == HORIZONTAL else LEFT)
    return scrollbar


def create_code_scroll_box(frame, item, orient=HORIZONTAL):
    scrollbar = Scrollbar(frame, orient=orient)
    scrollbar.config(command=item.xview if orient == HORIZONTAL else item.yview)
    item.config(xscrollcommand=scrollbar.set if orient == HORIZONTAL else NONE,
                yscrollcommand=scrollbar.set if orient == VERTICAL else NONE)
    return scrollbar


def create_code_listbox(parent: Widget, select_mode, border_width: int, action=None, font=FONT, bg="white"):
    listbox = Listbox(parent, font=font, width=129, height=18, selectmode=select_mode, exportselection=False,
                      borderwidth=border_width, bg=bg)
    listbox.pack(fill=BOTH, expand=TRUE)
    listbox.bind('<<ListboxSelect>>', action)
    return listbox
