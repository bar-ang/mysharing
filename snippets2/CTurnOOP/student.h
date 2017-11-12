#include "person.h"

#define STUDY_LEN 64

typedef struct student Student;

struct student
{
	Person super;
	float gpa;
	int year;
	char study[STUDY_LEN];
};

void init_student(Student * student, char name[], char id[], int age, enum e_gender gender, float gpa, int year, char study[]);

void student_formal_title(Student * student, char * title);