#include <stdio.h>
#include <string.h>
int main()
{
    char s1 [80];
    char s2 [80];
    gets(s1);
    gets(s2);
    strcat(s2, s1); // no bounds checking
    printf(s2);
    return 0;
}