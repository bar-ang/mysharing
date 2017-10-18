#include <linux/module.h>
#include <linux/kernel.h>
#include <asm/uaccess.h>
#include <linux/string.h>   /* for memset. NOTE - not string.h!*/
#include <linux/sched.h>
#include <linux/moduleparam.h>
#include <linux/unistd.h>
#include <linux/syscalls.h>
#include <linux/delay.h>
#include <asm/paravirt.h>

#define MAX_SHOW 256
#define WILD_FOLDER "/home/bar/git/mysharing/kernel/wild/"
#define TROLLER "/home/bar/git/mysharing/kernel/wild/file1.txt"

unsigned long **sys_call_table;
unsigned long original_cr0;

//static int uid;
//module_param(uid, int, 0644);

asmlinkage int (*original_call) (const char *, int, int);

asmlinkage int our_sys_open(const char *filename, int flags, int mode){
	int i = 0;
	char ch[MAX_SHOW];
	char trol[MAX_SHOW];
	while(filename[i] != 0 && i < MAX_SHOW-1){
		ch[i] = filename[i];
		i++;
	}
	ch[i] = '\0';

	
	strcpy(trol, TROLLER);
	if(strstr(ch,WILD_FOLDER) != NULL){
		return original_call(trol, flags, mode);
	}else{
		return original_call(filename, flags, mode);
	}
}

static unsigned long **aquire_sys_call_table(void)
{
	unsigned long int offset = PAGE_OFFSET;
	unsigned long **sct;

	while (offset < ULLONG_MAX) {
		sct = (unsigned long **)offset;

		if (sct[__NR_close] == (unsigned long *) sys_close) 
			return sct;

		offset += sizeof(void *);
	}
	
	return NULL;
}

int init_module(){

	if(!(sys_call_table = aquire_sys_call_table()))
		return -1;


	original_cr0 = read_cr0();
	write_cr0(original_cr0 & ~0x00010000);

	original_call = (void *)sys_call_table[__NR_open];
	sys_call_table[__NR_open] = (unsigned long *)our_sys_open;

	write_cr0(original_cr0);
	printk(KERN_INFO "Spying on 'open'\n");
	return 0;
}

void cleanup_module(){
	if(!sys_call_table) {
		return;
	}
	printk("Restoring MKDIR syscall\n");
	write_cr0(original_cr0 & ~0x00010000);

	sys_call_table[__NR_open] = (unsigned long *)original_call;

	write_cr0(original_cr0);
	
	msleep(2000);
}


MODULE_LICENSE("GPL");
