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

from core.UI import UI
from core.analyzer_context import AnalyzerContext
from core.main_code_parser import get_initial_contexts, find_contexts
from handlers.buffer_overflow_handler import BufferOverflowHandler
from handlers.format_string_handler import FormatStringHandler
from handlers.sql_injection_handler import SqlInjectionHandler

HANDLER = {
    "Buffer Overflow": BufferOverflowHandler,
    "Format String Vulnerability": FormatStringHandler,
    "SQL injection": SqlInjectionHandler,
    # "Command Injection": None,
    # "Neglect of Error Handling":		None,
    # "Bad Data Storage Management":		None,
    # "Data Leak":						None,
    # "Not Crypto-resistant Algorithms": None,
    # "Integer Overflow": None,
    # "Race Condition": None,
    # "Readers–writers problem":			None,
    # "Locked Mutexes problem":         None
}


def comment_remover(text):
    import re
    pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE)
    replacer = lambda match: None if match.group(0).startswith('/') else match.group(0)
    return re.sub(pattern, replacer, text)


if __name__ == '__main__':
    from re import match
    source = "int function(int   param1, char param2){\nint var = 2;\nstring test = \"text\";\nstd::thread t1(run, var, test);\nstd::thread t2(get, var);\n}\nint function2(){\nint test;\ntest\n \n}"
    formatted_text = source.split("\n")
    contexts = find_contexts(formatted_text)
    text = "int param1 =  5;\nint param2 = param1;\nint param;\nint param4;\nstd::thread t1(run, param1, param)\nstd::thread t2(get, param1, param2)\nstd::thread t3(run, param1, param2)"
    analyzer_context = AnalyzerContext(formatted_text)
    #output = RaceConditionHandler(analyzer_context).parse(formatted_text)
    text = "executeQuery(\"select * from users where name='lol'\")\nexecute(justParam)"
    formatted_text = text.split("\n")
    analyzer_context = AnalyzerContext(formatted_text)
    output = SqlInjectionHandler(analyzer_context).parse(formatted_text)
CLEAN_CODE = lambda program: [line.lstrip() for line in comment_remover(open(program, 'r').read()).splitlines() if
                              not match(r'^\s*$', line)]

ui = UI(HANDLER.keys())  #
ui.start_main(lambda vulnerability, program: HANDLER[vulnerability](AnalyzerContext(CLEAN_CODE(program))).parse(
    CLEAN_CODE(program)))
