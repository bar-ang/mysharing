#include <stdlib.h>
#include <stdio.h>

int main(){
	char z = 0;
	void * a = (void *)(&z);
	printf("%x (16) %d (10)\n", (int)a, (int)a);

	return 0;
}