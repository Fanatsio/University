#include "test-framework/unity.h"
#include "test-framework/unity_fixture.h"
#include "bst.h"
#include <time.h>

#define TIMES_TO_RUN_RANDOM_TESTS 10ul
#define GET_DOUBLE_PLUS_MINUS_100 ((rand() *  200.0) / (double)RAND_MAX - 100.0)
#define GET_SIZE_T_FROM_100_TO_200 ((size_t)rand() % 100ul + 100ul)

bst_t *tree_int = NULL;
bst_t *tree_dbl = NULL;

static void create_trees(void)
{
    tree_int = bst_create(sizeof(int));
    tree_dbl = bst_create(sizeof(double));
}

static void destroy_trees(void)
{
    if (tree_int)
    {
        bst_destroy(tree_int);
        tree_int = NULL;
    }
    if (tree_dbl)
    {
        bst_destroy(tree_dbl);
        tree_dbl = NULL;
    }
}

static int int_comparator(const void *a, const void *b)
{
    int int_a = *(const int*)a;
    int int_b = *(const int*)b;
    if (int_a < int_b)
        return -1;
    if (int_a > int_b)
        return 1;
    return 0;
}

static int double_comparator(const void *a, const void *b)
{
    double double_a = *(const double*)a;
    double double_b = *(const double*)b;
    if (!memcmp(a, b, sizeof(double)))
        return 0;
    if (double_a < double_b)
        return -1;
    if (double_a > double_b)
        return 1;
    return 0;
}

static int *get_n_rand_ints(size_t n)
{
    int *result = (int *)malloc(n * sizeof(int));
    for (size_t i = 0; i < n; i++)
        result[i] = rand() % 10000 - 5000;
    return result;
}

static double *get_n_rand_doubles(size_t n)
{
    double *result = (double *)malloc(n * sizeof(double));
    for (size_t i = 0; i < n; i++)
        result[i] = GET_DOUBLE_PLUS_MINUS_100;
    return result;
}


TEST_GROUP(Create);

TEST_SETUP(Create)
{
    create_trees();
}

TEST_TEAR_DOWN(Create)
{
    destroy_trees();
}

TEST(Create, CreateEmptyTrees)
{
    TEST_ASSERT_NOT_NULL(tree_int);
    TEST_ASSERT_NULL(tree_int->root);
    TEST_ASSERT_EQUAL_UINT64(tree_int->data_size, sizeof(int));

    TEST_ASSERT_NOT_NULL(tree_dbl);
    TEST_ASSERT_NULL(tree_dbl->root);
    TEST_ASSERT_EQUAL_UINT64(tree_dbl->data_size, sizeof(double));
}

TEST_GROUP_RUNNER(Create)
{
    RUN_TEST_CASE(Create, CreateEmptyTrees);
}


TEST_GROUP(Insert);

TEST_SETUP(Insert)
{
    create_trees();
}

TEST_TEAR_DOWN(Insert)
{
    destroy_trees();
}

TEST(Insert, InsertToEmpty)
{
    // TEST_IGNORE();
    int i = 3;
    bst_insert_node(tree_int, &i, int_comparator);
    TEST_ASSERT_NOT_NULL(tree_int->root);
    TEST_ASSERT_EQUAL_INT(i, *(int *)tree_int->root->data);
    TEST_ASSERT_NULL(tree_int->root->left);
    TEST_ASSERT_NULL(tree_int->root->right);

    double d = 1.234;
    bst_insert_node(tree_dbl, &d, double_comparator);
    TEST_ASSERT_NOT_NULL(tree_dbl->root);
    TEST_ASSERT_EQUAL_DOUBLE(d, *(double *)tree_dbl->root->data);
    TEST_ASSERT_NULL(tree_dbl->root->left);
    TEST_ASSERT_NULL(tree_dbl->root->right);
}

TEST(Insert, InsertRootLeft)
{
    // TEST_IGNORE();
    int i1 = 420;
    int i2 = 69;

    bst_insert_node(tree_int, &i1, int_comparator);
    bst_insert_node(tree_int, &i2, int_comparator);

    TEST_ASSERT_EQUAL_INT(i1, *(int *)tree_int->root->data);
    TEST_ASSERT_NULL(tree_int->root->right);
    TEST_ASSERT_NOT_NULL(tree_int->root->left);
    TEST_ASSERT_EQUAL_INT(i2, *(int *)tree_int->root->left->data);
    TEST_ASSERT_NULL(tree_int->root->left->left);
    TEST_ASSERT_NULL(tree_int->root->left->right);


    double d1 = 6.9;
    double d2 = 1.4e-20;

    bst_insert_node(tree_dbl, &d1, double_comparator);
    bst_insert_node(tree_dbl, &d2, double_comparator);

    TEST_ASSERT_EQUAL_DOUBLE(d1, *(double *)tree_dbl->root->data);
    TEST_ASSERT_NULL(tree_dbl->root->right);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->left);
    TEST_ASSERT_EQUAL_DOUBLE(d2, *(double *)tree_dbl->root->left->data);
    TEST_ASSERT_NULL(tree_dbl->root->left->left);
    TEST_ASSERT_NULL(tree_dbl->root->left->right);
}

TEST(Insert, InsertRootRight)
{
    // TEST_IGNORE();
    int i1 = 69;
    int i2 = 420;

    bst_insert_node(tree_int, &i1, int_comparator);
    bst_insert_node(tree_int, &i2, int_comparator);

    TEST_ASSERT_EQUAL_INT(i1, *(int *)tree_int->root->data);
    TEST_ASSERT_NULL(tree_int->root->left);
    TEST_ASSERT_NOT_NULL(tree_int->root->right);
    TEST_ASSERT_EQUAL_INT(i2, *(int *)tree_int->root->right->data);
    TEST_ASSERT_NULL(tree_int->root->right->left);
    TEST_ASSERT_NULL(tree_int->root->right->right);


    double d1 = 1.4e-20;
    double d2 = 6.9;

    bst_insert_node(tree_dbl, &d1, double_comparator);
    bst_insert_node(tree_dbl, &d2, double_comparator);

    TEST_ASSERT_EQUAL_DOUBLE(d1, *(double *)tree_dbl->root->data);
    TEST_ASSERT_NULL(tree_dbl->root->left);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->right);
    TEST_ASSERT_EQUAL_DOUBLE(d2, *(double *)tree_dbl->root->right->data);
    TEST_ASSERT_NULL(tree_dbl->root->right->left);
    TEST_ASSERT_NULL(tree_dbl->root->right->right);
}

