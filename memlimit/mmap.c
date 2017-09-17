#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <string.h>

int main(int argc, char ** argv){
	int f = open("msg.txt",O_RDWR);
	if(f < 0){
		printf("Cannot open file: %s\n",strerror(errno));
		return errno;
	}
	char * map = (char *)mmap(NULL, 80, PROT_READ|PROT_WRITE, MAP_SHARED, f, 0);
	if(map == (char *)(-1)){
		printf("Cannot map: %s\n",strerror(errno));
		return errno;
	}

	sprintf(map,"Getting nowhere\n");

	if(munmap(map, 5)< 0){
		printf("Cannot unmap: %s\n",strerror(errno));
		return errno;
	}

	return 0;
}