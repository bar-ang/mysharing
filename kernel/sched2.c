/*
 *  sched.c - schedule a function to be called on every timer interrupt.
 *
 *  Copyright (C) 2001 by Peter Jay Salzman
 */


#include <linux/kernel.h>       /* We're doing kernel work */
#include <linux/module.h>       /* Specifically, a module */
#include <linux/proc_fs.h>      /* Necessary because we use the proc fs */
#include <linux/workqueue.h>    /* We schedule tasks here */
#include <linux/sched.h>        /* We need to put ourselves to sleep
                                   and wake up later */
#include <linux/init.h>         /* For __init and __exit */
#include <linux/interrupt.h>    /* For irqreturn_t */
#include <linux/uaccess.h>

struct proc_dir_entry *procfile;
#define PROC_ENTRY_FILENAME "sched2"
#define MY_WORK_QUEUE_NAME "WQsched.c"

MODULE_LICENSE("GPL");

/*
 * The number of times the timer interrupt has been called so far
 */
static int TimerIntrpt = 0;

static void intrpt_routine(struct work_struct *work);

static int die = 0;             /* set this to 1 for shutdown */

/*
 * The work queue structure for this task, from workqueue.h
 */
static struct workqueue_struct *my_workqueue;

static struct delayed_work Task;
static DECLARE_DELAYED_WORK(Task, intrpt_routine);


/*
 * This function will be called on every timer interrupt. Notice the void*
 * pointer - task functions can be used for more than one purpose, each time
 * getting a different parameter.
 */
static void intrpt_routine(struct work_struct *work)
{
    /*
     * Increment the counter
     */
    TimerIntrpt++;

    /*
     * If cleanup wants us to die
     */
    if (die == 0)
        queue_delayed_work(my_workqueue, &Task, 100);
}


static int readDone = 1;
ssize_t procfile_read(struct file *file,char *user_buffer,
                      size_t leng, loff_t * offset)
{
    if(readDone > 0){
        char msg[64];
        sprintf(msg,"It was %d ticks.\n", TimerIntrpt);
        if(copy_to_user(user_buffer,msg,strlen(msg)))
            return -EFAULT;
        readDone = 0;
        return strlen(msg);
    }else{
        readDone = 1;
        return 0;
    }
}

static const struct file_operations fops = {
    .owner = THIS_MODULE,
    .read  = procfile_read,
};

/*
 * Initialize the module - register the proc file
 */
int __init init_module()
{
    /*
     * Create our /proc file
     */
    procfile = proc_create(PROC_ENTRY_FILENAME, 0777, NULL, &fops);

    if (procfile == NULL) {
        remove_proc_entry(PROC_ENTRY_FILENAME, NULL);
        printk(KERN_ALERT "Error: Could not initialize /proc/%s\n",
               PROC_ENTRY_FILENAME);
        return -ENOMEM;
    }
    proc_set_size(procfile, 80);
    proc_set_user(procfile,  GLOBAL_ROOT_UID, GLOBAL_ROOT_GID);

    /*
     * Put the task in the work_timer task queue, so it will be executed at
     * next timer interrupt
     */
    my_workqueue = create_workqueue(MY_WORK_QUEUE_NAME);
    queue_delayed_work(my_workqueue, &Task, 100);

    printk(KERN_INFO "/proc/%s created\n", PROC_ENTRY_FILENAME);

    return 0;
}

/*
 * Cleanup
 */
void __exit cleanup_module()
{
    /*
     * Unregister our /proc file
     */
    remove_proc_entry(PROC_ENTRY_FILENAME, NULL);
    printk(KERN_INFO "/proc/%s removed\n", PROC_ENTRY_FILENAME);

    die = 1;                /* keep intrp_routine from queueing itself */
    cancel_delayed_work(&Task);     /* no "new ones" */
    flush_workqueue(my_workqueue);  /* wait till all "old ones" finished */
    destroy_workqueue(my_workqueue);

    /*
     * Sleep until intrpt_routine is called one last time. This is
     * necessary, because otherwise we'll deallocate the memory holding
     * intrpt_routine and Task while work_timer still references them.
     * Notice that here we don't allow signals to interrupt us.
     *
     * Since WaitQ is now not NULL, this automatically tells the interrupt
     * routine it's time to die.
     */
}