TEST(Insert, InsertRootLeftLeft)
{
    // TEST_IGNORE();
    int i1 = 3;
    int i2 = 2;
    int i3 = 1;
 
    bst_insert_node(tree_int, &i1, int_comparator);
    bst_insert_node(tree_int, &i2, int_comparator);
    bst_insert_node(tree_int, &i3, int_comparator);

    TEST_ASSERT_EQUAL_INT(i1, *(int *)tree_int->root->data);
    TEST_ASSERT_NOT_NULL(tree_int->root->left);
    TEST_ASSERT_NULL(tree_int->root->right);
    TEST_ASSERT_EQUAL_INT(i2, *(int *)tree_int->root->left->data);
    TEST_ASSERT_NOT_NULL(tree_int->root->left->left);
    TEST_ASSERT_NULL(tree_int->root->left->right);
    TEST_ASSERT_EQUAL_INT(i3, *(int *)tree_int->root->left->left->data);
    TEST_ASSERT_NULL(tree_int->root->left->left->left);
    TEST_ASSERT_NULL(tree_int->root->left->left->right);


    double d1 = 6.9;
    double d2 = 0.42;
    double d3 = 1.4e-20;

    bst_insert_node(tree_dbl, &d1, double_comparator);
    bst_insert_node(tree_dbl, &d2, double_comparator);
    bst_insert_node(tree_dbl, &d3, double_comparator);

    TEST_ASSERT_EQUAL_DOUBLE(d1, *(double *)tree_dbl->root->data);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->left);
    TEST_ASSERT_NULL(tree_dbl->root->right);
    TEST_ASSERT_EQUAL_DOUBLE(d2, *(double *)tree_dbl->root->left->data);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->left->left);
    TEST_ASSERT_NULL(tree_dbl->root->left->right);
    TEST_ASSERT_EQUAL_DOUBLE(d3, *(double *)tree_dbl->root->left->left->data);
    TEST_ASSERT_NULL(tree_dbl->root->left->left->left);
    TEST_ASSERT_NULL(tree_dbl->root->left->left->right);
}


TEST(Insert, InsertRootLeftRight)
{
    // TEST_IGNORE();
    int i1 = 3;
    int i2 = 1;
    int i3 = 2;
 
    bst_insert_node(tree_int, &i1, int_comparator);
    bst_insert_node(tree_int, &i2, int_comparator);
    bst_insert_node(tree_int, &i3, int_comparator);

    TEST_ASSERT_EQUAL_INT(i1, *(int *)tree_int->root->data);
    TEST_ASSERT_NOT_NULL(tree_int->root->left);
    TEST_ASSERT_NULL(tree_int->root->right);
    TEST_ASSERT_EQUAL_INT(i2, *(int *)tree_int->root->left->data);
    TEST_ASSERT_NOT_NULL(tree_int->root->left->right);
    TEST_ASSERT_NULL(tree_int->root->left->left);
    TEST_ASSERT_EQUAL_INT(i3, *(int *)tree_int->root->left->right->data);
    TEST_ASSERT_NULL(tree_int->root->left->right->left);
    TEST_ASSERT_NULL(tree_int->root->left->right->right);


    double d1 = 6.9;
    double d2 = 1.4e-20;
    double d3 = 0.42;

    bst_insert_node(tree_dbl, &d1, double_comparator);
    bst_insert_node(tree_dbl, &d2, double_comparator);
    bst_insert_node(tree_dbl, &d3, double_comparator);

    TEST_ASSERT_EQUAL_DOUBLE(d1, *(double *)tree_dbl->root->data);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->left);
    TEST_ASSERT_NULL(tree_dbl->root->right);
    TEST_ASSERT_EQUAL_DOUBLE(d2, *(double *)tree_dbl->root->left->data);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->left->right);
    TEST_ASSERT_NULL(tree_dbl->root->left->left);
    TEST_ASSERT_EQUAL_DOUBLE(d3, *(double *)tree_dbl->root->left->right->data);
    TEST_ASSERT_NULL(tree_dbl->root->left->right->left);
    TEST_ASSERT_NULL(tree_dbl->root->left->right->right);
}


TEST(Insert, InsertBalancedLeftFirst)
{
    // TEST_IGNORE();
    int i1 = 2;
    int i2 = 1;
    int i3 = 3;
 
    bst_insert_node(tree_int, &i1, int_comparator);
    bst_insert_node(tree_int, &i2, int_comparator);
    bst_insert_node(tree_int, &i3, int_comparator);

    TEST_ASSERT_EQUAL_INT(i1, *(int *)tree_int->root->data);
    TEST_ASSERT_NOT_NULL(tree_int->root->left);
    TEST_ASSERT_NOT_NULL(tree_int->root->right);
    TEST_ASSERT_EQUAL_INT(i2, *(int *)tree_int->root->left->data);
    TEST_ASSERT_NULL(tree_int->root->left->left);
    TEST_ASSERT_NULL(tree_int->root->left->right);
    TEST_ASSERT_EQUAL_INT(i3, *(int *)tree_int->root->right->data);
    TEST_ASSERT_NULL(tree_int->root->right->left);
    TEST_ASSERT_NULL(tree_int->root->right->left);


    double d1 = 0.42;
    double d2 = 1.4e-20;
    double d3 = 6.9;

    bst_insert_node(tree_dbl, &d1, double_comparator);
    bst_insert_node(tree_dbl, &d2, double_comparator);
    bst_insert_node(tree_dbl, &d3, double_comparator);

    TEST_ASSERT_EQUAL_DOUBLE(d1, *(double *)tree_dbl->root->data);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->left);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->right);
    TEST_ASSERT_EQUAL_DOUBLE(d2, *(double *)tree_dbl->root->left->data);
    TEST_ASSERT_NULL(tree_dbl->root->left->left);
    TEST_ASSERT_NULL(tree_dbl->root->left->right);
    TEST_ASSERT_EQUAL_DOUBLE(d3, *(double *)tree_dbl->root->right->data);
    TEST_ASSERT_NULL(tree_dbl->root->right->left);
    TEST_ASSERT_NULL(tree_dbl->root->right->left);
}

