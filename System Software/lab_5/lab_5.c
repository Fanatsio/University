#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/random.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Rechuk Dmitriy");
MODULE_DESCRIPTION("Random Number Generator Kernel Module");

static int generate_random_integer(int min, int max) {
    return get_random_int() % (max - min + 1) + min;
}

static double generate_random_real(double min, double max) {
    unsigned int rand_val = get_random_bytes(&rand_val, sizeof(rand_val));
    return min + ((double)rand_val / UINT_MAX) * (max - min);
}

static int __init random_generator_init(void) {
    printk(KERN_INFO "Random Generator Module: Initialization\n");

    int random_int = generate_random_integer(1, 100);
    double random_real = generate_random_real(0.0, 1.0);

    printk(KERN_INFO "Random Integer: %d\n", random_int);
    printk(KERN_INFO "Random Real: %lf\n", random_real);

    return 0;
}

static void __exit random_generator_exit(void) {
    printk(KERN_INFO "Random Generator Module: Exiting\n");
}

module_init(random_generator_init);
module_exit(random_generator_exit);
