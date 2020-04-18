#include <stdio.h>
#include <stdlib.h>
#include <time.h>
void keygen()
{
    printf("First number: %d\n", srand(500) % 100);
    srand(time(NULL));
    printf("Random number: %d\n", rand() % 100);
    srand(1);
    printf("Again the first number: %d\n", rand() % 100);
}