TEST(Insert, InsertBalancedRightFirst)
{
    // TEST_IGNORE();
    int i1 = 2;
    int i2 = 3;
    int i3 = 1;
 
    bst_insert_node(tree_int, &i1, int_comparator);
    bst_insert_node(tree_int, &i2, int_comparator);
    bst_insert_node(tree_int, &i3, int_comparator);

    TEST_ASSERT_EQUAL_INT(i1, *(int *)tree_int->root->data);
    TEST_ASSERT_NOT_NULL(tree_int->root->left);
    TEST_ASSERT_NOT_NULL(tree_int->root->right);
    TEST_ASSERT_EQUAL_INT(i2, *(int *)tree_int->root->right->data);
    TEST_ASSERT_NULL(tree_int->root->left->left);
    TEST_ASSERT_NULL(tree_int->root->left->right);
    TEST_ASSERT_EQUAL_INT(i3, *(int *)tree_int->root->left->data);
    TEST_ASSERT_NULL(tree_int->root->right->left);
    TEST_ASSERT_NULL(tree_int->root->right->left);


    double d1 = 0.42;
    double d2 = 6.9;
    double d3 = 1.4e-20;

    bst_insert_node(tree_dbl, &d1, double_comparator);
    bst_insert_node(tree_dbl, &d2, double_comparator);
    bst_insert_node(tree_dbl, &d3, double_comparator);

    TEST_ASSERT_EQUAL_DOUBLE(d1, *(double *)tree_dbl->root->data);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->left);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->right);
    TEST_ASSERT_EQUAL_DOUBLE(d2, *(double *)tree_dbl->root->right->data);
    TEST_ASSERT_NULL(tree_dbl->root->left->left);
    TEST_ASSERT_NULL(tree_dbl->root->left->right);
    TEST_ASSERT_EQUAL_DOUBLE(d3, *(double *)tree_dbl->root->left->data);
    TEST_ASSERT_NULL(tree_dbl->root->right->left);
    TEST_ASSERT_NULL(tree_dbl->root->right->left);
}


TEST(Insert, InsertRootRightLeft)
{
    // TEST_IGNORE();
    int i1 = 1;
    int i2 = 3;
    int i3 = 2;
 
    bst_insert_node(tree_int, &i1, int_comparator);
    bst_insert_node(tree_int, &i2, int_comparator);
    bst_insert_node(tree_int, &i3, int_comparator);

    TEST_ASSERT_EQUAL_INT(i1, *(int *)tree_int->root->data);
    TEST_ASSERT_NOT_NULL(tree_int->root->right);
    TEST_ASSERT_NULL(tree_int->root->left);
    TEST_ASSERT_EQUAL_INT(i2, *(int *)tree_int->root->right->data);
    TEST_ASSERT_NOT_NULL(tree_int->root->right->left);
    TEST_ASSERT_NULL(tree_int->root->right->right);
    TEST_ASSERT_EQUAL_INT(i3, *(int *)tree_int->root->right->left->data);
    TEST_ASSERT_NULL(tree_int->root->right->left->left);
    TEST_ASSERT_NULL(tree_int->root->right->left->right);


    double d1 = 1.4e-20;
    double d2 = 6.9;
    double d3 = 0.42;

    bst_insert_node(tree_dbl, &d1, double_comparator);
    bst_insert_node(tree_dbl, &d2, double_comparator);
    bst_insert_node(tree_dbl, &d3, double_comparator);

    TEST_ASSERT_EQUAL_DOUBLE(d1, *(double *)tree_dbl->root->data);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->right);
    TEST_ASSERT_NULL(tree_dbl->root->left);
    TEST_ASSERT_EQUAL_DOUBLE(d2, *(double *)tree_dbl->root->right->data);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->right->left);
    TEST_ASSERT_NULL(tree_dbl->root->right->right);
    TEST_ASSERT_EQUAL_DOUBLE(d3, *(double *)tree_dbl->root->right->left->data);
    TEST_ASSERT_NULL(tree_dbl->root->right->left->left);
    TEST_ASSERT_NULL(tree_dbl->root->right->left->right);
}

TEST(Insert, InsertRootRightRight)
{
    // TEST_IGNORE();
    int i1 = 1;
    int i2 = 2;
    int i3 = 3;
 
    bst_insert_node(tree_int, &i1, int_comparator);
    bst_insert_node(tree_int, &i2, int_comparator);
    bst_insert_node(tree_int, &i3, int_comparator);

    TEST_ASSERT_EQUAL_INT(i1, *(int *)tree_int->root->data);
    TEST_ASSERT_NOT_NULL(tree_int->root->right);
    TEST_ASSERT_NULL(tree_int->root->left);
    TEST_ASSERT_EQUAL_INT(i2, *(int *)tree_int->root->right->data);
    TEST_ASSERT_NOT_NULL(tree_int->root->right->right);
    TEST_ASSERT_NULL(tree_int->root->right->left);
    TEST_ASSERT_EQUAL_INT(i3, *(int *)tree_int->root->right->right->data);
    TEST_ASSERT_NULL(tree_int->root->right->right->left);
    TEST_ASSERT_NULL(tree_int->root->right->right->right);


    double d1 = 1.4e-20;
    double d2 = 0.42;
    double d3 = 6.9;

    bst_insert_node(tree_dbl, &d1, double_comparator);
    bst_insert_node(tree_dbl, &d2, double_comparator);
    bst_insert_node(tree_dbl, &d3, double_comparator);

    TEST_ASSERT_EQUAL_DOUBLE(d1, *(double *)tree_dbl->root->data);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->right);
    TEST_ASSERT_NULL(tree_dbl->root->left);
    TEST_ASSERT_EQUAL_DOUBLE(d2, *(double *)tree_dbl->root->right->data);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->right->right);
    TEST_ASSERT_NULL(tree_dbl->root->right->left);
    TEST_ASSERT_EQUAL_DOUBLE(d3, *(double *)tree_dbl->root->right->right->data);
    TEST_ASSERT_NULL(tree_dbl->root->right->right->left);
    TEST_ASSERT_NULL(tree_dbl->root->right->right->right);
}

TEST(Insert, Insert5Nodes)
{
    // TEST_IGNORE();
    int arr_int[] = {3, 2, 4, 1, 5};
    double arr_dbl[] = {5.5, 3.2, 7.1, 2.1, 8.3};

    for (size_t i = 0ul; i < 5ul; i++)
    {
        bst_insert_node(tree_int, arr_int + i, int_comparator);
        bst_insert_node(tree_dbl, arr_dbl + i, double_comparator);
    }

    TEST_ASSERT_EQUAL_INT(arr_int[0], *(int *)tree_int->root->data);
    TEST_ASSERT_NOT_NULL(tree_int->root->left);
    TEST_ASSERT_NOT_NULL(tree_int->root->right);
    TEST_ASSERT_EQUAL_INT(arr_int[1], *(int *)tree_int->root->left->data);
    TEST_ASSERT_EQUAL_INT(arr_int[3], *(int *)tree_int->root->left->left->data);
    TEST_ASSERT_NULL(tree_int->root->left->left->left);
    TEST_ASSERT_NULL(tree_int->root->left->left->right);
    TEST_ASSERT_NULL(tree_int->root->left->right);
    TEST_ASSERT_EQUAL_INT(arr_int[2], *(int *)tree_int->root->right->data);
    TEST_ASSERT_EQUAL_INT(arr_int[4], *(int *)tree_int->root->right->right->data);
    TEST_ASSERT_NULL(tree_int->root->right->right->left);
    TEST_ASSERT_NULL(tree_int->root->right->right->right);


    TEST_ASSERT_EQUAL_DOUBLE(arr_dbl[0], *(double *)tree_dbl->root->data);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->left);
    TEST_ASSERT_NOT_NULL(tree_dbl->root->right);
    TEST_ASSERT_EQUAL_DOUBLE(arr_dbl[1], *(double *)tree_dbl->root->left->data);
    TEST_ASSERT_EQUAL_DOUBLE(arr_dbl[3], *(double *)tree_dbl->root->left->left->data);
    TEST_ASSERT_NULL(tree_dbl->root->left->left->left);
    TEST_ASSERT_NULL(tree_dbl->root->left->left->right);
    TEST_ASSERT_NULL(tree_dbl->root->left->right);
    TEST_ASSERT_EQUAL_DOUBLE(arr_dbl[2], *(double *)tree_dbl->root->right->data);
    TEST_ASSERT_EQUAL_DOUBLE(arr_dbl[4], *(double *)tree_dbl->root->right->right->data);
    TEST_ASSERT_NULL(tree_dbl->root->right->right->left);
    TEST_ASSERT_NULL(tree_dbl->root->right->right->right);
}

