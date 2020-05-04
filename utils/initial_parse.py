import re


def replace(match):
    return None if match.group(0).startswith('/') else match.group(0)


def clean_code(program, mode='r'):
    pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE)
    tmp = []
    a = open(program, mode)
    text = a.read()
    cleaned_code = re.sub(pattern, replace, text)
    for line in cleaned_code.splitlines():
        tmp.append(line.lstrip())
    a.close()
    return tmp