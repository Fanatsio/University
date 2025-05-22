#include "test-framework/unity.h"
#include "test-framework/unity_fixture.h"
#include "list.h"
#include <time.h>

#define TIMES_TO_RUN_RANDOM_TESTS 10ul

list_t *list_int = NULL;
list_t *list_dbl = NULL;

static void create_lists(void)
{
    list_int = list_create(sizeof(int));
    list_dbl = list_create(sizeof(double));
}

static void destroy_lists(void)
{
    if (list_int)
    {
        list_destroy(list_int);
        list_int = NULL;
    }
    if (list_dbl)
    {
        list_destroy(list_dbl);
        list_dbl = NULL;
    }
}


TEST_GROUP(Create);

TEST_SETUP(Create)
{
    create_lists();
}

TEST_TEAR_DOWN(Create)
{
    destroy_lists();
}

TEST(Create, CreateEmptyList)
{
    TEST_ASSERT_NOT_NULL(list_int);
    TEST_ASSERT_NULL(list_int->head);
    TEST_ASSERT_EQUAL_UINT64(list_int->data_size, sizeof(int));

    TEST_ASSERT_NOT_NULL(list_dbl);
    TEST_ASSERT_NULL(list_dbl->head);
    TEST_ASSERT_EQUAL_UINT64(list_dbl->data_size, sizeof(double));
}

TEST_GROUP_RUNNER(Create)
{
    RUN_TEST_CASE(Create, CreateEmptyList);
}

// destroy will be tested by memcheck, so we don't need to test it

TEST_GROUP(Append);

TEST_SETUP(Append)
{
    create_lists();
}

TEST_TEAR_DOWN(Append)
{
    destroy_lists();
}

TEST(Append, AppendToEmpty)
{
    // TEST_IGNORE();
    int i = 3;

    // make sure to malloc and memcpy data in append,
    // since i variable exists in function stackframe only
    list_append(list_int, &i);
    TEST_ASSERT_EQUAL_INT(i, *(int *)list_int->head->data);
    TEST_ASSERT_NULL(list_int->head->next);

    double d = 1.234;
    list_append(list_dbl, &d);
    TEST_ASSERT_EQUAL_DOUBLE(d, *(double *)list_dbl->head->data);
    TEST_ASSERT_NULL(list_dbl->head->next);

    // check on mem leaks, UAFs, and double frees here!
}

TEST(Append, AppendTwoTimes)
{
    // TEST_IGNORE();
    int i1 = 69;
    int i2 = 420;

    list_append(list_int, &i1);
    list_append(list_int, &i2);

    TEST_ASSERT_EQUAL_INT(i1, *(int *)list_int->head->data);
    TEST_ASSERT_NOT_NULL(list_int->head->next);

    TEST_ASSERT_EQUAL_INT(i2, *(int *)list_int->head->next->data);
    TEST_ASSERT_NULL(list_int->head->next->next);


    double d1 = 6.9;
    double d2 = 1.4e-20;

    list_append(list_dbl, &d1);
    list_append(list_dbl, &d2);

    TEST_ASSERT_EQUAL_DOUBLE(d1, *(double *)list_dbl->head->data);
    TEST_ASSERT_NOT_NULL(list_dbl->head->next);

    TEST_ASSERT_EQUAL_DOUBLE(d2, *(double *)list_dbl->head->next->data);
    TEST_ASSERT_NULL(list_dbl->head->next->next);
}


static int *get_n_rand_ints(size_t n)
{
    int *result = (int *)malloc(n * sizeof(int));
    for (size_t i = 0; i < n; i++)
        result[i] = rand() % 10000 - 5000;
    return result;
}

#define GET_DOUBLE_PLUS_MINUS_100 ((rand() *  200.0) / (double)RAND_MAX - 100.0)

static double *get_n_rand_doubles(size_t n)
{
    double *result = (double *)malloc(n * sizeof(double));
    for (size_t i = 0; i < n; i++)
        result[i] = GET_DOUBLE_PLUS_MINUS_100;
    return result;
}

