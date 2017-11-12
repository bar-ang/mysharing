#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "student.h"

int main(){
	Student bar;
	init_student(&bar,"Bar Angel","307901587",24, male, 85.2, 3, "Computer Science");

	char title[NAME_LEN+5];
	student_formal_title(&bar, title);

	printf("%s\n", title);

	return 0;
}

