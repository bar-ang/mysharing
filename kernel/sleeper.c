
/*
 *  sleep.c - Set any one who tries to read the file to sleep
 *  all the sleeping proccess will wakeup when someone writes "hey, wake up!" into the proc file.
 */

#include <linux/kernel.h>       /* We're doing kernel work */
#include <linux/module.h>       /* Specifically, a module */
#include <linux/proc_fs.h>      /* Necessary because we use proc fs */
#include <linux/sched.h>        /* For putting processes to sleep and
                                   waking them up */
#include <linux/uaccess.h>      /* for get_user and put_user */


/*
 * Here we keep the last message received, to prove that we can process our
 * input
 */
#define MESSAGE_LENGTH 80
#define PROC_ENTRY_FILENAME "sleeper"

static struct proc_dir_entry *procfile;

DECLARE_WAIT_QUEUE_HEAD(WaitQ);

static int sleeping = 1;
static int count = 0;


//~~~~~~~~~~~~~~~~~~Reading & writing~~~~~~~~~~~~~~~~~~~~~~~
static ssize_t module_input(struct file *file,  /* The file itself */
                            const char *buf,    /* The buffer with input */
                            size_t length,      /* The buffer's length */
                            loff_t * offset)    /* offset to file - ignore */
{
	printk("wakeup!");
	sleeping = 0;
	wake_up(&WaitQ);

	return 1;
}

static ssize_t module_output(struct file *file, /* see include/linux/fs.h   */
                             char *buf, /* The buffer to put data to
                                           (in the user segment)    */
                             size_t len,        /* The length of the buffer */
                             loff_t * offset)
{
	printk("proccess go to sleep");
	while(sleeping>0){
		wait_event_interruptible(WaitQ, !sleeping);
		count++;
	}
	if(count > 0){
		count--;
	}else{
		sleeping = 1;
	}
	return 0;
}

//~~~~~~~~~~~~~~~~~~~~File operations~~~~~~~~~~~~~~~~~~~~~~~
static struct file_operations fops = {
    .read = module_output,  /* "read" from the file */
    .write = module_input,  /* "write" to the file */
};


//~~~~~~~~~~~~~~~~~~~Module init and cleaning~~~~~~~~~~~~~~~
int init_module()
{
    procfile = proc_create(PROC_ENTRY_FILENAME, 0777, NULL, &fops);
    if(procfile == NULL)
    {
        remove_proc_entry(PROC_ENTRY_FILENAME, NULL);
        printk(KERN_DEBUG "Error: Could not initialize /proc/%s\n", PROC_ENTRY_FILENAME);
        return -ENOMEM;
    }
    proc_set_size(procfile, 80);
    proc_set_user(procfile,  GLOBAL_ROOT_UID, GLOBAL_ROOT_GID);

    printk(KERN_INFO "/proc/test created\n");

    return 0;
}

void cleanup_module()
{
    remove_proc_entry(PROC_ENTRY_FILENAME, NULL);
    printk(KERN_DEBUG "/proc/%s removed\n", PROC_ENTRY_FILENAME);
}