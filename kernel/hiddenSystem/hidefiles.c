#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/syscalls.h>
#include <linux/delay.h>
#include <asm/paravirt.h>
#include <linux/moduleparam.h>  /* which will have params */
#include <linux/unistd.h>       /* The list of system calls */
#include <linux/sched.h>
#include <linux/uaccess.h>
#include <linux/string.h>

#define MESSAGE "THIS FILE IS HIDDEN."
#define SYSC __NR_read
#define BUFFSIZE 256
unsigned long **sys_call_table;
unsigned long original_cr0;


/*
 * UID we want to spy on - will be filled from the
 * command line
 */
static int uid;
module_param(uid, int, 0644);


asmlinkage int (*original_call) (int, void *, size_t );

int read_subsitute(int fd, void *buf, size_t count){
	char compact[BUFFSIZE];
	int result;
	compact[0] = 'a';
	compact[1] = 0;
	result = original_call(fd, buf, count);

	//char buff_in_kernel[BUFFSIZE];
	//char * p;
	//for(p = buff_in_kernel;p<buff_in_kernel+count && p<buff_in_kernel+BUFFSIZE-1; p++){
		//get_user(*p, (char *)buf);
		//*p = *buf;
	//	buf++;
	//}
	//*p = 0;
	//if(strstr(compact,MESSAGE) != NULL)
		//printk("read: %s\n", (char *)compact);
	return result;
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


static int __init syscall_start(void)
{
    if(!(sys_call_table = aquire_sys_call_table()))
        return -1;

    original_cr0 = read_cr0();

    write_cr0(original_cr0 & ~0x00010000);

    /* keep track of the original open function */
    original_call = (void*)sys_call_table[SYSC];

    /* use our open function instead */
    sys_call_table[SYSC] = (unsigned long *)read_subsitute;

    write_cr0(original_cr0);

    printk(KERN_INFO "Spying on UID:%d\n", uid);

    return 0;
}

static void __exit syscall_end(void)
{
	
    if(!sys_call_table) {
        return;
    }

    /*
     * Return the system call back to normal
     */
    if (sys_call_table[SYSC] != (unsigned long *)read_subsitute) {
        printk(KERN_ALERT "Somebody else also played with the ");
        printk(KERN_ALERT "open system call\n");
        printk(KERN_ALERT "The system may be left in ");
        printk(KERN_ALERT "an unstable state.\n");
    }

    write_cr0(original_cr0 & ~0x00010000);
    sys_call_table[SYSC] = (unsigned long *)original_call;
    write_cr0(original_cr0);

    msleep(1200);
    printk(KERN_ALERT "BYE BYE!");
}

module_init(syscall_start);
module_exit(syscall_end);

MODULE_LICENSE("GPL");