TEST_GROUP_RUNNER(Insert)
{
    RUN_TEST_CASE(Insert, InsertToEmpty);
    RUN_TEST_CASE(Insert, InsertRootLeft);
    RUN_TEST_CASE(Insert, InsertRootRight);
    RUN_TEST_CASE(Insert, InsertRootLeftLeft);
    RUN_TEST_CASE(Insert, InsertRootLeftRight);
    RUN_TEST_CASE(Insert, InsertBalancedLeftFirst);
    RUN_TEST_CASE(Insert, InsertBalancedRightFirst);
    RUN_TEST_CASE(Insert, InsertRootRightLeft);
    RUN_TEST_CASE(Insert, InsertRootRightRight);
    RUN_TEST_CASE(Insert, Insert5Nodes);
}


TEST_GROUP(Length);

TEST_SETUP(Length)
{
    create_trees();
}

TEST_TEAR_DOWN(Length)
{
    destroy_trees();
}

TEST(Length, EmptyLength)
{
    // TEST_IGNORE();
    TEST_ASSERT_EQUAL_UINT64(0ul, bst_length(tree_int));
    TEST_ASSERT_EQUAL_UINT64(0ul, bst_length(tree_dbl));
}

TEST(Length, OneNodeLength)
{
    // TEST_IGNORE();
    int i = 1;
    bst_insert_node(tree_int, &i, int_comparator);
    TEST_ASSERT_EQUAL_UINT64(1ul, bst_length(tree_int));

    double d = 1.1;
    bst_insert_node(tree_dbl, &d, double_comparator);
    TEST_ASSERT_EQUAL_UINT64(1ul, bst_length(tree_dbl));
}

TEST(Length, TwoNodeLength)
{
    // TEST_IGNORE();
    int i1 = 1, i2 = 2;
    bst_insert_node(tree_int, &i1, int_comparator);
    bst_insert_node(tree_int, &i2, int_comparator);
    TEST_ASSERT_EQUAL_UINT64(2ul, bst_length(tree_int));

    double d1 = 1.1, d2 = 2.2;
    bst_insert_node(tree_dbl, &d1, double_comparator);
    bst_insert_node(tree_dbl, &d2, double_comparator);
    TEST_ASSERT_EQUAL_UINT64(2ul, bst_length(tree_dbl));
}

TEST(Length, NNodeLength)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("inserting %zu ints", n);
    int *ints = get_n_rand_ints(n);
    for (size_t i = 0; i < n; i++)
        bst_insert_node(tree_int, ints + i, int_comparator);
    TEST_ASSERT_EQUAL_UINT64(n, bst_length(tree_int));
    free(ints);
    
    n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("inserting %zu doubles", n);
    double *doubles = get_n_rand_doubles(n);
    for (size_t i = 0; i < n; i++)
        bst_insert_node(tree_dbl, doubles + i, double_comparator);
    TEST_ASSERT_EQUAL_UINT64(n, bst_length(tree_dbl));
    free(doubles);
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
    create_trees();
}

TEST_TEAR_DOWN(Empty)
{
    destroy_trees();
}

TEST(Empty, EmptyIsEmpty_NotEmptyAfterInserts)
{
    // TEST_IGNORE();
    TEST_ASSERT_TRUE(bst_empty(tree_int));
    int i = 1;
    bst_insert_node(tree_int, &i, int_comparator);
    TEST_ASSERT_FALSE(bst_empty(tree_int));
    i = 0;
    bst_insert_node(tree_int, &i, int_comparator);
    TEST_ASSERT_FALSE(bst_empty(tree_int));
    i = 2;
    bst_insert_node(tree_int, &i, int_comparator);
    TEST_ASSERT_FALSE(bst_empty(tree_int));

    TEST_ASSERT_TRUE(bst_empty(tree_dbl));
    double d = 1.1;
    bst_insert_node(tree_dbl, &d, double_comparator);
    TEST_ASSERT_FALSE(bst_empty(tree_dbl));
    d = 1.0;
    bst_insert_node(tree_dbl, &d, double_comparator);
    TEST_ASSERT_FALSE(bst_empty(tree_dbl));
    d = 1.2;
    bst_insert_node(tree_dbl, &d, double_comparator);
    TEST_ASSERT_FALSE(bst_empty(tree_dbl));
}

TEST_GROUP_RUNNER(Empty)
{
    RUN_TEST_CASE(Empty, EmptyIsEmpty_NotEmptyAfterInserts);
}


TEST_GROUP(Contains);

TEST_SETUP(Contains)
{
    create_trees();
}

TEST_TEAR_DOWN(Contains)
{
    destroy_trees();
}

TEST(Contains, EmptyTreeNotContainsAnything)
{
    // TEST_IGNORE();
    TEST_MESSAGE("This test can take pretty long time to finish...");
    for (int i = INT_MIN; i < INT_MAX; ++i)
        TEST_ASSERT_FALSE(bst_contains(tree_int, &i, int_comparator));

    double d;
    for (size_t i = 0; i < 10000; ++i)
    {
        d = GET_DOUBLE_PLUS_MINUS_100;
        TEST_ASSERT_FALSE(bst_contains(tree_dbl, &d, double_comparator));
    }
}

