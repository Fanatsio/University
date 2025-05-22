#include "list.h"

item_t *list_create(int val) {
    item_t *new_item = (item_t *)malloc(sizeof(item_t));
    if (!new_item) {
        return NULL;
    }

    new_item->data = val;
    INIT_LIST_HEAD(&(new_item->lists));

    return new_item;
}

void list_append(item_t *head, int val) {
    item_t *new_item = list_create(val);
    if (!new_item) {
        return;
    }

    list_add_tail(&(new_item->lists), &(head->lists));
}

void list_destroy(item_t *head) {
    if (head == NULL) {
        return;
    }

    struct list_head *current = head->lists.next;
    struct list_head *temp;

    while (current != NULL) {
        temp = current->next;
        item_t *item = list_entry(current, item_t, lists);
        free(item);
        current = temp;
    }

    free(head);
}

size_t list_length(item_t *head) {
    if (head == NULL) {
        return 0;
    }

    size_t count = 1;

    item_t *pos;
    list_for_each_entry(pos, &(head->lists), lists) {
        count++;
    }

    return count;
}

bool list_contains(item_t *head, int value) {
    if (head == NULL) {
        return false;
    }

    item_t *pos;
    list_for_each_entry(pos, &(head->lists), lists) {
        if (pos->data == value) {
            return true;
        }
    }

    return pos->data == value;
}

size_t list_index(item_t *head, int value) {
    if (head == NULL) {
        return SIZE_MAX;
    }

    size_t index = 0;
    item_t *pos;

    list_for_each_entry(pos, &(head->lists), lists) {
        if (pos->data == value) {
            return index;
        }
        index++;
    }

    return pos->data == value ? index : SIZE_MAX;
}

int *list_pop(item_t *head) {
    if (head == NULL) {
        return NULL;
    }

    item_t *prev = NULL;
    item_t *pos = NULL;

    list_for_each_entry(pos, &(head->lists), lists) {
        prev = pos;
    }

    int *data = malloc(sizeof(int));
    if (!data) {
        return NULL;
    }

    *data = pos->data;

    if (prev) {
        list_del(&(prev->lists), &(pos->lists));
    } else {
        INIT_LIST_HEAD(&(head->lists));
    }

    free(pos);
    return data;
}

void list_remove(item_t *head, int value) {
    if (head == NULL) {
        return;
    }

    item_t *prev = NULL;
    item_t *pos = NULL;

    list_for_each_entry(pos, &(head->lists), lists) {
        if (pos->data == value) break;
        prev = pos;
    }

    if (pos == NULL || pos->data != value) {
        return;
    }

    if (list_is_singular(&(head->lists))) {
        free(head);
        return;
    }

    if (prev == NULL && pos->lists.next) {
        item_t *next = list_entry(pos->lists.next, item_t, lists);
        *head = *next;
        free(next);
    } else if (list_is_last(&(pos->lists))) {
        list_del(&(prev->lists), &(pos->lists));
    } else {
        prev->lists.next = pos->lists.next;
    }

    if (pos != head) {
        free(pos);
    }
}

void list_insert(item_t *head, size_t index, int value) {
    if (head == NULL) {
        return;
    }

    item_t *new_item = list_create(value);
    if (!new_item) {
        return;
    }

    item_t *pos = head;
    size_t current_index = 0;

    while (pos->lists.next != NULL && current_index < index) {
        pos = list_entry(pos->lists.next, item_t, lists);
        current_index++;
    }

    list_add(&(new_item->lists), &(pos->lists), pos->lists.next);
}

void list_print_int(item_t *head, FILE *f) {
    if (head == NULL) {
        fprintf(f, "NULL\n");
        return;
    }

    item_t *pos;
    list_for_each_entry(pos, &(head->lists), lists) {
        fprintf(f, "(%d) -> ", pos->data);
    }
    fprintf(f, "(%d) -> NULL\n", pos->data);
}
