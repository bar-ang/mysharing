#include <linux/kernel.h>       /* We're doing kernel work */
#include <linux/module.h>       /* Specifically, a module */
#include <linux/proc_fs.h>      /* Necessary because we use proc fs */
#include <linux/sched.h>        /* For putting processes to sleep and          waking them up */
#include <linux/signal.h>
#include <linux/uaccess.h>      /* for get_user and put_user */
#include <linux/unistd.h>
#include <linux/string.h>
#include <linux/syscalls.h>
#include <asm/paravirt.h>
#include <linux/moduleparam.h>

#define PROC_ENTRY_FILENAME "mystery"

static struct proc_dir_entry *procfile;
unsigned long **sys_call_table;


typedef struct task_struct * Task;

MODULE_LICENSE("GPL");


static int module_open(struct inode *inode, struct file *file)
{
    printk("it was %d who opened the file\n", current->pid);
	return 0;
}

int module_close(struct inode *inode, struct file *file)
{
    Task task = current;
    printk("it was %d who changed the folder\n", task->pid);
	return 0;
}




static struct file_operations fops = {
    .open = module_open,    /* called when the /proc file is opened */
    .release = module_close,        /* called when it's closed */
};

int init_module()
{

    printk("open offest: %ld",(long)sys_call_table[__NR_open]);

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

/*
 * Cleanup - unregister our file from /proc.  This could get dangerous if
 * there are still processes waiting in WaitQ, because they are inside our
 * open function, which will get unloaded. I'll explain how to avoid removal
 * of a kernel module in such a case in chapter 10.
 */
void cleanup_module()
{
    remove_proc_entry(PROC_ENTRY_FILENAME, NULL);
    printk(KERN_DEBUG "/proc/%s removed\n", PROC_ENTRY_FILENAME);
}
