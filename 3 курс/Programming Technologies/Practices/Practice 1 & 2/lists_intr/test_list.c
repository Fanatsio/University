#include "test-framework/unity.h"
#include "test-framework/unity_fixture.h"
#include "list.h"
#include <time.h>

#define TIMES_TO_RUN_RANDOM_TESTS 10ul

item_t *list_int = NULL;

static void create_lists(int first_val)
{
    list_int = list_create(first_val);
}

static void destroy_lists(void)
{
    if (list_int)
    {
        list_destroy(list_int);
        list_int = NULL;
    }
}


TEST_GROUP(Create);

TEST_SETUP(Create)
{
    create_lists(INT_MAX);
}

TEST_TEAR_DOWN(Create)
{
    destroy_lists();
}

TEST(Create, CreateAlmostEmptyList)
{
    TEST_ASSERT_NOT_NULL(list_int);
    TEST_ASSERT_NULL(list_int->lists.next);
    TEST_ASSERT_EQUAL_UINT64(INT_MAX, list_int->data);
}

TEST_GROUP_RUNNER(Create)
{
    RUN_TEST_CASE(Create, CreateAlmostEmptyList);
}

// destroy will be tested by memcheck, so we don't need to test it

TEST_GROUP(Append);

TEST_SETUP(Append) {}

TEST_TEAR_DOWN(Append)
{
    destroy_lists();
}

TEST(Append, AppendToAlmostEmpty)
{
    // TEST_IGNORE();
    int i = 6;
    create_lists(3);

    list_append(list_int, i);

    TEST_ASSERT_EQUAL_INT(3, list_int->data);
    TEST_ASSERT_NOT_NULL(list_int->lists.next);
    item_t *pos = list_next_entry(list_first_entry(&(list_int->lists), item_t, lists), lists);
    TEST_ASSERT_EQUAL_INT(i, pos->data);
    TEST_ASSERT_NULL(list_int->lists.next->next);

    // check on mem leaks, UAFs, and double frees here!
}

TEST(Append, AppendTwoTimes)
{
    // TEST_IGNORE();
    int i1 = 69;
    int i2 = 420;

    create_lists(i1);
    list_append(list_int, i2);

    TEST_ASSERT_EQUAL_INT(i1, list_int->data);
    TEST_ASSERT_NOT_NULL(list_int->lists.next);

    item_t *pos = list_next_entry(list_first_entry(&(list_int->lists), item_t, lists), lists);
    TEST_ASSERT_EQUAL_INT(i2, pos->data);
    TEST_ASSERT_NOT_NULL(list_int->lists.next);
}


static int *get_n_rand_ints(size_t n)
{
    int *result = (int *)malloc(n * sizeof(int));
    for (size_t i = 0; i < n; i++)
        result[i] = rand() % 10000 - 5000;
    return result;
}


#define GET_SIZE_T_FROM_100_TO_200 ((size_t)rand() % 100ul + 100ul)


TEST(Append, AppendNTimes)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("appending %zu ints", n);
    int *iarr = get_n_rand_ints(n);

    create_lists(iarr[0]);

    for (size_t i = 1; i < n; i++)
        list_append(list_int, *(iarr + i));

    struct list_head *node = &(list_int->lists);
    for (size_t i = 0; i < n; i++)
    {
        item_t *pos = list_entry(node, item_t, lists);
        TEST_ASSERT_EQUAL_INT(iarr[i], pos->data);
        node = node->next;
        if (i == n - 1)
            break;
        TEST_ASSERT_NOT_NULL(node);
    }
    TEST_ASSERT_NULL(node);
    free(iarr);
}

TEST_GROUP_RUNNER(Append)
{
    RUN_TEST_CASE(Append, AppendToAlmostEmpty);
    RUN_TEST_CASE(Append, AppendTwoTimes);
    RUN_TEST_CASE(Append, AppendNTimes);
}


TEST_GROUP(Length);

TEST_SETUP(Length) {}

TEST_TEAR_DOWN(Length)
{
    destroy_lists();
}

TEST(Length, OneNodeLength)
{
    // TEST_IGNORE();
    int i = 1;
    create_lists(i);
    TEST_ASSERT_EQUAL_UINT64(1ul, list_length(list_int));
}

