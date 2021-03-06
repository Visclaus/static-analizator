from collections import namedtuple

func_types = ["char", "unsigned char", "signed char", "int", "byte", "unsigned int", "signed int", "short int",
              "unsigned short int", "signed short int", "long int", "singed long int", "unsigned long int",
              "long long int", "signed long long int", "unsigned long long int", "float", "double", "long double",
              "wchar_t", "void"]

sample_words = ["Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "sed", "do", "eiusmod",
                "tempor", "incididunt", "ut", "labore", "et", "dolore", "magna", "aliqua", "Ut", "enim", "ad", "minim",
                "veniam", "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi", "ut", "aliquip", "ex", "ea",
                "commodo", "consequat.", "Duis", "aute", "irure", "dolor", "in", "reprehenderit", "in", "voluptate",
                "velit", "esse", "cillum", "dolore", "eu", "fugiat", "nulla", "pariatur.", "Excepteur", "sint",
                "occaecat", "cupidatat", "non", "proident,", "sunt", "in", "culpa", "qui", "officia", "deserunt",
                "mollit", "anim", "id", "est", "laborum."
                ]

types = ["char", "unsigned char", "signed char", "int", "byte", "unsigned int", "signed int", "short int",
         "unsigned short int", "signed short int", "long int", "singed long int", "unsigned long int",
         "long long int", "signed long long int", "unsigned long long int", "float", "double", "long double",
         "wchar_t"]

stream_types = ["ifstream", "ofstream"]

int_types = ["int", "short", "char", "long", "byte"]

cond = ["==", "<", ">", "<=", ">=", "!="]

Limit = namedtuple('Limit', 'min max')
integer_limits = {'int': Limit(-2 ** 31, 2 ** 31 - 1),
                  'byte': Limit(-2 ** 15, 2 ** 15 - 1),
                  'short': Limit(-2 ** 15, 2 ** 15 - 1),
                  'char': Limit(-2 ** 7, 2 ** 7 - 1),
                  'long': Limit(-2 ** 63, 2 ** 63 - 1)}



