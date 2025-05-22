#ifndef BST_H
#define BST_H

#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>

typedef struct tree_node_t
{
    void *data;
    struct tree_node_t *left;
    struct tree_node_t *right;
} tree_node_t;

typedef struct
{
    tree_node_t *root;
    size_t data_size;
} bst_t;

typedef int (*comparator_func)(const void *, const void *);
typedef void (*print_datatype_func)(FILE *, void *);

bst_t *bst_create(size_t);
bool bst_empty(bst_t *);
bool bst_contains(bst_t *, void *, comparator_func);
size_t bst_length(bst_t *);
void bst_insert_node(bst_t *, void *, comparator_func);
void bst_delete_node(bst_t *, void *, comparator_func);
void bst_insert_array(bst_t *, size_t, void *, comparator_func);
void bst_destroy(bst_t *);
void bst_print_int(bst_t *, FILE *);
void *bst_preorder_traversal(bst_t *);
void *bst_inorder_traversal(bst_t *);
void *bst_postorder_traversal(bst_t *);
void *bst_level_order_traversal(bst_t *);
void bst_render(bst_t *, print_datatype_func, bool);

#endif