TEST(Length, TwoNodeLength)
{
    // TEST_IGNORE();
    int i = 1;
    create_lists(i);
    list_append(list_int, i);
    TEST_ASSERT_EQUAL_UINT64(2ul, list_length(list_int));
}

TEST(Length, NNodeLength)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("appending %zu ints", n);
    int iv = 1;
    create_lists(iv);
    for (size_t i = 1; i < n; i++)
        list_append(list_int, iv);
    TEST_ASSERT_EQUAL_UINT64(n, list_length(list_int));
}

TEST_GROUP_RUNNER(Length)
{
    RUN_TEST_CASE(Length, OneNodeLength);
    RUN_TEST_CASE(Length, TwoNodeLength);
    RUN_TEST_CASE(Length, NNodeLength);
}


TEST_GROUP(Contains);

TEST_SETUP(Contains) {}

TEST_TEAR_DOWN(Contains)
{
    destroy_lists();
}

TEST(Contains, NotEmptyListContainsSomething)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    int i = -(int)n;
    create_lists(-(int)n);
    TEST_ASSERT_TRUE(list_contains(list_int, i));
    for (i = -(int)n + 1; i <= (int)n; i++)
    {
        TEST_ASSERT_FALSE(list_contains(list_int, i));
        list_append(list_int, i);
        TEST_ASSERT_TRUE(list_contains(list_int, i));
    }
}


TEST_GROUP_RUNNER(Contains)
{
    RUN_TEST_CASE(Contains, NotEmptyListContainsSomething);
}


TEST_GROUP(Index);

TEST_SETUP(Index) {}

TEST_TEAR_DOWN(Index)
{
    destroy_lists();
}

TEST(Index, NotEmptyListIndex)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    int iv = 0;

    create_lists(iv);
    TEST_ASSERT_EQUAL_UINT64(iv, list_index(list_int, iv));
    for (int i = 1; i <= (int)n; i++)
    {
        iv = (int)i;
        TEST_ASSERT_EQUAL_UINT64(SIZE_MAX, list_index(list_int, i));
        list_append(list_int, iv);
        TEST_ASSERT_EQUAL_UINT64(i, list_index(list_int, i));
    }
}

TEST(Index, IndexFirstOnly)
{
    // TEST_IGNORE();
    int i = 420;
    create_lists(i);
    list_append(list_int, i);
    list_append(list_int, i);
    TEST_ASSERT_EQUAL_UINT64(0ul, list_index(list_int, i));
}

TEST_GROUP_RUNNER(Index)
{
    RUN_TEST_CASE(Index, NotEmptyListIndex);
    RUN_TEST_CASE(Index, IndexFirstOnly);
}


TEST_GROUP(Pop);

TEST_SETUP(Pop) {}

TEST_TEAR_DOWN(Pop) {}

TEST(Pop, PopFromNonEmptySmall)
{
    // TEST_IGNORE();

    // list_pop must return malloc'ed\calloc'ed void ptr, so we need to free it after use
    int i = 69;
    create_lists(i);
    i = 420;
    list_append(list_int, i);
    int *iactual = list_pop(list_int);
    TEST_ASSERT_EQUAL_INT(i, *iactual);
    free(iactual);
    iactual = list_pop(list_int);
    TEST_ASSERT_EQUAL_INT(69, *iactual);
    free(iactual);
}

TEST(Pop, PopFromNonEmptyBig)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("appending and popping %zu ints", n);
    int *iarr = get_n_rand_ints(n);

    create_lists(*iarr);
    for (size_t i = 1; i < n; i++)
        list_append(list_int, *(iarr + i));
    int *iactual;
    for (size_t i = n - 1; i > 0; i--)
    {
        iactual = list_pop(list_int);
        TEST_ASSERT_EQUAL_INT(iarr[i], *iactual);
        free(iactual);
    }
    iactual = list_pop(list_int);
    TEST_ASSERT_EQUAL_INT(iarr[0], *iactual);
    free(iactual);
    free(iarr);
}

TEST_GROUP_RUNNER(Pop)
{
    RUN_TEST_CASE(Pop, PopFromNonEmptySmall);
    RUN_TEST_CASE(Pop, PopFromNonEmptyBig);
}


TEST_GROUP(Remove);

TEST_SETUP(Remove) {}