#define GET_SIZE_T_FROM_100_TO_200 ((size_t)rand() % 100ul + 100ul)


TEST(Append, AppendNTimes)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("appending %zu ints", n);
    int *iarr = get_n_rand_ints(n);

    for (size_t i = 0; i < n; i++)
        list_append(list_int, iarr + i);    

    list_node_t *node = list_int->head;
    for (size_t i = 0; i < n; i++)
    {   
        TEST_ASSERT_EQUAL_INT(iarr[i], *(int *)node->data);
        node = node->next;
        if (i == n - 1)
            break;
        TEST_ASSERT_NOT_NULL(node);
    }
    TEST_ASSERT_NULL(node);
    free(iarr);

    n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("appending %zu doubles", n);
    double *darr = get_n_rand_doubles(n);

    for (size_t i = 0; i < n; i++)
    {
        list_append(list_dbl, darr + i);    
    }

    node = list_dbl->head;
    for (size_t i = 0; i < n; i++)
    {   
        TEST_ASSERT_EQUAL_DOUBLE(darr[i], *(double *)node->data);
        node = node->next;
        if (i == n - 1)
            break;
        TEST_ASSERT_NOT_NULL(node);
    }
    TEST_ASSERT_NULL(node);
    free(darr);
}

TEST_GROUP_RUNNER(Append)
{
    RUN_TEST_CASE(Append, AppendToEmpty);
    RUN_TEST_CASE(Append, AppendTwoTimes);
    RUN_TEST_CASE(Append, AppendNTimes);
}


TEST_GROUP(Length);

TEST_SETUP(Length)
{
    create_lists();
}

TEST_TEAR_DOWN(Length)
{
    destroy_lists();
}

TEST(Length, EmptyLength)
{
    // TEST_IGNORE();
    TEST_ASSERT_EQUAL_UINT64(0ul, list_length(list_int));
    TEST_ASSERT_EQUAL_UINT64(0ul, list_length(list_dbl));
}

TEST(Length, OneNodeLength)
{
    // TEST_IGNORE();
    int i = 1;
    list_append(list_int, &i);
    TEST_ASSERT_EQUAL_UINT64(1ul, list_length(list_int));

    double d = 1.1;
    list_append(list_dbl, &d);
    TEST_ASSERT_EQUAL_UINT64(1ul, list_length(list_dbl));
}

TEST(Length, TwoNodeLength)
{
    // TEST_IGNORE();
    int i = 1;
    list_append(list_int, &i);
    list_append(list_int, &i);
    TEST_ASSERT_EQUAL_UINT64(2ul, list_length(list_int));

    double d = 1.1;
    list_append(list_dbl, &d);
    list_append(list_dbl, &d);
    TEST_ASSERT_EQUAL_UINT64(2ul, list_length(list_dbl));
}

TEST(Length, NNodeLength)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("appending %zu ints", n);
    int iv = 1;
    for (size_t i = 0; i < n; i++)
        list_append(list_int, &iv);
    TEST_ASSERT_EQUAL_UINT64(n, list_length(list_int));
    
    n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("appending %zu doubles", n);
    double d = 1.1;
    for (size_t i = 0; i < n; i++)
        list_append(list_dbl, &d);
    TEST_ASSERT_EQUAL_UINT64(n, list_length(list_dbl));
}

TEST_GROUP_RUNNER(Length)
{
    RUN_TEST_CASE(Length, EmptyLength);
    RUN_TEST_CASE(Length, OneNodeLength);
    RUN_TEST_CASE(Length, TwoNodeLength);
    RUN_TEST_CASE(Length, NNodeLength);
}


TEST_GROUP(Empty);

TEST_SETUP(Empty)
{
    create_lists();
}

TEST_TEAR_DOWN(Empty)
{
    destroy_lists();
}

