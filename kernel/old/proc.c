#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/types.h>
#include <linux/fs.h>
#include <asm/uaccess.h>
#include <linux/string.h>

#define procfs_name "helloworld"

void bprintk(char __user * buffer, char * str, int size);

/**
* This structure hold information about the /proc file
*
*/
struct proc_dir_entry *Our_Proc_File;

ssize_t procfile_read(struct file * file, char __user * buff, size_t size, loff_t * offset)
{
	char msg[100] = "WHELLO!";
	bprintk(buff,msg,100);
	return 100;
}

static struct file_operations fops = {
	.owner = THIS_MODULE,
	.read = procfile_read
};

int init_module()
{
	Our_Proc_File = proc_create(procfs_name, 0644, NULL, &fops);
	if (Our_Proc_File == NULL) {
		proc_remove(Our_Proc_File);
		printk(KERN_ALERT "Error: Could not initialize /proc/%s\n",
		procfs_name);
		return -ENOMEM;
	}


	printk(KERN_INFO "/proc/%s created\n", procfs_name);
	return 0;

}
void cleanup_module()
{
	proc_remove(Our_Proc_File);
	printk(KERN_INFO "/proc/%s removed\n", procfs_name);
}

void bprintk(char __user * buffer, char * str, int size){
	int i;
    for(i=0;i<size;i++){
    	put_user(*(str+i), buffer+i);
	}
}
