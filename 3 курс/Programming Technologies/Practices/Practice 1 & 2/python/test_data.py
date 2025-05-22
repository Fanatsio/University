SINGLE_VALUES1 = [0, 1, 2, 3, 4]
SINGLE_VALUES2 = [1, 22, 333, 69, 420]
DOUBLE_VALUES = [[0, 1], [1, 2], [7, 3], [69, 420]]
TRIPLE_VALUES = [[0, 1, 2], [7, 3, 4], [69, 420, 42]]
DIFFERENT_LISTS = [
    [1],
    SINGLE_VALUES1,
    SINGLE_VALUES2,
    *DOUBLE_VALUES,
    *TRIPLE_VALUES,
]
DIFFERENT_LISTS_WITH_EMPTY = [[]] + DIFFERENT_LISTS


def get_list_str(input_seq):
    if input_seq:
        return "(" + ") -> (".join(map(str, input_seq)) + ") -> None"
    return "None"


STR_CHECK_2_VALUES = [(t, get_list_str(t)) for t in DOUBLE_VALUES]
STR_CHECK_3_VALUES = [(t, get_list_str(t)) for t in TRIPLE_VALUES]