TEST(Empty, EmptyIsEmpty_NotEmptyAfterAppends)
{
    // TEST_IGNORE();
    TEST_ASSERT_TRUE(list_empty(list_int));
    int i = 1;
    list_append(list_int, &i);
    TEST_ASSERT_FALSE(list_empty(list_int));
    list_append(list_int, &i);
    TEST_ASSERT_FALSE(list_empty(list_int));
    list_append(list_int, &i);
    TEST_ASSERT_FALSE(list_empty(list_int));

    TEST_ASSERT_TRUE(list_empty(list_dbl));
    double d = 1.1;
    list_append(list_dbl, &d);
    TEST_ASSERT_FALSE(list_empty(list_dbl));
    list_append(list_dbl, &d);
    TEST_ASSERT_FALSE(list_empty(list_dbl));
    list_append(list_dbl, &d);
    TEST_ASSERT_FALSE(list_empty(list_dbl));
}

TEST_GROUP_RUNNER(Empty)
{
    RUN_TEST_CASE(Empty, EmptyIsEmpty_NotEmptyAfterAppends);
}


TEST_GROUP(Contains);

TEST_SETUP(Contains)
{
    create_lists();
}

TEST_TEAR_DOWN(Contains)
{
    destroy_lists();
}

TEST(Contains, EmptyListNotContainsAnything)
{
    // TEST_IGNORE();
    TEST_MESSAGE("This test can take pretty long time to finish...");
    for (int i = INT_MIN; i < INT_MAX; ++i)
        TEST_ASSERT_FALSE(list_contains(list_int, &i));

    double d;
    for (size_t i = 0; i < 10000; ++i)
    {
        d = GET_DOUBLE_PLUS_MINUS_100;
        TEST_ASSERT_FALSE(list_contains(list_dbl, &d));
    }
}

TEST(Contains, NotEmptyListContainsSomething)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    for (int i = -(int)n; i <= (int)n; i++)
    {
        TEST_ASSERT_FALSE(list_contains(list_int, &i));
        list_append(list_int, &i);
        TEST_ASSERT_TRUE(list_contains(list_int, &i));
    }

    n = GET_SIZE_T_FROM_100_TO_200;
    for (double i = -(double)n; i <= (double)n; i++)
    {
        TEST_ASSERT_FALSE(list_contains(list_dbl, &i));
        list_append(list_dbl, &i);
        TEST_ASSERT_TRUE(list_contains(list_dbl, &i));
    }
}


TEST_GROUP_RUNNER(Contains)
{
    RUN_TEST_CASE(Contains, EmptyListNotContainsAnything);
    RUN_TEST_CASE(Contains, NotEmptyListContainsSomething);
}


TEST_GROUP(Index);

TEST_SETUP(Index)
{
    create_lists();
}

TEST_TEAR_DOWN(Index)
{
    destroy_lists();
}

TEST(Index, EmptyListIndexSizeMax)
{
    // TEST_IGNORE();
    TEST_MESSAGE("This test can take pretty long time to finish...");
    // SIZE_MAX used as not found flag
    for (int i = INT_MIN; i < INT_MAX; ++i)
        TEST_ASSERT_EQUAL_UINT64(SIZE_MAX, list_index(list_int, &i));

    double d;
    for (size_t i = 0; i < 10000; ++i)
    {
        d = GET_DOUBLE_PLUS_MINUS_100;
        TEST_ASSERT_EQUAL_UINT64(SIZE_MAX, list_index(list_dbl, &d));
    }
}

TEST(Index, NotEmptyListIndex)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    int iv;
    for (size_t i = 0; i <= n; i++)
    {
        iv = (int)i;
        TEST_ASSERT_EQUAL_UINT64(SIZE_MAX, list_index(list_int, &i));
        list_append(list_int, &iv);
        TEST_ASSERT_EQUAL_UINT64(i, list_index(list_int, &i));
    }

    // index must use memcmp to avoid FP comparisons
    n = GET_SIZE_T_FROM_100_TO_200;
    double d;
    for (size_t i = 0; i <= n; i++)
    {
        d = (double)i;
        TEST_ASSERT_EQUAL_UINT64(SIZE_MAX, list_index(list_dbl, &d));
        list_append(list_dbl, &d);
        TEST_ASSERT_EQUAL_UINT64(i, list_index(list_dbl, &d));
    }
}