TEST(Contains, NotEmptyTreeContainsSomething)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    for (int i = -(int)n; i <= (int)n; i++)
    {
        TEST_ASSERT_FALSE(bst_contains(tree_int, &i, int_comparator));
        bst_insert_node(tree_int, &i, int_comparator);
        TEST_ASSERT_TRUE(bst_contains(tree_int, &i, int_comparator));
    }

    n = GET_SIZE_T_FROM_100_TO_200;
    for (double i = -(double)n; i <= (double)n; i++)
    {
        TEST_ASSERT_FALSE(bst_contains(tree_dbl, &i, double_comparator));
        bst_insert_node(tree_dbl, &i, double_comparator);
        TEST_ASSERT_TRUE(bst_contains(tree_dbl, &i, double_comparator));
    }
}


TEST_GROUP_RUNNER(Contains)
{
    RUN_TEST_CASE(Contains, EmptyTreeNotContainsAnything);
    RUN_TEST_CASE(Contains, NotEmptyTreeContainsSomething);
}


TEST_GROUP(Delete);

TEST_SETUP(Delete)
{
    create_trees();
}

TEST_TEAR_DOWN(Delete)
{
    destroy_trees();
}

TEST(Delete, DeleteFromEmptyTree)
{
    // TEST_IGNORE();
    int i = 69;
    TEST_ASSERT_TRUE(bst_empty(tree_int));
    bst_delete_node(tree_int, &i, int_comparator);
    TEST_ASSERT_TRUE(bst_empty(tree_int));
    i = 420;
    bst_delete_node(tree_int, &i, int_comparator);
    TEST_ASSERT_TRUE(bst_empty(tree_int));

    double d = 6.9;
    TEST_ASSERT_TRUE(bst_empty(tree_dbl));
    bst_delete_node(tree_dbl, &d, double_comparator);
    TEST_ASSERT_TRUE(bst_empty(tree_dbl));
    d = 1.4e-20;
    bst_delete_node(tree_dbl, &d, double_comparator);
    TEST_ASSERT_TRUE(bst_empty(tree_dbl));
}

TEST(Delete, DeleteSingle)
{
    // TEST_IGNORE();
    int i = 69;
    bst_insert_node(tree_int, &i, int_comparator);
    bst_delete_node(tree_int, &i, int_comparator);
    TEST_ASSERT_TRUE(bst_empty(tree_int));

    i = 420;
    bst_insert_node(tree_int, &i, int_comparator);
    bst_delete_node(tree_int, &i, int_comparator);
    TEST_ASSERT_TRUE(bst_empty(tree_int));

    double d = 6.9;
    bst_insert_node(tree_dbl, &d, double_comparator);
    bst_delete_node(tree_dbl, &d, double_comparator);
    TEST_ASSERT_TRUE(bst_empty(tree_dbl));
    d = 1.4e-20;
    bst_insert_node(tree_dbl, &d, double_comparator);
    bst_delete_node(tree_dbl, &d, double_comparator);
    TEST_ASSERT_TRUE(bst_empty(tree_dbl));
}


TEST(Delete, DeleteFromNonEmptyTreeMakesTreeEmpty)
{
    // TEST_IGNORE();
    int i[] = {69, 420, 1};
    bst_insert_node(tree_int, i, int_comparator);
    bst_insert_node(tree_int, i+1, int_comparator);
    bst_insert_node(tree_int, i+2, int_comparator);
    bst_delete_node(tree_int, i+1, int_comparator);
    TEST_ASSERT_FALSE(bst_contains(tree_int, i+1, int_comparator));
    TEST_ASSERT_FALSE(bst_empty(tree_int));
    TEST_ASSERT_EQUAL_UINT64(2ul, bst_length(tree_int));
    bst_delete_node(tree_int, i+2, int_comparator);
    TEST_ASSERT_EQUAL_UINT64(1ul, bst_length(tree_int));
    TEST_ASSERT_FALSE(bst_contains(tree_int, i+2, int_comparator));
    bst_delete_node(tree_int, i, int_comparator);
    TEST_ASSERT_TRUE(bst_empty(tree_int));

    double d[] = {6.9, 1.4e20, 42.0};
    bst_insert_node(tree_dbl, d, double_comparator);
    bst_insert_node(tree_dbl, d+1, double_comparator);
    bst_insert_node(tree_dbl, d+2, double_comparator);
    bst_delete_node(tree_dbl, d+1, double_comparator);
    TEST_ASSERT_FALSE(bst_contains(tree_dbl, d+1, double_comparator));
    TEST_ASSERT_FALSE(bst_empty(tree_dbl));
    TEST_ASSERT_EQUAL_UINT64(2ul, bst_length(tree_dbl));
    bst_delete_node(tree_dbl, d+2, double_comparator);
    TEST_ASSERT_EQUAL_UINT64(1ul, bst_length(tree_dbl));
    TEST_ASSERT_FALSE(bst_contains(tree_dbl, d+2, double_comparator));
    bst_delete_node(tree_dbl, d, double_comparator);
    TEST_ASSERT_TRUE(bst_empty(tree_dbl));
}

TEST(Delete, DeleteRootFrom2NodeTree)
{
    // TEST_IGNORE();
    int i[] = {69, 420};
    bst_insert_node(tree_int, i, int_comparator);
    bst_insert_node(tree_int, i+1, int_comparator);
    bst_delete_node(tree_int, i, int_comparator);
    TEST_ASSERT_EQUAL_UINT64(1ul, bst_length(tree_int));
    TEST_ASSERT_EQUAL_INT(i[1], *(int *)tree_int->root->data);
    TEST_ASSERT_NULL(tree_int->root->left);
    TEST_ASSERT_NULL(tree_int->root->right);
    bst_delete_node(tree_int, i+1, int_comparator);
    TEST_ASSERT_TRUE(bst_empty(tree_int));

    bst_insert_node(tree_int, i+1, int_comparator);
    bst_insert_node(tree_int, i, int_comparator);
    bst_delete_node(tree_int, i+1, int_comparator);
    TEST_ASSERT_EQUAL_UINT64(1ul, bst_length(tree_int));
    TEST_ASSERT_EQUAL_INT(i[0], *(int *)tree_int->root->data);
    TEST_ASSERT_NULL(tree_int->root->left);
    TEST_ASSERT_NULL(tree_int->root->right);
    bst_delete_node(tree_int, i, int_comparator);
    TEST_ASSERT_TRUE(bst_empty(tree_int));

    double d[] = {6.9, 42.0};
    bst_insert_node(tree_dbl, d, double_comparator);
    bst_insert_node(tree_dbl, d+1, double_comparator);
    bst_delete_node(tree_dbl, d, double_comparator);
    TEST_ASSERT_EQUAL_UINT64(1ul, bst_length(tree_dbl));
    TEST_ASSERT_EQUAL_INT(d[1], *(double *)tree_dbl->root->data);
    TEST_ASSERT_NULL(tree_dbl->root->left);
    TEST_ASSERT_NULL(tree_dbl->root->right);
    bst_delete_node(tree_dbl, d+1, double_comparator);
    TEST_ASSERT_TRUE(bst_empty(tree_dbl));

    bst_insert_node(tree_dbl, d+1, double_comparator);
    bst_insert_node(tree_dbl, d, double_comparator);
    bst_delete_node(tree_dbl, d+1, double_comparator);
    TEST_ASSERT_EQUAL_UINT64(1ul, bst_length(tree_dbl));
    TEST_ASSERT_EQUAL_INT(d[0], *(double *)tree_dbl->root->data);
    TEST_ASSERT_NULL(tree_dbl->root->left);
    TEST_ASSERT_NULL(tree_dbl->root->right);
    bst_delete_node(tree_dbl, d, double_comparator);
    TEST_ASSERT_TRUE(bst_empty(tree_dbl));
}


