#include <stdlib.h>
#include <stdio.h>

int main(int argc, char ** argv){
	int * y = (int*)malloc(100*sizeof(int));
	
	if(y == NULL){
		printf("memory allocation failed.\n");
		return -1;
	}

	printf("OK! %s\n", argv[1]);
	free(y);
	return 0;
}