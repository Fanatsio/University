from typing import Any


class ListNode:
    def __init__(self, *args):
        if not args:
            return
        
        if len(args) == 1:
            self.value = args[0]
            self.next = None
        elif len(args) == 2 and isinstance(args[1], ListNode):
            self.value = args[0]
            self.next = args[1]
        else:
            raise TypeError()
    
    def __str__(self):
        return f"({self.value}) -> {self.next}"
    
    def __eq__(self, val):
        if not isinstance(val, ListNode):
            return False
        
        return self.value == val.value and self.next == val.next
    
    def __ne__(self, val):
        return not self.__eq__(val)
    
    
class MyList:
    def __init__(self, *args):
        if args and args[0] is not None:
            x = ListNode(args[0])
            self.head = x
            self._count = 1
        else:
            self.head = None
            self._count = 0

    def append(self, value):
        if self.head:
            a = self.head
            while a.next:
                a = a.next
            a.next = ListNode(value)
        else:
            self.head = ListNode(value)
        self._count += 1
    
    def __len__(self):
        return self._count
    
    def __str__(self):
        if not len(self):
            return "None"
        else:
            a = self.head
            result = f"({a.value}) -> "
            while a.next:
                a = a.next
                result += f"({a.value}) -> "
            a = a.next
            result += f"{a}"
            return result
        
    def __repr__(self):
        return str(self)
    
    def __eq__(self, n2):
        if isinstance(n2, MyList):
            return str(self) == str(n2)
        else:
            return False
    
    def __ne__(self, n2):
        return not self == n2
    
    def __contains__(self, value):
        if not len(self):
            return False
        else:
            a = self.head
            if a.value == value:
                return True
            while a.next:
                a = a.next
                if a.value == value:
                    return True
        return False
    
    def remove(self, value):
        if self.head is None:
            raise ValueError()

        if self.head.value == value:
            self.head = self.head.next
            self._count -= 1
            return

        current = self.head
        while current.next:
            if current.next.value == value:
                current.next = current.next.next
                self._count -= 1
                return
            current = current.next

        raise ValueError()
    
    def pop(self):
        if self.head is None:
            raise IndexError('pop from empty list')
        
        current = self.head
        if current.next is None:
            value = current.value
            self.head = None
            self._count -= 1
            return value
        
        while current.next.next:
            current = current.next
        value = current.next.value
        current.next = None
        self._count -= 1
        return value

    def clear(self):
        self.head = None
        self._count = 0

    def extend(self, other):
        if isinstance(other, MyList):
            a = other.head
            
            while a:
                self.append(a.value)
                a = a.next
                
        else:
            raise TypeError()

    
    def copy(self):
        new_list = MyList()
        current = self.head
        while current:
            new_list.append(current.value)
            current = current.next
        return new_list

    def insert(self, index, value):
        if (not isinstance(index, int)) or index < 0:
            raise IndexError() 
        if index >= self._count:
            self.append(value)
            return
        if index == 0:
            new_node = ListNode(value, self.head)
            self.head = new_node
            self._count += 1
            return
        current = self.head
        for _ in range(index - 1):
            current = current.next
            if current is None:
                return
        new_node = ListNode(value, current.next)
        current.next = new_node
        self._count += 1

    def index(self, value):
        current = self.head
        idx = 0
        while current:
            if current.value == value:
                return idx
            current = current.next
            idx += 1
        raise ValueError(f"{value} is not in list")

    def count(self, value):
        _count = 0
        current = self.head
        while current:
            if current.value == value:
                _count += 1
            current = current.next
        return _count

    def reverse(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev
