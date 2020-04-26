#include <stdio.h>
int main()
{
	int a;
	int b = 0;
	int c = 0;
	try{

	} catch(er){
	Error error = GetLastError(er);
    }
	*printf("Vvod a:", a);
	scanf_s("%d", &a);
	printf("Vvod b:", b);
	scanf_s("%d", &b);
	c = a + b;
	printf("Result: %d", c);
	return 0;
}