TEST(Index, IndexFirstOnly)
{
    // TEST_IGNORE();
    int i = 420;
    list_append(list_int, &i);
    list_append(list_int, &i);
    list_append(list_int, &i);
    TEST_ASSERT_EQUAL_UINT64(0ul, list_index(list_int, &i));

    double d = 6.9;
    list_append(list_dbl, &d);
    list_append(list_dbl, &d);
    list_append(list_dbl, &d);
    TEST_ASSERT_EQUAL_UINT64(0ul, list_index(list_dbl, &d));
}

TEST_GROUP_RUNNER(Index)
{
    RUN_TEST_CASE(Index, EmptyListIndexSizeMax);
    RUN_TEST_CASE(Index, NotEmptyListIndex);
    RUN_TEST_CASE(Index, IndexFirstOnly);
}


TEST_GROUP(Pop);

TEST_SETUP(Pop)
{
    create_lists();
}

TEST_TEAR_DOWN(Pop)
{
    destroy_lists();
}

TEST(Pop, PopFromEmptyList)
{
    // TEST_IGNORE();
    for (size_t i = 0; i < 10; ++i)
    {
        TEST_ASSERT_NULL(list_pop(list_int));
        TEST_ASSERT_NULL(list_pop(list_dbl));
    }
}

TEST(Pop, PopFromNonEmptySmall)
{
    // TEST_IGNORE();

    // list_pop must return malloc'ed\calloc'ed void ptr, so we need to free it after use
    int i = 69;
    list_append(list_int, &i);
    i = 420;
    list_append(list_int, &i);
    int *iactual = (int *)list_pop(list_int);
    TEST_ASSERT_EQUAL_INT(i, *iactual);
    free(iactual);
    iactual = (int *)list_pop(list_int);
    TEST_ASSERT_EQUAL_INT(69, *iactual);
    free(iactual);


    double d = 6.9;
    list_append(list_dbl, &d);
    d = 1.4e20;
    list_append(list_dbl, &d);
    
    double *dactual = (double *)list_pop(list_dbl);
    TEST_ASSERT_EQUAL_DOUBLE(d, *dactual);
    free(dactual);
    dactual = (double *)list_pop(list_dbl);
    TEST_ASSERT_EQUAL_DOUBLE(6.9, *dactual);
    free(dactual);
}

TEST(Pop, PopFromNonEmptyBig)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("appending and popping %zu ints", n);
    int *iarr = get_n_rand_ints(n);

    for (size_t i = 0; i < n; i++)
        list_append(list_int, iarr + i);    
    
    int *iactual;
    for (size_t i = n - 1; i > 0; i--)
    {   
        iactual = (int *)list_pop(list_int);
        TEST_ASSERT_EQUAL_INT(iarr[i], *iactual);
        free(iactual);
    }
    iactual = (int *)list_pop(list_int);
    TEST_ASSERT_EQUAL_INT(iarr[0], *iactual);
    free(iactual);
    free(iarr);

    TEST_ASSERT_TRUE(list_empty(list_int));

    n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("appending and popping %zu doubles", n);
    double *darr = get_n_rand_doubles(n);

    for (size_t i = 0; i < n; i++)
        list_append(list_dbl, darr + i);    
    
    double *dactual;
    for (size_t i = n - 1; i > 0; i--)
    {   
        dactual = (double *)list_pop(list_dbl);
        TEST_ASSERT_EQUAL_DOUBLE(darr[i], *dactual);
        free(dactual);
    }
    dactual = (double *)list_pop(list_dbl);
    TEST_ASSERT_EQUAL_DOUBLE(darr[0], *dactual);
    free(dactual);
    free(darr);

    TEST_ASSERT_TRUE(list_empty(list_dbl));

}

