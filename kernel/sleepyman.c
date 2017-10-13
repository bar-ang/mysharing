#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>

#define SLEEPER "/proc/sleeper"

int main(int argv, char ** argc){
	if(argv <= 1){
		printf("You forgot the message. :(\n");
		return -1;
	}
	printf("When I'll wake up I'll tell you.\n");

	int f = open(SLEEPER,O_RDONLY);
	if(f < 0){
		printf("failed to open the sleeper: %s\n", strerror(errno));		
		return errno;
	}
	char b[1];
	int r = read(f, b, 1);
	if(r < 0){
		printf("failed to read from sleeper: %s\n", strerror(errno));		
		return errno;
	}

	printf("Good morning: %s\n", argc[1]);	
	return 0;
}