#include <linux/module.h>
#include <linux/fs.h>
#include <linux/uaccess.h>
#include <linux/random.h>

#define DEVICE_NAME "random_device"

static int major_number;
static struct class *random_class = NULL;
static struct device *random_device = NULL;

static int random_open(struct inode *inode, struct file *file)
{
    printk(KERN_INFO "Random Device: opened\n");
    return 0;
}

static int random_release(struct inode *inode, struct file *file)
{
    printk(KERN_INFO "Random Device: closed\n");
    return 0;
}

static ssize_t random_read(struct file *file, char *buffer, size_t length, loff_t *offset)
{
    unsigned int rand_num;
    get_random_bytes(&rand_num, sizeof(rand_num));
    rand_num %= 100; // ограничиваем диапазон от 0 до 99

    if (copy_to_user(buffer, &rand_num, sizeof(rand_num))) {
        return -EFAULT;
    }

    printk(KERN_INFO "Random number generated: %d\n", rand_num);

    return sizeof(rand_num);
}

static struct file_operations fops = {
    .open = random_open,
    .release = random_release,
    .read = random_read,
};

static int __init random_device_init(void)
{
    major_number = register_chrdev(0, DEVICE_NAME, &fops);
    if (major_number < 0) {
        printk(KERN_ALERT "Random Device: failed to register a major number\n");
        return major_number;
    }

    random_class = class_create(THIS_MODULE, "random_class");
    if (IS_ERR(random_class)) {
        unregister_chrdev(major_number, DEVICE_NAME);
        printk(KERN_ALERT "Random Device: failed to register device class\n");
        return PTR_ERR(random_class);
    }

    random_device = device_create(random_class, NULL, MKDEV(major_number, 0), NULL, DEVICE_NAME);
    if (IS_ERR(random_device)) {
        class_destroy(random_class);
        unregister_chrdev(major_number, DEVICE_NAME);
        printk(KERN_ALERT "Random Device: failed to create the device\n");
        return PTR_ERR(random_device);
    }

    printk(KERN_INFO "Random Device: module loaded\n");
    return 0;
}

static void __exit random_device_exit(void)
{
    device_destroy(random_class, MKDEV(major_number, 0));
    class_unregister(random_class);
    class_destroy(random_class);
    unregister_chrdev(major_number, DEVICE_NAME);
    printk(KERN_INFO "Random Device: module unloaded\n");
}

module_init(random_device_init);
module_exit(random_device_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Dmitriy Rechuk");
MODULE_DESCRIPTION("Random Device Driver");
