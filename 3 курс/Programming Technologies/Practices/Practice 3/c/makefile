CFLAGS  = -std=c11
# CFLAGS += -O0 -g # Debug
CFLAGS += -O1
CFLAGS += -Wall -Wextra -pedantic
CFLAGS += -Wformat=2
CFLAGS += -Wnull-dereference
CFLAGS += -Winit-self
CFLAGS += -Wunused
CFLAGS += -Wstrict-overflow=5
CFLAGS += -Wstringop-overflow=4
CFLAGS += -Wundef
CFLAGS += -Wshadow
CFLAGS += -Wpointer-arith
CFLAGS += -Wbad-function-cast
CFLAGS += -Wcast-qual
CFLAGS += -Wcast-align
CFLAGS += -Wwrite-strings
CFLAGS += -Wconversion
CFLAGS += -Wstrict-prototypes
CFLAGS += -Wold-style-definition
CFLAGS += -Wmissing-prototypes
CFLAGS += -Wmissing-declarations
CFLAGS += -Wunreachable-code
CFLAGS += -Winline
CFLAGS += -Werror
CFLAGS += -fstrict-aliasing
# https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html

ASANFLAGS  = -fsanitize=address
ASANFLAGS += -fno-common
ASANFLAGS += -fno-omit-frame-pointer

UNITYFLAGS += -DUNITY_INCLUDE_CONFIG_H


UNITYROOT = test-framework
C_FILES = *.c
SRC = $(UNITYROOT)/$(C_FILES) ./$(C_FILES)


COMPILE_MSG = echo Compiling $@
COMPILE = $(CC) $(CFLAGS) $(UNITYFLAGS) $^ -o $@
RUN = ./$@ -v

TEST_TARGET = tests
MEMCHECK_TARGET = memcheck


$(TEST_TARGET): $(SRC)
	@$(COMPILE_MSG)
	@$(COMPILE)
	@$(RUN)


$(MEMCHECK_TARGET): $(SRC)
	@$(COMPILE_MSG)
	@$(COMPILE) $(ASANFLAGS)
	@$(RUN)
	@echo "Memory check passed"


.PHONY: clean
clean:
	rm -rf *.o $(TEST_TARGET) $(MEMCHECK_TARGET)