TEST(Delete, DeleteLeafFrom2NodeTree)
{
    // TEST_IGNORE();
    int i[] = {69, 420};
    bst_insert_node(tree_int, i, int_comparator);
    bst_insert_node(tree_int, i+1, int_comparator);
    bst_delete_node(tree_int, i+1, int_comparator);
    TEST_ASSERT_EQUAL_UINT64(1ul, bst_length(tree_int));
    TEST_ASSERT_EQUAL_INT(i[0], *(int *)tree_int->root->data);
    TEST_ASSERT_NULL(tree_int->root->left);
    TEST_ASSERT_NULL(tree_int->root->right);

    double d[] = {6.9, 42.0};
    bst_insert_node(tree_dbl, d, double_comparator);
    bst_insert_node(tree_dbl, d+1, double_comparator);
    bst_delete_node(tree_dbl, d+1, double_comparator);
    TEST_ASSERT_EQUAL_UINT64(1ul, bst_length(tree_dbl));
    TEST_ASSERT_EQUAL_INT(d[0], *(double *)tree_dbl->root->data);
    TEST_ASSERT_NULL(tree_dbl->root->left);
    TEST_ASSERT_NULL(tree_dbl->root->right);
    bst_delete_node(tree_dbl, d, double_comparator);
    TEST_ASSERT_TRUE(bst_empty(tree_dbl));
}

TEST(Delete, DeleteAbsentDoesNothing)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("inserting %zu ints", n);
    int *iarr = get_n_rand_ints(n);
    for (size_t i = 0; i < n; i++)
    {
        bst_insert_node(tree_int, iarr + i, int_comparator);
    }
    free(iarr);
    TEST_ASSERT_EQUAL_UINT64(n, bst_length(tree_int));
    int iv = 0xDEAD;
    bst_delete_node(tree_int, &iv, int_comparator);
    TEST_ASSERT_EQUAL_UINT64(n, bst_length(tree_int));
    iv = 0xBABE;
    bst_delete_node(tree_int, &iv, int_comparator);
    TEST_ASSERT_EQUAL_UINT64(n, bst_length(tree_int));

    n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("inserting %zu doubles", n);
    double *darr = get_n_rand_doubles(n);
    for (size_t i = 0; i < n; i++)
    {
        bst_insert_node(tree_dbl, darr + i, double_comparator);
    }
    free(darr);
    TEST_ASSERT_EQUAL_UINT64(n, bst_length(tree_dbl));
    double d = 0xB0B.DEEP0;
    bst_delete_node(tree_dbl, &d, double_comparator);
    TEST_ASSERT_EQUAL_UINT64(n, bst_length(tree_dbl));
    d = 0xD0B.BEEP0;
    bst_delete_node(tree_dbl, &d, double_comparator);
    TEST_ASSERT_EQUAL_UINT64(n, bst_length(tree_dbl));
}

TEST(Delete, DeletePresent)
{
    // TEST_IGNORE();
    size_t n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("inserting %zu ints", n);
    int *iarr = get_n_rand_ints(n);
    for (size_t i = 0; i < n; i++)
    {
        bst_insert_node(tree_int, iarr + i, int_comparator);
    }
    int to_delete_i = iarr[(size_t)rand() % n];
    bst_delete_node(tree_int, &to_delete_i, int_comparator);

    for (size_t i = 0; i < n; i++)
    {
        if (iarr[i] == to_delete_i)
            TEST_ASSERT_FALSE(bst_contains(tree_int, iarr + i, int_comparator));
        else
            TEST_ASSERT_TRUE(bst_contains(tree_int, iarr + i, int_comparator));
    }
    free(iarr);
    TEST_ASSERT_EQUAL_UINT64(n - 1ul, bst_length(tree_int));


    n = GET_SIZE_T_FROM_100_TO_200;
    TEST_PRINTF("inserting %zu doubles", n);
    double *darr = get_n_rand_doubles(n);
    for (size_t i = 0; i < n; i++)
    {
        bst_insert_node(tree_dbl, darr + i, double_comparator);
    }
    double to_delete_d = darr[(size_t)rand() % n];
    bst_delete_node(tree_dbl, &to_delete_d, double_comparator);

    for (size_t i = 0; i < n; i++)
    {
        if (darr[i] == to_delete_d)
            TEST_ASSERT_FALSE(bst_contains(tree_dbl, darr + i, double_comparator));
        else
            TEST_ASSERT_TRUE(bst_contains(tree_dbl, darr + i, double_comparator));
    }
    free(darr);
    TEST_ASSERT_EQUAL_UINT64(n - 1ul, bst_length(tree_dbl));
}


TEST_GROUP_RUNNER(Delete)
{
    RUN_TEST_CASE(Delete, DeleteFromEmptyTree);
    RUN_TEST_CASE(Delete, DeleteSingle);
    RUN_TEST_CASE(Delete, DeleteFromNonEmptyTreeMakesTreeEmpty);
    RUN_TEST_CASE(Delete, DeleteRootFrom2NodeTree);
    RUN_TEST_CASE(Delete, DeleteLeafFrom2NodeTree);
    RUN_TEST_CASE(Delete, DeleteAbsentDoesNothing);
    RUN_TEST_CASE(Delete, DeletePresent);
}



TEST_GROUP(Print);

FILE *f;
const char *filename = "test.txt";

TEST_SETUP(Print)
{
    create_trees();
}

TEST_TEAR_DOWN(Print)
{
    destroy_trees();
    remove(filename);
}

TEST(Print, PrintIntEmptyTree)
{
    // TEST_IGNORE();
    f = fopen(filename, "w");
    bst_print_int(tree_int, f);
    fclose(f);
    f = fopen(filename, "r");
    char buf[64];
    fscanf(f, "%[^\n]", buf);
    fclose(f);
    TEST_ASSERT_EQUAL_STRING(buf, "()");
}

