import re

from core.UI import UI
from core.main_code_parser import find_contexts
from handlers.buffer_overflow_handler import BufferOverflowHandler
from handlers.commands_introduction_hadler import CommandsIntroductionHandler
from handlers.data_leak_handler import DataLeakHandler
from handlers.data_storage_handler import DataStorageManagementHandler
from handlers.empty_catch_handler import EmptyCatchHandler
from handlers.file_access_handler import IncorrectFileAccessHandler
from handlers.format_string_handler import FormatStringHandler
from handlers.integer_overflow_handler import IntegerOverflowHandler
from handlers.memory_leak_handler import MemoryLeakHandler
from handlers.race_condition_handler import RaceConditionHandler
from handlers.readers_writers_handler import ReadersWritersHandler
from handlers.random_generator_handler import RandomGeneratorHandler
from handlers.sql_injection_handler import SQLInjectionHandler

handlers = {
    BufferOverflowHandler.vulnerability_name: BufferOverflowHandler,
    IntegerOverflowHandler.vulnerability_name: IntegerOverflowHandler,
    RandomGeneratorHandler.vulnerability_name: RandomGeneratorHandler,
    CommandsIntroductionHandler.vulnerability_name: CommandsIntroductionHandler,
    DataLeakHandler.vulnerability_name: DataLeakHandler,
    SQLInjectionHandler.vulnerability_name: SQLInjectionHandler,
    EmptyCatchHandler.vulnerability_name: EmptyCatchHandler,
    "Format String Vulnerability": FormatStringHandler,
    "Incorrect file access": IncorrectFileAccessHandler,
    "Bad Data Storage Management": DataStorageManagementHandler,
    "Race Condition": RaceConditionHandler,
    "Memory Leak": MemoryLeakHandler,
    "Readers–writers problem": ReadersWritersHandler,
}


def replace(match):
    return None if match.group(0).startswith('/') else match.group(0)


def clean_code(program):
    pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE)
    tmp = []
    text = open(program, 'r').read()
    cleaned_code = re.sub(pattern, replace, text)
    for line in cleaned_code.splitlines():
        tmp.append(line.lstrip())
    return tmp


if __name__ == '__main__':
    ui = UI(handlers.keys())
    ui.start_main(lambda vulnerability, program: handlers[vulnerability]().parse(find_contexts(clean_code(program))))
