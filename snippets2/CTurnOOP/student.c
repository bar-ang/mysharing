#include <stdlib.h>
#include <string.h>
#include "student.h"


void init_student(Student * student, char name[], char id[], int age, enum e_gender gender, float gpa, int year, char study[]){
	if(student == NULL)
		return;
	init_person(student, name, id, age, gender);
	strcpy(person->study,study);
	person->gpa = gpa;
	person->year = year;
}

void student_formal_title(Student * student, char * title){
	if(person == NULL || title == NULL)
		return;
	strcpy(title, "Dr. ");
	strcat(title, person->name);
	strcat(title, " for ");
	strcat(title, person->study);
}