TEST(Print, PrintIntNonEmptyTree)
{
    // TEST_IGNORE();
    int iarr[] = {351, 420, 69, 28980, 489};
    for (size_t i = 0; i < sizeof(iarr) / sizeof(int); i++)
        bst_insert_node(tree_int, iarr + i, int_comparator);
    f = fopen(filename, "w");
    bst_print_int(tree_int, f);
    fclose(f);
    f = fopen(filename, "r");
    char buf[64];
    fscanf(f, "%[^\n]", buf);
    fclose(f);
    TEST_ASSERT_EQUAL_STRING(buf, "(351, l -> (69), r -> (420, r -> (28980, l -> (489))))");
}

TEST_GROUP_RUNNER(Print)
{
    RUN_TEST_CASE(Print, PrintIntEmptyTree);
    RUN_TEST_CASE(Print, PrintIntNonEmptyTree);
}

int TREE_ARRAYS[][15] = {
    {1},
    {1, 2, 3},
    {5, 2, 1, 3, 6, 4},
    {8, 5, 1, 7, 10, 12},
    {25, 15, 10, 4, 12, 22, 18, 24, 50, 35, 31, 44, 70, 66, 90}
};


TEST_GROUP(Traverse);

TEST_SETUP(Traverse)
{
    create_trees();
}

TEST_TEAR_DOWN(Traverse)
{
    destroy_trees();
}

TEST(Traverse, PreorderEmptyAndOne)
{
    // TEST_IGNORE();
    void *result = bst_preorder_traversal(tree_int);
    TEST_ASSERT_NULL(result);
    size_t size = 1ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[0], int_comparator);
    int *actual = bst_preorder_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(TREE_ARRAYS[0], actual, size);
    free(actual);
}

TEST(Traverse, PreorderThree)
{
    // TEST_IGNORE();
    size_t size = 3ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[1], int_comparator);
    int *actual = bst_preorder_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(TREE_ARRAYS[1], actual, size);
    free(actual);
}

TEST(Traverse, PreorderSix1)
{
    // TEST_IGNORE();
    size_t size = 6ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[2], int_comparator);
    int expected[] = {5, 2, 1, 3, 4, 6};
    int *actual = bst_preorder_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected, actual, size);
    free(actual);
}

TEST(Traverse, PreorderSix2)
{
    // TEST_IGNORE();
    size_t size = 6ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[3], int_comparator);
    int expected[] = {8, 5, 1, 7, 10, 12};
    int *actual = bst_preorder_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected, actual, size);
    free(actual);
}

TEST(Traverse, PreorderFifteen)
{
    // TEST_IGNORE();
    size_t size = 15ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[4], int_comparator);
    int expected[] = {25, 15, 10, 4, 12, 22, 18, 24, 50, 35, 31, 44, 70, 66, 90};
    int *actual = bst_preorder_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected, actual, size);
    free(actual);
}


TEST(Traverse, InorderEmptyAndOne)
{
    // TEST_IGNORE();
    void *result = bst_inorder_traversal(tree_int);
    TEST_ASSERT_NULL(result);
    size_t size = 1ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[0], int_comparator);
    int *actual = bst_inorder_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(TREE_ARRAYS[0], actual, size);
    free(actual);
}

TEST(Traverse, InorderThree)
{
    // TEST_IGNORE();
    size_t size = 3ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[1], int_comparator);
    int *actual = bst_inorder_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(TREE_ARRAYS[1], actual, size);
    free(actual);
}

TEST(Traverse, InorderSix1)
{
    // TEST_IGNORE();
    size_t size = 6ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[2], int_comparator);
    int expected[] = {1, 2, 3, 4, 5, 6};
    int *actual = bst_inorder_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected, actual, size);
    free(actual);
}

TEST(Traverse, InorderSix2)
{
    // TEST_IGNORE();
    size_t size = 6ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[3], int_comparator);
    int expected[] = {1, 5, 7, 8, 10, 12};
    int *actual = bst_inorder_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected, actual, size);
    free(actual);
}

TEST(Traverse, InorderFifteen)
{
    // TEST_IGNORE();
    size_t size = 15ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[4], int_comparator);
    int expected[] = {4, 10, 12, 15, 18, 22, 24, 25, 31, 35, 44, 50, 66, 70, 90};
    int *actual = bst_inorder_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected, actual, size);
    free(actual);
}


TEST(Traverse, PostorderEmptyAndOne)
{
    // TEST_IGNORE();
    void *result = bst_postorder_traversal(tree_int);
    TEST_ASSERT_NULL(result);
    size_t size = 1ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[0], int_comparator);
    int *actual = bst_postorder_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(TREE_ARRAYS[0], actual, size);
    free(actual);
}

TEST(Traverse, PostorderThree)
{
    // TEST_IGNORE();
    size_t size = 3ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[1], int_comparator);
    int expected[] = {3, 2, 1};
    int *actual = bst_postorder_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected, actual, size);
    free(actual);
}

TEST(Traverse, PostorderSix1)
{
    // TEST_IGNORE();
    size_t size = 6ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[2], int_comparator);
    int expected[] = {1, 4, 3, 2, 6, 5};
    int *actual = bst_postorder_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected, actual, size);
    free(actual);
}

TEST(Traverse, PostorderSix2)
{
    // TEST_IGNORE();
    size_t size = 6ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[3], int_comparator);
    int expected[] = {1, 7, 5, 12, 10, 8};
    int *actual = bst_postorder_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected, actual, size);
    free(actual);
}

TEST(Traverse, PostorderFifteen)
{
    // TEST_IGNORE();
    size_t size = 15ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[4], int_comparator);
    int expected[] = {4, 12, 10, 18, 24, 22, 15, 31, 44, 35, 66, 90, 70, 50, 25};
    int *actual = bst_postorder_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected, actual, size);
    free(actual);
}

TEST(Traverse, LevelOrderEmptyAndOne)
{
    // TEST_IGNORE();
    void *result = bst_level_order_traversal(tree_int);
    TEST_ASSERT_NULL(result);
    size_t size = 1ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[0], int_comparator);
    int *actual = bst_level_order_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(TREE_ARRAYS[0], actual, size);
    free(actual);
}

TEST(Traverse, LevelOrderThree)
{
    // TEST_IGNORE();
    size_t size = 3ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[1], int_comparator);
    int expected[] = {1, 2, 3};
    int *actual = bst_level_order_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected, actual, size);
    free(actual);
}

TEST(Traverse, LevelOrderSix1)
{
    // TEST_IGNORE();
    size_t size = 6ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[2], int_comparator);
    int expected[] = {5, 2, 6, 1, 3, 4};
    int *actual = bst_level_order_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected, actual, size);
    free(actual);
}

