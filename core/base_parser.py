import collections

warning = collections.namedtuple('Warning', ['line_count', 'line', 'name', 'lvl', 'msg'])


class BaseParser:
    def __init__(self, analyzer_context):
        self.analyzer_context = analyzer_context
        self.vulnerability_name = "base vulnerable"
        self.output = []  # array of warnings

    def parse(self, cpp_code):
        pass

