/*
 *  print_string.c - Send output to the tty we're running on, regardless if it's
 *  through X11, telnet, etc.  We do this by printing the string to the tty
 *  associated with the current task.
 */
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h>
#include <linux/sched.h>        /* For current */
#include <linux/tty.h>          /* For the tty declarations */
#include <linux/version.h>      /* For LINUX_VERSION_CODE */

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Peter Jay Salzman");

static void printu(char *str)
{
    struct tty_struct *my_tty;
    const struct tty_operations *ttyops;
    /*
     * The tty for the current task
     */
    my_tty = get_current_tty();
    ttyops = my_tty->driver->ops;

    if (my_tty != NULL) {
        (ttyops->write) (my_tty, str, strlen(str));
        (ttyops->write) (my_tty, "\015\012", 2);
        //(ttyops->stop) (my_tty);
    }
}

static int __init print_string_init(void)
{
    printu("The module has been inserted.  Hello world!");
    return 0;
}

static void __exit print_string_exit(void)
{
    printu("The module has been removed.  Farewell world!");
}

module_init(print_string_init);
module_exit(print_string_exit);
