class StudentNode:
    def __init__(self, surname, birth_year, enrollment_year, grades, _prev=None, _next=None):
        self.surname: str = surname
        self.birth_year: int = birth_year
        self.enrollment_year: int = enrollment_year
        self.grades: list[int] = grades
        self.next: StudentNode | None = _next
        self.prev: StudentNode | None = _prev

    def __str__(self):
        return f"{{ {self.surname} }} {{ {self.birth_year} }} {{ {self.enrollment_year} }} {{ {self.grades} }}"

    def __copy__(self):
        return StudentNode(
            self.surname, self.birth_year, self.enrollment_year, self.grades
        )

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, StudentNode):
            raise TypeError(f" {type(other)} not StudentNode")

        return str(self) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if not isinstance(other, StudentNode):
            raise TypeError(f" {type(other)} not StudentNode")
        return self.surname < other.surname

    def __gt__(self, other):
        if not isinstance(other, StudentNode):
            raise TypeError(f" {type(other)} not StudentNode")
        return self.surname > other.surname

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)


class DoublyLinkedList:
    def __init__(self):
        self.tail: StudentNode | None = None
        self.head: StudentNode | None = None

    def append(self, node: StudentNode):
        if self.tail is None:
            node.prev = None
            node.next = None
            self.tail = node
            self.head = node
        else:
            node.prev = self.tail
            node.next = None
            self.tail.next = node
            self.tail = node

    def remove(self, value: StudentNode):
        if value.prev:
            value.prev.next = value.next
        else:
            self.head = value.next

        if value.next:
            value.next.prev = value.prev
        else:
            self.tail = value.prev

    def sort(self):
        if not self.head or not self.head.next:
            return

        sorted_tail = self.head
        unsorted = self.head.next

        while unsorted:
            current = unsorted
            unsorted = unsorted.next

            if current < sorted_tail:
                sorted_tail.next = unsorted

                if current < self.head:
                    current.next = self.head
                    current.prev = None
                    self.head.prev = current
                    self.head = current
                else:
                    pointer = self.head
                    while pointer.next < current:
                        pointer = pointer.next
                    current.next = pointer.next
                    current.prev = pointer
                    pointer.next.prev = current
                    pointer.next = current
            else:
                sorted_tail = current

        self.tail = sorted_tail

    def linear_search_by_surname(self, surname) -> StudentNode | None:
        for i in self:
            if i.surname == surname:
                return i
        return None

    def binary_search_by_surname(self, surname) -> StudentNode | None:
        def get_middle(start, end):
            slow = start
            fast = start.next

            while fast != end:
                fast = fast.next
                if fast != end:
                    fast = fast.next
                    slow = slow.next
            return slow

        left = self.head
        right = None

        while left != right:
            mid = get_middle(left, right)
            if mid.surname == surname:
                return mid
            elif mid.surname < surname:
                left = mid.next
            else:
                right = mid

        return None

    def __len__(self):
        count = 0
        for _ in self:
            count += 1
        return count

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current
            current = current.next

    def __str__(self):
        return " <-> ".join([str(i) for i in self])
