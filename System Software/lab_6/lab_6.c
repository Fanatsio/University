#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define MAX_SIZE 100

int arr[MAX_SIZE];
int sorted[MAX_SIZE];

typedef struct {
    int start_index;
    int end_index;
} thread_args;

void merge(int start, int mid, int end) {
    int i, j, k;
    for (i = start; i <= end; i++)
        sorted[i] = arr[i];
    i = start;
    j = mid + 1;
    k = start;
    while (i <= mid && j <= end) {
        if (sorted[i] <= sorted[j]) {
            arr[k++] = sorted[i++];
        } else {
            arr[k++] = sorted[j++];
        }
    }
    while (i <= mid) {
        arr[k++] = sorted[i++];
    }
}

void *merge_sort(void *arg) {
    thread_args *args = (thread_args *)arg;
    int start = args->start_index;
    int end = args->end_index;
    if (start < end) {
        int mid = (start + end) / 2;
        thread_args left_args = {start, mid};
        thread_args right_args = {mid + 1, end};
        pthread_t left_thread, right_thread;
        pthread_create(&left_thread, NULL, merge_sort, &left_args);
        pthread_create(&right_thread, NULL, merge_sort, &right_args);
        pthread_join(left_thread, NULL);
        pthread_join(right_thread, NULL);
        merge(start, mid, end);
    }
    pthread_exit(NULL);
    return 0;
}

int main() {
    int size;
    srand(time(NULL));
    printf("Enter the number of elements in the array: ");
    scanf("%d", &size);
    for (int i = 0; i < size; i++) {
        arr[i] = rand() % 1000;
    }
    printf("The array is: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    thread_args args = {0, size - 1};
    pthread_t sort_thread;
    pthread_create(&sort_thread, NULL, merge_sort, &args);
    pthread_join(sort_thread, NULL);
    printf("\nThe sorted array is: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
    return 0;
}