TEST_GROUP_RUNNER(Pop)
{
    RUN_TEST_CASE(Pop, PopFromEmptyList);
    RUN_TEST_CASE(Pop, PopFromNonEmptySmall);
    RUN_TEST_CASE(Pop, PopFromNonEmptyBig);
}


TEST_GROUP(Remove);

TEST_SETUP(Remove)
{
    create_lists();
}

TEST_TEAR_DOWN(Remove)
{
    destroy_lists();
}

TEST(Remove, RemoveFromEmptyList)
{
    // TEST_IGNORE();
    int i = 69;
    TEST_ASSERT_TRUE(list_empty(list_int));
    list_remove(list_int, &i);
    TEST_ASSERT_TRUE(list_empty(list_int));
    i = 420;
    list_remove(list_int, &i);
    TEST_ASSERT_TRUE(list_empty(list_int));

    double d = 6.9;
    TEST_ASSERT_TRUE(list_empty(list_int));
    list_remove(list_dbl, &d);
    TEST_ASSERT_TRUE(list_empty(list_dbl));
    d = 1.4e-20;
    list_remove(list_dbl, &d);
    TEST_ASSERT_TRUE(list_empty(list_dbl));
}

TEST(Remove, RemoveFromNonEmptyListMakesListEmpty)
{
    // TEST_IGNORE();
    int i[] = {69, 420};
    list_append(list_int, i);
    list_append(list_int, i+1);
    list_remove(list_int, i);
    TEST_ASSERT_FALSE(list_contains(list_int, i));
    TEST_ASSERT_EQUAL_UINT64(0ul, list_index(list_int, i+1));
    TEST_ASSERT_FALSE(list_empty(list_int));
    TEST_ASSERT_EQUAL_UINT64(1ul, list_length(list_int));
    list_remove(list_int, i+1);
    TEST_ASSERT_TRUE(list_empty(list_int));

    // remove must use memcmp to avoid FP comparisons
    double d[] = {6.9, 1.4e20};
    list_append(list_dbl, d);
    list_append(list_dbl, d+1);
    list_remove(list_dbl, d+1);
    TEST_ASSERT_FALSE(list_contains(list_dbl, d+1));
    TEST_ASSERT_EQUAL_UINT64(0ul, list_index(list_dbl, d));
    TEST_ASSERT_FALSE(list_empty(list_dbl));
    TEST_ASSERT_EQUAL_UINT64(1ul, list_length(list_dbl));
    list_remove(list_dbl, d);
    TEST_ASSERT_TRUE(list_empty(list_dbl));
}

TEST(Remove, RemoveHeadFromNonEmptyList)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("appending and removing %zu ints", n);
    int iv;
    for (size_t i = 0; i < n; i++)
    {
        iv = (int)i;
        list_append(list_int, &i);
    }

    for (size_t i = 0; i < n; i++)
    {
        iv = (int)i;
        list_remove(list_int, &iv);
        TEST_ASSERT_EQUAL_UINT64(n - i - 1, list_length(list_int));
        TEST_ASSERT_FALSE(list_contains(list_int, &iv));
        if (i == n - 1)
            break;
        iv++;
        TEST_ASSERT_EQUAL_UINT64(0ul, list_index(list_int, &iv));
    }
    TEST_ASSERT_TRUE(list_empty(list_int));
    
    n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("appending and removing %zu doubles", n);
    double d;
    for (size_t i = 0; i < n; i++)
    {
        d = (double)i;
        list_append(list_dbl, &d);
    }

    for (size_t i = 0; i < n; i++)
    {
        d = (double)i;
        list_remove(list_dbl, &d);
        TEST_ASSERT_EQUAL_UINT64(n - i - 1, list_length(list_dbl));
        TEST_ASSERT_FALSE(list_contains(list_dbl, &d));
        if (i == n - 1)
            break;
        d++;
        TEST_ASSERT_EQUAL_UINT64(0ul, list_index(list_dbl, &d));
    }
    TEST_ASSERT_TRUE(list_empty(list_dbl));
}

