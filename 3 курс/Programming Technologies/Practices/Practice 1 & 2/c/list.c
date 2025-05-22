#include "list.h"
#include <stdio.h>
#include <stdlib.h>

list_t *list_create(size_t size)
{
    list_t *list = malloc(sizeof(list_t));
    list->head = NULL;
    list->data_size = size;
    return list;
}


bool list_empty(list_t * list)
{
    return list->head == NULL;
}

bool list_contains(list_t * list, void * item)
{
    list_node_t *node = list->head;
    while (node != NULL)
    {
        if (!memcmp(node->data, item, list->data_size))
            return true;
        
        node = node->next;
    }
    return false;
}


size_t list_length(list_t* list)
{
    list_node_t *node = list->head;
    size_t length = 0;
    while (node != NULL)
    {
        length++;
        node = node->next;
    }
    return length;
}

size_t list_index(list_t * list, void * item)
{
    list_node_t *node = list->head;
    size_t index = 0;
    while (node != NULL)
    {
        if (!memcmp(node->data, item, list->data_size)) {
            return index;
        }
        index++;
        node = node->next;
    }
    return (size_t)-1;
}

void* list_pop(list_t* list)
{
    if (list->head == NULL)
    {
        return NULL;
    }

    if (list->head->next == NULL)
    {
        void *data = list->head->data;
        free(list->head);
        list->head = NULL;
        return data;
    }

    list_node_t *current = list->head;
    while (current->next->next != NULL)
    {
        current = current->next;
    }

    void *data = current->next->data; 
    free(current->next);
    current->next = NULL;

    return data;
}

void list_append(list_t* list, void *item) {
    list_node_t *new_node = (list_node_t *)malloc(sizeof(list_node_t));
    if (!new_node) {
        return;
    }

    new_node->data = (void *)malloc(list->data_size);
    if (!new_node->data) {
        free(new_node);
        return;
    }

    memcpy(new_node->data, item, list->data_size);
    new_node->next = NULL;

    if (list->head == NULL) {
    list->head = new_node;
    } else {
        list_node_t *node = list->head;
        while (node->next != NULL) {
            node = node->next;
        }
        node->next = new_node;
    }
}

void list_remove(list_t * list, void * item)
{
    list_node_t *node = list->head;
    list_node_t *prev = NULL;
    while (node != NULL)
    {
        if (!memcmp(node->data, item, list->data_size))
        {
            if (prev == NULL) {
                list->head = node->next;
            } else {
                prev->next = node->next;
            }
            free(node->data);
            free(node);
            return;
        }
        prev = node;
        node = node->next;
    }
}

void list_insert(list_t *list, size_t index, void *item)
{
    if (list == NULL || item == NULL)
        return;

    list_node_t *new_node = malloc(sizeof(list_node_t));
    if (new_node == NULL)
        return; 

    new_node->data = malloc(list->data_size);
    if (new_node->data == NULL)
    { 
        free(new_node);
        return;
    }
    memcpy(new_node->data, item, list->data_size);

    if (index == 0 || list->head == NULL)
    {
        new_node->next = list->head;
        list->head = new_node;
    }
    else
    {
        list_node_t *current = malloc(sizeof(list_node_t));
        current = list->head;
        size_t i = 0;
        while (current->next != NULL && i < index - 1)
        {
            current = current->next;
            i++;
        }

        new_node->next = current->next;
        current->next = new_node;
        current = NULL;
        free(current);
    }
}

void list_destroy(list_t * list)
{
    list_node_t *node = list->head;
    while (node != NULL)
    {
        list_node_t *next = node->next;
        free(node->data);
        free(node);
        
        node = next;
    }
    free(list);
}

void list_print_int(list_t *list, FILE *out)
{
    if (list->head == NULL)
    {
        fprintf(out, "NULL");
        return;
    }
    list_node_t *node = list->head;
    while (node != NULL)
    {
        fprintf(out, "(%d)", *(int *)node->data); 
        if (node->next != NULL)
        {
            fprintf(out, " -> "); 
        }
        else
        {
            fprintf(out, " -> NULL"); 
        }
        node = node->next;
    }
}