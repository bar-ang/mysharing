#include <stdlib.h>
#include <string.h>
#include "person.h"


void init_person(Person * person, char name[], char id[], int age, enum e_gender gender){
	if(person == NULL)
		return;
	strcpy(person->name,name);
	strcpy(person->id,id);
	person->age = age;
	person->gender = gender;
}

void person_formal_title(Person * person, char * title){
	if(person == NULL || title == NULL)
		return;
	strcpy(title, "Mr. ");
	strcat(title, person->name);
}