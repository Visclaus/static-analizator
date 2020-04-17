# from core import parse_utils
# from core.parse_utils import *
# from handlers.race_condition_handler import RaceConditionHandler
# from handlers.sql_injection_handler import SqlInjectionHandler
#
# if __name__ == '__main__':
#     # text = "int param1;\nint param2;\nint param;\nint param4;\nstd::thread t1(run, param1, param)\nstd::thread t2(get, param1, param2)\nstd::thread t3(run, param1, param2)"
#     # formatted_text = text.split("\n")
#     # analyzer_context = AnalyzerContext(formatted_text)
#     # output = RaceConditionHandler(analyzer_context).parse(formatted_text)
#     text = "executeQuery(\"select * from users where name='lol'\")\nexecute(justParam)"
#     formatted_text = text.split("\n")
#     analyzer_context = AnalyzerContext(formatted_text)
#     output = SqlInjectionHandler(analyzer_context).parse(formatted_text)

# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
from os import getcwd

from core.UI import UI
from core.main_code_parser import get_initial_contexts, find_contexts, AnalyzedCode
from handlers.buffer_overflow_handler import BufferOverflowHandler
from handlers.empty_catch_handler import EmptyCatchHandler
from handlers.format_string_handler import FormatStringHandler
from handlers.race_condition_handler import RaceConditionHandler
from handlers.rng_handler import RandomGenHandler
from handlers.sql_injection_handler import SQLInjectionHandler

HANDLER = {
    "Buffer Overflow": BufferOverflowHandler,
    "Empty Catch Block": EmptyCatchHandler,
    # "Format String Vulnerability": FormatStringHandler,
    # "SQL injection": SqlInjectionHandler,
    # "Command Injection": None,
    # "Neglect of Error Handling":		None,
    # "Bad Data Storage Management":		None,
    # "Data Leak":						None,
    "Non safe random generator algorithms": RandomGenHandler,
    # "Integer Overflow": None,
    "Race Condition": RaceConditionHandler,
    # "Readers–writers problem":			None,
    # "Locked Mutexes problem":         None
}


def comment_remover(text):
    import re
    pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE)
    replacer = lambda match: None if match.group(0).startswith('/') else match.group(0)
    return re.sub(pattern, replacer, text)


def clean_code(program):
    tmp = []
    for line in comment_remover(open(program, 'r').read()).splitlines():
        tmp.append(line.lstrip())
    return tmp


if __name__ == '__main__':
    from re import match

    test = '  test with   spaces'
    just_space = ''
    test = test.lstrip()
    just_space = just_space.lstrip()
    CLEAN_CODE = lambda program: [line.lstrip() for line in comment_remover(open(program, 'r').read()).splitlines()]
    #
    # code = CLEAN_CODE(getcwd() + '/tests/' + 'dev_test.cpp')
    # main_code_parser = AnalyzedCode(code)
    ui = UI(HANDLER.keys())  #
    ui.start_main(lambda vulnerability, program: HANDLER[vulnerability]().parse(find_contexts(CLEAN_CODE(program))))