TEST(Remove, RemoveTailFromNonEmptyList)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("appending and removing %zu ints", n);
    int iv;
    for (size_t i = 0; i < n; i++)
    {
        iv = (int)i;
        list_append(list_int, &i);
    }

    for (size_t i = n - 1; i > 0; i--)
    {
        iv = (int)i;
        list_remove(list_int, &iv);
        TEST_ASSERT_FALSE(list_contains(list_int, &iv));
        TEST_ASSERT_EQUAL_UINT64(i, list_length(list_int));
        iv--;
        TEST_ASSERT_EQUAL_UINT64(i - 1ul, list_index(list_int, &iv));
    }
    list_remove(list_int, &iv);
    TEST_ASSERT_TRUE(list_empty(list_int));
    
    n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("appending and removing %zu doubles", n);
    double d;
    for (size_t i = 0; i < n; i++)
    {
        d = (double)i;
        list_append(list_dbl, &d);
    }

    for (size_t i = n - 1; i > 0; i--)
    {
        d = (double)i;
        list_remove(list_dbl, &d);
        TEST_ASSERT_FALSE(list_contains(list_dbl, &d));
        TEST_ASSERT_EQUAL_UINT64(i, list_length(list_dbl));
        d--;
        TEST_ASSERT_EQUAL_UINT64(i - 1ul, list_index(list_dbl, &d));
    }
    list_remove(list_dbl, &d);
    TEST_ASSERT_TRUE(list_empty(list_dbl));
}

TEST(Remove, RemoveRandom)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;   
    int iv;
    for (size_t i = 0; i < n; i++)
    {
        iv = (int)i;
        list_append(list_int, &iv);
    }

    int i_to_remove = rand() % ((int)n - 2) + 1;
    TEST_PRINTF("removing %d from list of %zu ints", i_to_remove, n);
    int i_b4 = i_to_remove - 1;
    int i_after = i_to_remove + 1;
    size_t idx = list_index(list_int, &i_to_remove);
    list_remove(list_int, &i_to_remove);
    TEST_ASSERT_FALSE(list_contains(list_int, &i_to_remove));
    TEST_ASSERT_EQUAL_UINT64(n - 1ul, list_length(list_int));
    TEST_ASSERT_EQUAL_UINT64(idx - 1ul, list_index(list_int, &i_b4));
    TEST_ASSERT_EQUAL_UINT64(idx, list_index(list_int, &i_after));

    n = GET_SIZE_T_FROM_100_TO_200;   
    double d;
    for (size_t i = 0; i < n; i++)
    {
        d = (double)i;
        list_append(list_dbl, &d);
    }

    double to_remove = (double)(rand() % ((int)n - 2) + 1);
    TEST_PRINTF("removing %lf from list of %zu doubles", to_remove, n);
    double b4 = to_remove - 1.0;
    double after = to_remove + 1.0;
    idx = list_index(list_dbl, &to_remove);
    list_remove(list_dbl, &to_remove);
    TEST_ASSERT_FALSE(list_contains(list_dbl, &to_remove));
    TEST_ASSERT_EQUAL_UINT64(n - 1ul, list_length(list_dbl));
    TEST_ASSERT_EQUAL_UINT64(idx - 1ul, list_index(list_dbl, &b4));
    TEST_ASSERT_EQUAL_UINT64(idx, list_index(list_dbl, &after));
}