TEST_TEAR_DOWN(Remove) {}

TEST(Remove, RemoveFromAlmostEmptyList)
{
    // TEST_IGNORE();
    create_lists(333);
    int i = 69;
    list_remove(list_int, i);
    i = 420;
    list_remove(list_int, i);
    destroy_lists();
}

TEST(Remove, RemoveFromNonEmptyListMakesListAlmostEmpty)
{
    // TEST_IGNORE();
    int i[] = {69, 420};
    create_lists(*i);
    list_append(list_int, *(i + 1));
    list_remove(list_int, *i);
    TEST_ASSERT_FALSE(list_contains(list_int, *i));
    TEST_ASSERT_EQUAL_UINT64(0ul, list_index(list_int, *(i + 1)));
    TEST_ASSERT_EQUAL_UINT64(1ul, list_length(list_int));
    list_remove(list_int, *(i + 1));
}

TEST(Remove, RemoveHeadFromNonEmptyList)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("appending and removing %zu ints", n);
    int iv = 0;
    create_lists(iv);
    for (size_t i = 1; i < n; i++)
    {
        iv = (int)i;
        list_append(list_int, iv);
    }

    for (size_t i = 0; i < n; i++)
    {
        iv = (int)i;
        list_remove(list_int, iv);
        if (i == n - 1)
            break;
        TEST_ASSERT_EQUAL_UINT64(n - i - 1, list_length(list_int));
        TEST_ASSERT_FALSE(list_contains(list_int, iv));
        iv++;
        TEST_ASSERT_EQUAL_UINT64(0ul, list_index(list_int, iv));
    }
}

TEST(Remove, RemoveTailFromNonEmptyList)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("appending and removing %zu ints", n);
    int iv = 0;
    create_lists(iv);
    for (size_t i = 1; i < n; i++)
    {
        iv = (int)i;
        list_append(list_int, iv);
    }

    for (size_t i = n - 1; i > 0; i--)
    {
        iv = (int)i;
        list_remove(list_int, iv);
        TEST_ASSERT_FALSE(list_contains(list_int, iv));
        TEST_ASSERT_EQUAL_UINT64(i, list_length(list_int));
        iv--;
        TEST_ASSERT_EQUAL_UINT64(i - 1ul, list_index(list_int, iv));
    }
    list_remove(list_int, iv);
}

TEST(Remove, RemoveRandom)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    int iv = 0;
    create_lists(iv);
    for (size_t i = 1; i < n; i++)
    {
        iv = (int)i;
        list_append(list_int, iv);
    }

    int i_to_remove = rand() % ((int)n - 2) + 1;
    TEST_PRINTF("removing %d from list of %zu ints", i_to_remove, n);
    int i_b4 = i_to_remove - 1;
    int i_after = i_to_remove + 1;
    size_t idx = list_index(list_int, i_to_remove);
    list_remove(list_int, i_to_remove);
    TEST_ASSERT_FALSE(list_contains(list_int, i_to_remove));
    TEST_ASSERT_EQUAL_UINT64(n - 1, list_length(list_int));
    TEST_ASSERT_EQUAL_UINT64(idx - 1, list_index(list_int, i_b4));
    TEST_ASSERT_EQUAL_UINT64(idx, list_index(list_int, i_after));
    destroy_lists();
}

TEST(Remove, RemoveFirstOnly)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    int iv = 420;
    create_lists(iv);
    for (size_t i = 1; i < n; i++)
        list_append(list_int, iv);
    list_remove(list_int, iv);
    TEST_ASSERT_EQUAL_UINT64(n - 1ul, list_length(list_int));
    destroy_lists();
}

TEST_GROUP_RUNNER(Remove)
{
    RUN_TEST_CASE(Remove, RemoveFromAlmostEmptyList);
    RUN_TEST_CASE(Remove, RemoveFromNonEmptyListMakesListAlmostEmpty);
    RUN_TEST_CASE(Remove, RemoveHeadFromNonEmptyList);
    RUN_TEST_CASE(Remove, RemoveTailFromNonEmptyList);
    for (size_t i = 0; i < TIMES_TO_RUN_RANDOM_TESTS; i++)
    RUN_TEST_CASE(Remove, RemoveRandom);
    RUN_TEST_CASE(Remove, RemoveFirstOnly);
}


