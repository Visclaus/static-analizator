func_decl_regexp = \
        r"^(char|unsigned char|signed char|int|byte|unsigned int|signed int|short int|unsigned short int|" \
        r"signed short int|long int|singed long int|unsigned long int|long long int|signed long long int|" \
        r"unsigned long long int|float|double|long double|wchar_t|short|long|void)\s+" \
        r"(\*+\s*)?" \
        r"(\w+)\s*" \
        r"(\(.*\))"

func_param_regexp = \
    r"(char|unsigned char|signed char|int|byte|unsigned int|signed int|short int|unsigned short int|" \
    r"signed short int|long int|singed long int|unsigned long int|long long int|signed long long int|" \
    r"unsigned long long int|float|double|long double|wchar_t|short|long)\s+" \
    r"(\*+\s*)?" \
    r"(\w+)\s*" \
    r"(\[.*\])*"

variable_regexp = \
    r"^(extern\s+)?" \
    r"(const\s+)?" \
    r"(char|unsigned char|signed char|int|byte|short|long|ofstream|ifstream||wchar_t" \
    r"|unsigned int|signed int|short int|unsigned short int|signed short int|long int|singed long int" \
    r"|unsigned long int|long long int|signed long long int|unsigned long long int|float|double|long double)\s+" \
    r"(\*+\s*)?" \
    r"(\w+)\s*" \
    r"(\[.+]\s*)?" \
    r"(=.+)?\s*;"

assignment_regexp = r"(\w+)\s*=\s*(.+)\s*;"

thread_regexp = r'^(std::)?thread\s+(\w+)\s*\(\s*(\w+)\s*(,\s*[\w,"]*\s*)*\)\s*;'