TEST(Remove, RemoveFirstOnly)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;   
    int iv = 420;
    for (size_t i = 0; i < n; i++)
        list_append(list_int, &iv);
    list_remove(list_int, &iv);
    TEST_ASSERT_FALSE(list_empty(list_int));
    TEST_ASSERT_EQUAL_UINT64(n - 1ul, list_length(list_int));

    n = GET_SIZE_T_FROM_100_TO_200;   
    double d = 6.9;
    for (size_t i = 0; i < n; i++)
        list_append(list_dbl, &d);
    list_remove(list_dbl, &d);
    TEST_ASSERT_FALSE(list_empty(list_dbl));
    TEST_ASSERT_EQUAL_UINT64(n - 1ul, list_length(list_dbl));
}

TEST_GROUP_RUNNER(Remove)
{
    RUN_TEST_CASE(Remove, RemoveFromEmptyList);
    RUN_TEST_CASE(Remove, RemoveFromNonEmptyListMakesListEmpty);
    RUN_TEST_CASE(Remove, RemoveHeadFromNonEmptyList);
    RUN_TEST_CASE(Remove, RemoveTailFromNonEmptyList);
    for (size_t i = 0; i < TIMES_TO_RUN_RANDOM_TESTS; i++)
        RUN_TEST_CASE(Remove, RemoveRandom);
    RUN_TEST_CASE(Remove, RemoveFirstOnly);
}


TEST_GROUP(Insert);

TEST_SETUP(Insert)
{
    create_lists();
}

TEST_TEAR_DOWN(Insert)
{
    destroy_lists();
}

TEST(Insert, InsertToEmptyList)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    int iv;
    for (size_t i = 0; i < n; i++)
    {
        iv = (int)i + 69;
        list_insert(list_int, i, &iv);
        TEST_ASSERT_FALSE(list_empty(list_int));
        TEST_ASSERT_EQUAL_UINT64(1ul, list_length(list_int));
        TEST_ASSERT_EQUAL_INT(iv, *(int *)list_int->head->data);
        free(list_pop(list_int));
        TEST_ASSERT_TRUE(list_empty(list_int));
    }

    n = GET_SIZE_T_FROM_100_TO_200;
    double d;
    for (size_t i = 0; i < n; i++)
    {
        d = (double)i + 0.24;
        list_insert(list_dbl, i, &d);
        TEST_ASSERT_FALSE(list_empty(list_dbl));
        TEST_ASSERT_EQUAL_UINT64(1ul, list_length(list_dbl));
        TEST_ASSERT_EQUAL_DOUBLE(d, *(double *)list_dbl->head->data);
        free(list_pop(list_dbl));
        TEST_ASSERT_TRUE(list_empty(list_dbl));
    }
}

TEST(Insert, InsertToRandomIndexToNonEmtyList)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    int iv;
    for (size_t i = 0; i < n; i++)
    {
        iv = (int)i;
        list_append(list_int, &i);
    }
    iv = 420;
    size_t idx = (size_t)rand() % (n + n / 2ul);
    TEST_PRINTF("inserting on %zu index to list of %zu ints", idx, n);
    list_insert(list_int, idx, &iv);
    int b4, after;
    if (idx == 0)
    {
        after = 0;
        TEST_ASSERT_EQUAL_UINT64(1ul, list_index(list_int, &after));
        TEST_ASSERT_EQUAL_UINT64(idx, list_index(list_int, &iv));
    }
    else
        if (idx >= n)
        {
            b4 = (int)n - 1;
            TEST_ASSERT_EQUAL_UINT64(n - 1ul, list_index(list_int, &b4));
            TEST_ASSERT_EQUAL_UINT64(n, list_index(list_int, &iv));
        }
        else
        {
            b4 = (int)idx - 1;
            after = (int)idx;
            TEST_ASSERT_EQUAL_UINT64(idx - 1ul, list_index(list_int, &b4));
            TEST_ASSERT_EQUAL_UINT64(idx, list_index(list_int, &iv));
            TEST_ASSERT_EQUAL_UINT64(idx + 1ul, list_index(list_int, &after));
        }
    
    TEST_ASSERT_EQUAL_UINT64(n + 1ul, list_length(list_int));

    n = GET_SIZE_T_FROM_100_TO_200;
    double d;
    for (size_t i = 0; i < n; i++)
    {
        d = (double)i;
        list_append(list_dbl, &d);
    }
    d = 6969.0;
    idx = (size_t)rand() % (n + n / 2ul);
    TEST_PRINTF("inserting on %zu index to list of %zu doubles", idx, n);
    list_insert(list_dbl, idx, &d);
    double d_b4, d_after;
    if (idx == 0)
    {
        d_after = 0.0;
        TEST_ASSERT_EQUAL_UINT64(1ul, list_index(list_dbl, &d_after));
        TEST_ASSERT_EQUAL_UINT64(idx, list_index(list_dbl, &d));
    }
    else
        if (idx >= n)
        {
            d_b4 = (double)n - 1.0;
            TEST_ASSERT_EQUAL_UINT64(n - 1ul, list_index(list_dbl, &d_b4));
            TEST_ASSERT_EQUAL_UINT64(n, list_index(list_dbl, &d));
        }
        else
        {
            d_b4 = (double)idx - 1.0;
            d_after = (double)idx;
            TEST_ASSERT_EQUAL_UINT64(idx - 1ul, list_index(list_dbl, &d_b4));
            TEST_ASSERT_EQUAL_UINT64(idx, list_index(list_dbl, &d));
            TEST_ASSERT_EQUAL_UINT64(idx + 1ul, list_index(list_dbl, &d_after));
        }
    TEST_ASSERT_EQUAL_UINT64(n + 1ul, list_length(list_dbl));
}

