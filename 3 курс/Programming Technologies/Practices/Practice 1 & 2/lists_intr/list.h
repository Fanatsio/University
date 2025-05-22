#ifndef _LINUX_LIST_H
#define _LINUX_LIST_H

#include <stddef.h>

#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <limits.h>

struct list_head
{
    struct list_head *next;
};

typedef struct
{
    int data;
    struct list_head lists;
} item_t;

item_t *list_create(int);
void list_append(item_t *, int);
void list_destroy(item_t *);
size_t list_length(item_t *);
bool list_contains(item_t *, int);
size_t list_index(item_t *, int);
int *list_pop(item_t *);
void list_remove(item_t *, int);
void list_insert(item_t *, size_t, int);
void list_print_int(item_t *, FILE *);

//#########################################################
// edited copy from include/linux/list.h [v5.2]
// feel free for use

#define LIST_POISON1 ((void *)0x100)

/**
 * Returns a pointer to the container of this list element.
 *
 * Example:
 * struct foo* f;
 * f = container_of(&foo->entry, struct foo, entry);
 * assert(f == foo);
 *
 * @param ptr Pointer to the struct list_head.
 * @param type Data type of the list element.
 * @param member Member name of the struct list_head field in the list element.
 * @return A pointer to the data struct containing the list head.
 */
#ifndef container_of
#define container_of(ptr, type, member) \
    (type *)((char *)(ptr) - (char *)&((type *)0)->member)
#endif



#define LIST_HEAD_INIT(name) \
    {                        \
        &(name)              \
    }

#define LIST_HEAD(name) \
    struct list_head name = LIST_HEAD_INIT(name)

static inline void INIT_LIST_HEAD(struct list_head *list)
{
    list->next = NULL;
}

/*
 * Delete a list entry by making the prev/next entries
 * point to each other.
 *
 * This is only for internal list manipulation where we know
 * the prev/next entries already!
 */
static inline void __list_del(struct list_head *prev, struct list_head *next)
{
    prev->next = next;
}

/**
 * list_del - deletes entry from list.
 * @head: list head.
 * @entry: the element to delete from the list.
 * Note: list_empty() on entry does not return true after this, the entry is
 * in an undefined state.
 */
#ifndef CONFIG_DEBUG_LIST
static inline void __list_del_entry(struct list_head *prev, struct list_head *entry)
{
    __list_del(prev, entry->next);
}

static inline void list_del(struct list_head *prev, struct list_head *entry)
{
    __list_del(prev, entry->next);
    entry->next = LIST_POISON1;
}
#else
extern void __list_del_entry(struct list_head *prev, struct list_head *entry);
extern void list_del(struct list_head *prev, struct list_head *entry);
#endif

/**
 * list_is_last - tests whether @list is the last entry in list @head
 * @list: the entry to test
 * @head: the head of the list
 */
static inline int list_is_last(const struct list_head *list)
{
    return list->next == NULL;
}

/**
 * list_is_singular - tests whether a list has just one entry.
 * @head: the list to test.
 */
static inline int list_is_singular(const struct list_head *head)
{
    return head->next == NULL;
}

/**
 * list_entry - get the struct for this entry
 * @ptr:	the &struct list_head pointer.
 * @type:	the type of the struct this is embedded in.
 * @member:	the name of the list_struct within the struct.
 */
#define list_entry(ptr, type, member) \
    container_of(ptr, type, member)

/**
 * list_first_entry - get the first element from a list
 * @ptr:	the list head to take the element from.
 * @type:	the type of the struct this is embedded in.
 * @member:	the name of the list_struct within the struct.
 *
 * Note, that list is expected to be not empty.
 */
#define list_first_entry(ptr, type, member) \
    list_entry(ptr, type, member)

/**
 * list_next_entry - get the next element in list
 * @pos:	the type * to cursor
 * @member:	the name of the list_struct within the struct.
 */
#define list_next_entry(pos, member) \
    list_entry((pos)->member.next, __typeof__(*(pos)), member)

/**
 * list_for_each	-	iterate over a list
 * @pos:	the &struct list_head to use as a loop cursor.
 * @head:	the head for your list.
 */
#define list_for_each(pos, head) \
    for (pos = head; pos->next != NULL; pos = pos->next)

/**
 * list_for_each_entry	-	iterate over list of given type
 * @pos:	the type * to use as a loop cursor.
 * @head:	the head for your list.
 * @member:	the name of the list_struct within the struct.
 */
#define list_for_each_entry(pos, head, member)                   \
    for (pos = list_first_entry(head, __typeof__(*pos), member); \
         pos->member.next != NULL;                               \
         pos = list_next_entry(pos, member))

/*
 * Insert a new entry between two known consecutive entries.
 *
 * This is only for internal list manipulation where we know
 * the prev/next entries already!
 */
#ifndef CONFIG_DEBUG_LIST
static inline void __list_add(struct list_head *new,
                              struct list_head *prev,
                              struct list_head *next)
{
    new->next = next;
    prev->next = new;
}
#else
extern void __list_add(struct list_head *new,
                       struct list_head *prev,
                       struct list_head *next);
#endif

/**
 * list_add - add a new entry
 * @new: new entry to be added
 * @head: list head to add it after
 *
 * Insert a new entry after the specified head.
 * This is good for implementing stacks.
 */
static inline void list_add(struct list_head *new, struct list_head *prev, struct list_head *next)
{
    __list_add(new, prev, next);
}

/**
 * list_add_tail - add a new entry
 * @new: new entry to be added
 * @head: list head
 *
 * Insert a new entry before the specified head.
 * This is useful for implementing queues.
 */
static inline void list_add_tail(struct list_head *new, struct list_head *head)
{
    struct list_head *pos;
    list_for_each(pos, head);
    __list_add(new, pos, NULL);
}

#endif