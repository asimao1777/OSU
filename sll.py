# Name: Andre Simao Osorio de Barros
# OSU Email: simaoosa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 3
# Due Date: Jul 21, 2024
# Description: Create an SLL Class and its methods.


from SLNode import *


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class LinkedList:
    def __init__(self, start_list=None) -> None:
        """
        Initialize new linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = SLNode(None)

        # populate SLL with initial values (if provided)
        # before using this feature, implement insert_back() method
        if start_list is not None:
            for value in start_list:
                self.insert_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        node = self._head.next
        while node:
            out += str(node.value)
            if node.next:
                out += ' -> '
            node = node.next
        out += ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        node = self._head.next
        while node:
            length += 1
            node = node.next
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return not self._head.next

    # ------------------------------------------------------------------ #

    def insert_front(self, value: object) -> None:
        """
        Insert a node into an SLL at the front (head).

        :param value: any Python object

        :return: does not return
        """
        frontSentinel = self._head
        new_node = SLNode(value)
        new_node.next = frontSentinel.next
        frontSentinel.next = new_node

    def insert_back(self, value: object) -> None:
        """
        Insert a node into an SLL at the back (tail).

        :param value: any Python object

        :return: does not return
        """
        frontSentinel = self._head
        new_node = SLNode(value)
        cur = frontSentinel                       # cur is always a node at index - 1 because it is the frontSentinel

        # Inserts new node at the tail of the linked list
        while cur.next is not None:
            cur = cur.next
        new_node.next = cur.next
        cur.next = new_node

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts a new value at a specified index position in the SLL

        :param index: an integer
        :param value: any Python object

        :return: does not return
        """
        # Data validation
        if index < 0 or index > self.length():
            raise SLLException

        frontSentinel = self._head
        cur = frontSentinel                       # cur is always a node at index - 1 because it is the frontSentinel
        counter = 0

        # Inserts new node at the index passed as parameter
        while counter != index:
            cur = cur.next
            counter += 1
        new_node = SLNode(value)
        new_node.next = cur.next
        cur.next = new_node

    def remove_at_index(self, index: int) -> None:
        """
        Removes the node from the SLL at the specified index position.

        :param index: an integer

        :return: does not return
        """
        # Data validation
        if index < 0 or index >= self.length():
            raise SLLException

        frontSentinel = self._head
        cur = frontSentinel                      # cur is always a node at index - 1 because it is the frontSentinel
        counter = 0

        # Removes node at the index passed as parameter
        while counter != index:
            cur = cur.next
            counter += 1
        cur.next = cur.next.next

    def remove(self, value: object) -> bool:
        """
        Removes the first node from the SLL which contains the value
        passed as parameter.

        :param value: any Python object

        :return: a boolean (True if node was removed, False otherwise)
        """
        frontSentinel = self._head
        cur = frontSentinel                     # cur is always a node at index - 1 because it is the frontSentinel
        counter = self.length()

        # Removes node the has the value passed as parameter
        while counter > 0:
            if cur.next.value == value:
                cur.next = cur.next.next
                return True
            counter -= 1
            cur = cur.next
        return False

    def count(self, value: object) -> int:
        """
        Counts the number of items in the list that matches the value
        passed as parameter

        :param value: any Python object

        :returns: an integer
        """
        frontSentinel = self._head
        cur = frontSentinel                     # cur is always a node at index - 1 because it is the frontSentinel
        num_matches = 0
        counter = self.length()

        # Traverses the SLL and counts equality between item and parameter
        while counter > 0:
            if cur.next.value == value:
                num_matches += 1
            cur = cur.next
            counter -= 1
        return num_matches

    def find(self, value: object) -> bool:
        """
        Checks whether a value exists in a SLL.

        :param value: any Python object

        :return: a boolean (True if the value exists, False otherwise)
        """
        frontSentinel = self._head
        cur = frontSentinel                     # cur is always a node at index - 1 because it is the frontSentinel
        counter = self.length()

        # Checks whether the value exists in the SLL
        while counter > 0:
            if cur.next.value == value:
                return True
            counter -= 1
            cur = cur.next
        return False

    def slice(self, start_index: int, size: int) -> "LinkedList":
        """
        Slices current SLL creating a new SLL through passing a start index and the
        cardinality of the new SLL as parameters.

        :param start_index: an integer
        :param size: an integer

        :return: a SLL object
        """
        # Data validation
        if start_index < 0 or start_index > self.length() - 1:
            raise SLLException("Invalid starting index.")

        if size < 0 or size > (self.length() - start_index):
            raise SLLException("Not enough nodes.")

        frontSentinel = self._head
        cur = frontSentinel                     # cur is always a node at index - 1 because it is the frontSentinel
        counter = 0

        new_sll = LinkedList()

        # Moves cur to the starting index (cur = node at start_index)
        while counter < start_index:
            cur = cur.next
            counter += 1

        # Inserts the values into a new SLL (starting at cur)
        for _ in range(size):
            new_sll.insert_back(cur.next.value)
            cur = cur.next

        return new_sll


if __name__ == "__main__":

    print("\n# insert_front example 1")
    test_case = ["A", "B", "C"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_front(case)
        print(lst)

    print("\n# insert_back example 1")
    test_case = ["C", "B", "A"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_back(case)
        print(lst)

    print("\n# insert_at_index example 1")
    lst = LinkedList()
    test_cases = [(0, "A"), (0, "B"), (1, "C"), (3, "D"), (-1, "E"), (5, "F")]
    for index, value in test_cases:
        print("Inserted", value, "at index", index, ": ", end="")
        try:
            lst.insert_at_index(index, value)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove_at_index example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6])
    print(f"Initial LinkedList : {lst}")
    for index in [0, 2, 0, 2, 2, -2]:
        print("Removed at index", index, ": ", end="")
        try:
            lst.remove_at_index(index)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [7, 3, 3, 3, 3]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# remove example 2")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [1, 2, 3, 1, 2, 3, 3, 2, 1]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# count example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 2])
    print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))

    print("\n# find example 1")
    lst = LinkedList(["Waldo", "Clark Kent", "Homer", "Santa Claus"])
    print(lst)
    print(lst.find("Waldo"))
    print(lst.find("Superman"))
    print(lst.find("Santa Claus"))

    print("\n# slice example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = lst.slice(1, 3)
    print("Source:", lst)
    print("Start: 1 Size: 3 :", ll_slice)
    ll_slice.remove_at_index(0)
    print("Removed at index 0 :", ll_slice)

    print("\n# slice example 2")
    lst = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("Source:", lst)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Start:", index, "Size:", size, end="")
        try:
            print(" :", lst.slice(index, size))
        except:
            print(" : exception occurred.")
