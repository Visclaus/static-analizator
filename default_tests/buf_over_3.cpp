#include <string.h>

int main (char **argv){
    char a[4];
    strcpy(a ,"a string longer than 4 characters"); // write past end of buffer (buffer overflow)
    printf("%s\n",a[6]); // read past end of buffer (also not a good idea)
}
2) Предупреждение в методе <main>!
Использование буфера <char a[4]> (строка 4) в небезопасной функции <printf> (строка 6).
Это может стать причиной переполнения буфера. Убедитесь в наличии проверки этой угрозы!