TEST(Traverse, LevelOrderSix2)
{
    // TEST_IGNORE();
    size_t size = 6ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[3], int_comparator);
    int expected[] = {8, 5, 10, 1, 7, 12};
    int *actual = bst_level_order_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected, actual, size);
    free(actual);
}

TEST(Traverse, LevelOrderFifteen)
{
    // TEST_IGNORE();
    size_t size = 15ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[4], int_comparator);
    int expected[] = {25, 15, 50, 10, 22, 35, 70, 4, 12, 18, 24, 31, 44, 66, 90};
    int *actual = bst_level_order_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected, actual, size);
    free(actual);
}

TEST(Traverse, DeleteRoot)
{
    size_t size = 15ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[4], int_comparator);
    int to_delete = 25;
    bst_delete_node(tree_int, &to_delete, int_comparator);
    int expected_pre[] = {31, 15, 10, 4, 12, 22, 18, 24, 50, 35, 44, 70, 66, 90};
    int expected_in[] = {4, 10, 12, 15, 18, 22, 24, 31, 35, 44, 50, 66, 70, 90};
    int expected_post[] = {4, 12, 10, 18, 24, 22, 15, 44, 35, 66, 90, 70, 50, 31};
    int expected_lev[] = {31, 15, 50, 10, 22, 35, 70, 4, 12, 18, 24, 44, 66, 90};
    int *actual_pre = bst_preorder_traversal(tree_int);
    int *actual_in = bst_inorder_traversal(tree_int);
    int *actual_post = bst_postorder_traversal(tree_int);
    int *actual_lev = bst_level_order_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected_pre, actual_pre, size - 1ul);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected_in, actual_in, size - 1ul);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected_post, actual_post, size - 1ul);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected_lev, actual_lev, size - 1ul);
    free(actual_pre);
    free(actual_in);
    free(actual_post);
    free(actual_lev);
}

TEST(Traverse, DeleteFullNode)
{
    size_t size = 15ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[4], int_comparator);
    int to_delete = 15;
    bst_delete_node(tree_int, &to_delete, int_comparator);
    int expected_pre[] = {25, 18, 10, 4, 12, 22, 24, 50, 35, 31, 44, 70, 66, 90};
    int expected_in[] = {4, 10, 12, 18, 22, 24, 25, 31, 35, 44, 50, 66, 70, 90};
    int expected_post[] = {4, 12, 10, 24, 22, 18, 31, 44, 35, 66, 90, 70, 50, 25};
    int expected_lev[] = {25, 18, 50, 10, 22, 35, 70, 4, 12, 24, 31, 44, 66, 90};
    int *actual_pre = bst_preorder_traversal(tree_int);
    int *actual_in = bst_inorder_traversal(tree_int);
    int *actual_post = bst_postorder_traversal(tree_int);
    int *actual_lev = bst_level_order_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected_pre, actual_pre, size - 1ul);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected_in, actual_in, size - 1ul);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected_post, actual_post, size - 1ul);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected_lev, actual_lev, size - 1ul);
    free(actual_pre);
    free(actual_in);
    free(actual_post);
    free(actual_lev);
}

TEST(Traverse, DeleteLeaf)
{
    size_t size = 15ul;
    bst_insert_array(tree_int, size, TREE_ARRAYS[4], int_comparator);
    int to_delete = 66;
    bst_delete_node(tree_int, &to_delete, int_comparator);
    int expected_pre[] = {25, 15, 10, 4, 12, 22, 18, 24, 50, 35, 31, 44, 70, 90};
    int expected_in[] = {4, 10, 12, 15, 18, 22, 24, 25, 31, 35, 44, 50, 70, 90};
    int expected_post[] = {4, 12, 10, 18, 24, 22, 15, 31, 44, 35, 90, 70, 50, 25};
    int expected_lev[] = {25, 15, 50, 10, 22, 35, 70, 4, 12, 18, 24, 31, 44, 90};
    int *actual_pre = bst_preorder_traversal(tree_int);
    int *actual_in = bst_inorder_traversal(tree_int);
    int *actual_post = bst_postorder_traversal(tree_int);
    int *actual_lev = bst_level_order_traversal(tree_int);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected_pre, actual_pre, size - 1ul);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected_in, actual_in, size - 1ul);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected_post, actual_post, size - 1ul);
    TEST_ASSERT_EQUAL_INT_ARRAY(expected_lev, actual_lev, size - 1ul);
    free(actual_pre);
    free(actual_in);
    free(actual_post);
    free(actual_lev);
}


TEST_GROUP_RUNNER(Traverse)
{
    RUN_TEST_CASE(Traverse, PreorderEmptyAndOne);
    RUN_TEST_CASE(Traverse, PreorderThree);
    RUN_TEST_CASE(Traverse, PreorderSix1);
    RUN_TEST_CASE(Traverse, PreorderSix2);
    RUN_TEST_CASE(Traverse, PreorderFifteen);
    RUN_TEST_CASE(Traverse, InorderEmptyAndOne);
    RUN_TEST_CASE(Traverse, InorderThree);
    RUN_TEST_CASE(Traverse, InorderSix1);
    RUN_TEST_CASE(Traverse, InorderSix2);
    RUN_TEST_CASE(Traverse, InorderFifteen);
    RUN_TEST_CASE(Traverse, PostorderEmptyAndOne);
    RUN_TEST_CASE(Traverse, PostorderThree);
    RUN_TEST_CASE(Traverse, PostorderSix1);
    RUN_TEST_CASE(Traverse, PostorderSix2);
    RUN_TEST_CASE(Traverse, PostorderFifteen);
    RUN_TEST_CASE(Traverse, LevelOrderEmptyAndOne);
    RUN_TEST_CASE(Traverse, LevelOrderThree);
    RUN_TEST_CASE(Traverse, LevelOrderSix1);
    RUN_TEST_CASE(Traverse, LevelOrderSix2);
    RUN_TEST_CASE(Traverse, LevelOrderFifteen);
    RUN_TEST_CASE(Traverse, DeleteRoot);
    RUN_TEST_CASE(Traverse, DeleteFullNode);
    RUN_TEST_CASE(Traverse, DeleteLeaf);
}


static void run_all_tests(void)
{
    RUN_TEST_GROUP(Create);
    RUN_TEST_GROUP(Insert);
    RUN_TEST_GROUP(Length);
    RUN_TEST_GROUP(Empty);
    RUN_TEST_GROUP(Contains);
    RUN_TEST_GROUP(Delete);
    RUN_TEST_GROUP(Print);
    RUN_TEST_GROUP(Traverse);
}

int main(int argc, const char * argv[])
{   
    srand((unsigned int)time(NULL));
    return UnityMain(argc, argv, run_all_tests);
}
