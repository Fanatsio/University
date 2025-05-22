#ifndef LINKED_LIST_H
#define LINKED_LIST_H

#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

typedef struct list_node_t
{
    void *data;
    struct list_node_t *next;
} list_node_t;

typedef struct
{
    list_node_t *head;
    size_t data_size;
} list_t;

list_t *list_create(size_t);
bool list_empty(list_t *);
bool list_contains(list_t *, void *);
size_t list_length(list_t*);
size_t list_index(list_t *, void *);
void *list_pop(list_t *);
void list_append(list_t*, void *);
void list_remove(list_t *, void *);
void list_insert(list_t *, size_t, void *);
void list_destroy(list_t *);
void list_print_int(list_t *, FILE *);

#endif