#include "stdafx.h"
#include <iostream>
#include <stdlib.h>


int random_addition(){
	int a = std::rand();
	printf("a = %d\n",a);
	int b = std::rand();
	printf("b = %d\n", b);
	int c = std::srand(500);
	printf("c = %d\n", c);
	c = a + b + c;
	printf("result of sum = %d\n", c);
	return 0;
}

int main(){
	for (int i = 0; i < 10; i++)
	{
		int random_value = std::rand();
		printf("random_value = %d\n", random_value);
	}
	random_addition();
	getchar();
    return 0;
}
