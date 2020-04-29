#include <string.h>

void func_1(char *param_1, int *param_2){
   char c[12];
   int *c = new int[12];
   int size = 1;
   strcpy(c, param_1);
   memcpy(c, param_2, size)
}


int main (char **argv){
   char c[12];
   func_1(argv[1], argv[2]);
   strcpy(c, argv[3]);
   return 0;
}