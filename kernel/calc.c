#include <linux/module.h>       /* Specifically, a module */
#include <linux/kernel.h>       /* We're doing kernel work */
#include <linux/proc_fs.h>      /* Necessary because we use the proc fs */
#include <linux/uaccess.h>      /* for copy_from_user */
#include <linux/string.h> 

#define PROCNAME "calculator"
#define MAXLEN 64

static long res;
static char op;
static struct proc_dir_entry *proc;

static int readonce;

ssize_t proc_read(struct file *filePointer,char *buffer,
                      size_t buffer_length, loff_t * offset);

static ssize_t proc_write(struct file *file, const char *buff,
                              size_t len, loff_t *off);

static const struct file_operations fops =
{
	.owner = THIS_MODULE,
	.write = proc_write,
	.read = proc_read
};

int init_module()
{
	proc = proc_create(PROCNAME,0777,NULL,&fops);
	if(proc == NULL){
		proc_remove(proc);
		printk("Error: could not create proc file.\n");
		return -ENOMEM;
	}
	printk("all set!\n");

	res = 0;
	op = '+';

	readonce = 0;

	return 0;
}

/**
 *This function is called when the module is unloaded
 *
 */
void cleanup_module()
{
	proc_remove(proc);
	printk("bye!\n");
}

static ssize_t proc_write(struct file *file, const char *buff,
                              size_t len, loff_t *off)
{
	char inputbuf[MAXLEN+1];
	long val;

	copy_from_user(inputbuf,buff,len);

	inputbuf[len] = '\0';


	if(inputbuf[0] == '+' ||
		inputbuf[0] == '-' ||
		inputbuf[0] == '*' ||
		inputbuf[0] == ':')
	{
		op = inputbuf[0];
	}
	else if(inputbuf[0] == 'c')
	{
		res = 0;
	}
	else
	{
		
		kstrtol(inputbuf,10,&val);
		switch(op){
			case '+':
				res += val;
				break;
			case '-':
				res -= val;
				break;
			case '*':
				res *= val;
				break;
			case ':':
				res /= val;
				break;
			default:
				res = val;
		}
		op = ';';
	}
	return len;
}

ssize_t proc_read(struct file *filePointer,char *buffer,
                      size_t buffer_length, loff_t * offset)
{
	char result[MAXLEN];

	sprintf(result, "%ld\n", res);

	copy_to_user(buffer,result,strlen(result));

	if(readonce == 0){
		readonce = 1;
		return strlen(result);
	}else{
		readonce = 0;
		return 0;
	}
}