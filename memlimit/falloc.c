#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/user.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>


#define BRK_EAX 12

int main(int argc, char ** argv){

	int pid = fork();
	if(pid < 0){
		printf("Fork failed.\n");
		return -1;
	}
	
	if(pid != 0){
		//child process is replaced with the wanted program.
		if(execv(argv[1],argv+1)<0){
			printf("execv failed.\n");	
			return -1;
		}
	}
	struct user_regs_struct regs;
	int status;

	//father proccess (the "debuger")
	if(ptrace(PTRACE_ATTACH,pid,NULL,NULL) < 0){
		printf("PTRACE_ATTACH failed.\n");	
		return -1;
	}


	waitpid(pid,&status,0);
	if(WIFEXITED(status)){
		printf("child done.\n");
		return 0;
	}

	
	while(1){
		if(ptrace(PTRACE_SYSCALL,pid,0,0)){
			printf("PTRACE_SYSCALL failed.\n");	
			return -1;
		}
		
		waitpid(pid,&status,0);
		if(WIFEXITED(status)){
			printf("child done.\n");
			return 0;
		}

		if(ptrace(PTRACE_GETREGS,pid,0,&regs)){
			printf("PTRACE_GETREGS failed.\n");	
			return -1;
		}

		if(regs.orig_eax == BRK_EAX){
			if(ptrace(PTRACE_POKETEXT,pid,regs.ecx,-1)){
				printf("PTRACE_POKETEXT failed.\n");	
				return -1;
			}
		}
	}

	return 0;
}