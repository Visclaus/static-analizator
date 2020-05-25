#include <string.h>
std::mutex SyncMutex;
mutex testMutex;
char *func_1(char *param_1, int *param_2)
{
   char c;
   unsigned int *var_27 = new unsigned int;
   c = 'c';
   int size = 1;
   char t = c;
   int d = size;
   strcpy(c, param_1);
   memcpy(c, param_2, size);
}


int main (char **argv){
   char c[12];
   func_1(argv[1], argv[2]);
   strcpy(c, argv[3]);
   return 0;
}