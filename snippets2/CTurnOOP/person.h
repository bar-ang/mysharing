#define NAME_LEN 64
#define ID_LEN 9


typedef struct person Person;

enum e_gender{
	male, female, other
};

struct person
{
	int age;
	enum e_gender gender;
	char name[NAME_LEN];
	char id[ID_LEN];
} ;



void init_person(Person * person, char name[], char id[], int age, enum e_gender gender);

void person_formal_title(Person * person, char * title);