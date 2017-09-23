#undef __KERNEL__
#define __KERNEL__ /* We're part of the kernel */
#undef MODULE
#define MODULE     /* Not a permanent part, though. */

#include <linux/ioctl.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <asm/uaccess.h>
#include <linux/string.h>   /* for memset. NOTE - not string.h!*/

#define DEV_NAME "sniffdev"
#define MAJOR_NUM 255
#define SUCCESS 0
#define BUFFSIZE 32

MODULE_LICENSE("GPL");

int __init init_module(void);
void __exit cleanup_module(void);
static ssize_t device_read(struct file *filp, char *buffer, size_t length, loff_t * offset);
static int device_open(struct inode *inode, struct file *file);
//static int device_release(struct inode *inode, struct file *file);
//static ssize_t device_write(struct file *filp, const char *buff, size_t len, loff_t * off);

static struct file_operations fops = {
	.read = device_read,
	// .write = device_write,
	 .open = device_open
	// .release = device_release
};

int __init init_module(void){
	unsigned int rc = 0;
	rc = register_chrdev(MAJOR_NUM, DEV_NAME, &fops); /* our own file operations struct */
    /* 
     * Negative values signify an error 
     */
    if (rc < 0) {
        printk(KERN_ALERT "%s failed with %d\n",
               "Sorry, registering the character device ", MAJOR_NUM);
        return -1;
    }

	printk("Module is in\n");
	return 0;
}

void __exit cleanup_module(void){
	unregister_chrdev(MAJOR_NUM, DEV_NAME);
	printk("Module is out\n");
}


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

static int device_open(struct inode *inode, struct file *file)
{
    printk("You tried to open the device-file\n");

    return SUCCESS;
}


static ssize_t device_read(struct file *file, 
               char __user * buffer, 
               size_t length, 
               loff_t * offset)
{
	int i;
    char msg[BUFFSIZE] = "Whello!";

    for(i=0;i<BUFFSIZE;i++){
    	put_user(msg[i],buffer+i);
	}

    return BUFFSIZE; 
}

/*

static int device_release(struct inode *inode, struct file *file)
{
    printk("you touched me.\n");
    return SUCCESS;
}

static ssize_t device_read(struct file *file, 
               char __user * buffer, 
               size_t length, 
               loff_t * offset)
{
    //read doesnt really do anything (for now)
    printk("you touched me.\n");

    return 0; // invalid argument error
}

// somebody tries to write into our device file
static ssize_t
device_write(struct file *file,
         const char __user * buffer, size_t length, loff_t * offset)
{
  printk("you touched me.\n");
 
  // return the number of input characters used
  return 16;
}

*/