TEST_GROUP(Insert);

TEST_SETUP(Insert) {}

TEST_TEAR_DOWN(Insert)
{
    destroy_lists();
}

TEST(Insert, InsertToAlmostEmptyList)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    int iv = 69;
    create_lists(iv);
    for (size_t i = 1; i < n; i++)
    {
        iv = (int)i + 69;
        list_insert(list_int, i, iv);
        TEST_ASSERT_EQUAL_UINT64(2ul, list_length(list_int));
        item_t *pos = list_next_entry(list_first_entry(&(list_int->lists), item_t, lists), lists);
        TEST_ASSERT_EQUAL_INT(iv, pos->data);
        free(list_pop(list_int));
        TEST_ASSERT_EQUAL_UINT64(1ul, list_length(list_int));
    }
}

TEST(Insert, InsertToRandomIndexToNonEmptyList)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    int iv;
    create_lists(0);
    for (size_t i = 1; i < n; i++)
    {
        iv = (int)i;
        list_append(list_int, iv);
    }
    iv = 420;
    size_t idx = (size_t)rand() % (n + n / 2ul);
    TEST_PRINTF("inserting on %zu index to list of %zu ints", idx, n);
    list_insert(list_int, idx, iv);
    int b4, after;
    if (idx == 0)
    {
        after = 0;
        TEST_ASSERT_EQUAL_UINT64(1ul, list_index(list_int, after));
        TEST_ASSERT_EQUAL_UINT64(idx, list_index(list_int, iv));
    }
    else if (idx >= n)
    {
        b4 = (int)n - 1;
        TEST_ASSERT_EQUAL_UINT64(n - 1ul, list_index(list_int, b4));
        TEST_ASSERT_EQUAL_UINT64(n, list_index(list_int, iv));
    }
    else
    {
        b4 = (int)idx - 1;
        after = (int)idx;
        TEST_ASSERT_EQUAL_UINT64(idx - 1ul, list_index(list_int, b4));
        TEST_ASSERT_EQUAL_UINT64(idx + 1ul, list_index(list_int, iv));
        TEST_ASSERT_EQUAL_UINT64(idx, list_index(list_int, after));
    }

    TEST_ASSERT_EQUAL_UINT64(n + 1ul, list_length(list_int));
}

TEST_GROUP_RUNNER(Insert)
{
    RUN_TEST_CASE(Insert, InsertToAlmostEmptyList);
    for (size_t i = 0; i < TIMES_TO_RUN_RANDOM_TESTS; i++)
    RUN_TEST_CASE(Insert, InsertToRandomIndexToNonEmptyList);
}


TEST_GROUP(Print);

FILE *f;
const char *filename = "test.txt";

TEST_SETUP(Print) {}

TEST_TEAR_DOWN(Print)
{
    destroy_lists();
    remove(filename);
}


TEST(Print, PrintIntNonEmptyList)
{
    // TEST_IGNORE();
    int iarr[] = {69, 420, 351, 28980, 489};
    create_lists(*iarr);
    for (size_t i = 1; i < sizeof(iarr) / sizeof(int); i++)
        list_append(list_int, *(iarr + i));
    f = fopen(filename, "w");
    list_print_int(list_int, f);
    fclose(f);
    f = fopen(filename, "r");
    char buf[64];
    if (fscanf(f, "%[^\n]", buf)==0){};
    fclose(f);
    TEST_ASSERT_EQUAL_STRING("(69) -> (420) -> (351) -> (28980) -> (489) -> NULL", buf);
}

TEST_GROUP_RUNNER(Print)
{
    RUN_TEST_CASE(Print, PrintIntNonEmptyList);
}


static void run_all_tests(void)
{
    RUN_TEST_GROUP(Create);
    RUN_TEST_GROUP(Append);
    RUN_TEST_GROUP(Length);
    RUN_TEST_GROUP(Contains);
    RUN_TEST_GROUP(Index);
    RUN_TEST_GROUP(Pop);
    RUN_TEST_GROUP(Remove);
    RUN_TEST_GROUP(Insert);
    RUN_TEST_GROUP(Print);
}

int main(int argc, const char *argv[])
{
    srand((unsigned int)time(NULL));
    return UnityMain(argc, argv, run_all_tests);
}