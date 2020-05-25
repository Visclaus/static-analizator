#include <string.h>

void func_1(char *param_1, int *param_2){
   char c[12];
   int *c = new int[12];
   gets(c)
   int size = 1;
   strcat(c, param_1);
}
2) Предупреждение в методе <func_1>!
Использование буфера <char c[12]> (строка 4) в небезопасной функции <strcat> (строка 8).
Это может стать причиной переполнения буфера. Убедитесь в наличии проверки этой угрозы!
