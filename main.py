from UI.UI import UI
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
from handlers.random_generator_handler import RandomGeneratorHandler
from handlers.readers_writers_handler import ReadersWritersHandler
from handlers.sql_injection_handler import SQLInjectionHandler
from utils.initial_parse import clean_code

handlers_list = {
    BufferOverflowHandler.vulnerability_name: BufferOverflowHandler,

    CommandsIntroductionHandler.vulnerability_name: CommandsIntroductionHandler,

    DataLeakHandler.vulnerability_name: DataLeakHandler,

    DataStorageManagementHandler.vulnerability_name: DataStorageManagementHandler,

    EmptyCatchHandler.vulnerability_name: EmptyCatchHandler,

    IncorrectFileAccessHandler.vulnerability_name: IncorrectFileAccessHandler,

    FormatStringHandler.vulnerability_name: FormatStringHandler,

    IntegerOverflowHandler.vulnerability_name: IntegerOverflowHandler,

    MemoryLeakHandler.vulnerability_name: MemoryLeakHandler,

    RaceConditionHandler.vulnerability_name: RaceConditionHandler,

    RandomGeneratorHandler.vulnerability_name: RandomGeneratorHandler,

    ReadersWritersHandler.vulnerability_name: ReadersWritersHandler,

    SQLInjectionHandler.vulnerability_name: SQLInjectionHandler,
}


if __name__ == '__main__':
    ui = UI(handlers_list.keys())
    ui.start_main(
        lambda vulnerability, program: handlers_list[vulnerability]().parse(find_contexts(clean_code(program))))
