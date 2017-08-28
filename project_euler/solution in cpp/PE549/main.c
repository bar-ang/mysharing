/*
 * main.c
 *
 *  Created on: Dec 9, 2016
 *      Author: Bar Angel
 */

#include <stdio.h>
#include <stdlib.h>

#define BYTE 8

void orb(void * arr, int loc){
	int offset = loc / BYTE;
	int local = loc % BYTE;
	char* carr = (char*)arr;
	carr[offset] ^= 1<<local;
}


int bitget(void * arr, int loc){
	int offset = loc / BYTE;
	int local = loc % BYTE;
	char seg = ((char*)arr)[offset];
	seg = seg>>local;

	return 1&seg;
}

void bitalt(void * bits, int size, int alt){
	for(int i=0;i < size; i+= alt)
		orb(bits,i);
}

int main(){
	void* dat = calloc(2,BYTE);

	char* ch = (char*)dat;
	int val = (int)dat;

	ch[0] = 255;
	ch[1] = 255;

	for(int i=0;i<sizeof(int)*BYTE;i++) {
	    if (val & 1)
	        printf("1");
	    else
	        printf("0");

	    val >>= 1;
	}
	printf("\n");

	free(dat);
	return 0;
}
