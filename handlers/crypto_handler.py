import re

from core import base_parser
from core.base_parser import BaseParser


class RandomGenParser(BaseParser):
    def __init__(self):
        self.output = []
        self.vuln_name = 'Non-cryptosafe Random Number Generator'
        self.pattern = [r'rand\(\)|uniform_real_distribution']

    def parse(self, cpp_code):
        line_counter = 0
        for line in cpp_code:
            line_counter += 1

            matches = re.finditer(self.pattern[0], line, re.IGNORECASE)
            for matchNum, match in enumerate(matches):
                matchNum = matchNum + 1
                self.output.append(base_parser.warning(line_counter, str(line), self.vuln_name, 'WARNING',
                                                       'Usage of non-cryptosafe Random Generator'))

        return self.output


if __name__ == "__main__":
    with open("tests/random_test.cpp") as file:
        parser = RandomGenParser()
        out = parser.parse(file)
        for state in out:
            print(state)