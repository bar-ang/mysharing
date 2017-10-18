#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h>
#include <linux/sched.h> /* For current */
#include <linux/tty.h> /* For the tty declarations */
#include <linux/version.h> /* For LINUX_VERSION_CODE */
#include <linux/fs.h>
#include <linux/major.h>
#include <linux/termios.h>
#include <linux/workqueue.h>
#include <linux/tty_driver.h>
#include <linux/tty_ldisc.h>
#include <linux/mutex.h>
#include <linux/tty_flags.h>
#include <uapi/linux/tty.h>

MODULE_LICENSE("GPL");


static void print_string(char *str){
	struct tty_struct *my_tty;
	struct tty_struct *current = get_current_tty();
	my_tty = current->signal->tty;

	if(my_tty != NULL){
		((my_tty->driver)->write)(my_tty, str, strlen(str));
		((my_tty−>driver)−>write)(my_tty, "\015\012", 2);
	}
}

static int __init print_string_init(void)
{
	print_string("The module has been inserted.");
	return 0;
}
static void __exit print_string_exit(void)
{
	print_string("The module has been removed.");
}