#include <string.h>

void foo (char *bar){
   char  c[12];

   strcpy(c, bar);  // no bounds checking
}

int main (int argc, char **argv){
   foo(argv[1]);
   char c[11];
   strcpy(c, *argv);
   return 0;
}