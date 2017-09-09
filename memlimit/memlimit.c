#include <stdlib.h>
#include <stdio.h>

int main(int argc, char ** argv){
	int x[100];

	//for(int i=0;i<1000;i++)
		asm("mov esp, esp");

	printf("limited.\n");
	int * y = (int*)malloc(100*sizeof(int));
	
	return 0;
}