TEST_GROUP_RUNNER(Insert)
{
    RUN_TEST_CASE(Insert, InsertToEmptyList);
    for (size_t i = 0; i < TIMES_TO_RUN_RANDOM_TESTS; i++)
        RUN_TEST_CASE(Insert, InsertToRandomIndexToNonEmtyList);
}


TEST_GROUP(Print);

FILE *f;
const char *filename = "test.txt";

TEST_SETUP(Print)
{
    create_lists();
}

TEST_TEAR_DOWN(Print)
{
    destroy_lists();
    remove(filename);
}

TEST(Print, PrintIntEmptyList)
{
    // TEST_IGNORE();
    f = fopen(filename, "w");
    list_print_int(list_int, f);
    fclose(f);
    f = fopen(filename, "r");
    char buf[64];
    if (fscanf(f, "%[^\n]", buf) == 0) {};
    fclose(f);
    TEST_ASSERT_EQUAL_STRING(buf, "NULL");
}

TEST(Print, PrintIntNonEmptyList)
{
    // TEST_IGNORE();
    int iarr[] = {69, 420, 351, 28980, 489};
    for (size_t i = 0; i < sizeof(iarr) / sizeof(int); i++)
        list_append(list_int, iarr + i);
    f = fopen(filename, "w");
    list_print_int(list_int, f);
    fclose(f);
    f = fopen(filename, "r");
    char buf[64];
    if (fscanf(f, "%[^\n]", buf) == 0) {};
    fclose(f);
    TEST_ASSERT_EQUAL_STRING(buf, "(69) -> (420) -> (351) -> (28980) -> (489) -> NULL");
}

TEST_GROUP_RUNNER(Print)
{
    RUN_TEST_CASE(Print, PrintIntEmptyList);
    RUN_TEST_CASE(Print, PrintIntNonEmptyList);
}


static void run_all_tests(void)
{
    RUN_TEST_GROUP(Create);
    RUN_TEST_GROUP(Append);
    RUN_TEST_GROUP(Length);
    RUN_TEST_GROUP(Empty);
    RUN_TEST_GROUP(Contains);
    RUN_TEST_GROUP(Index);
    RUN_TEST_GROUP(Pop);
    RUN_TEST_GROUP(Remove);
    RUN_TEST_GROUP(Insert);
    RUN_TEST_GROUP(Print);
}

int main(int argc, const char * argv[])
{   
    srand((unsigned int)time(NULL));
    return UnityMain(argc, argv, run_all_tests);
}
