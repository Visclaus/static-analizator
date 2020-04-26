#include <string.h>

int main (char **argv){
    char a[4];
    strcpy(a ,"a string longer than 4 characters"); // write past end of buffer (buffer overflow)
    printf("%s\n",a[6]); // read past end of buffer (also not a good idea)
}