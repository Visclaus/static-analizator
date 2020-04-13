#include  <stdio.h>
#include  <string.h>
#include  <stdlib.h>

int main (int argc, char argv)
{
	char buf[100];
	int *x = 1 ;
	int y[] = 2 ;
	x = 3;
	x = x+y;
	x = x/y;
	x = x + 216512512512512512512521;
    printf(x);
    char buf[100];
	return 0 ;
}