# Name: Andre Simao Osorio de Barros
# OSU Email: simaoosa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 04
# Due Date: Jul 26, 2024
# Description: Creation of an MinHeap class.


from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MinHeap with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MinHeap content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return "HEAP " + str(heap_data)

    def add(self, node: object) -> None:
        """
        Adds a new object to the MinHeap while maintains heap properties.

        :param node: any Python object

        :return: does not return
        """
        # Adds node to the last position in the min heap
        heap = self._heap
        heap.append(node)

        # Calculates the index of the node added and its parent
        index = heap.length() - 1
        parent_index = (index - 1) // 2

        # Percolates up the min heap to keep heap property
        while index > 0 and heap[index] < heap[parent_index]:
            temp = heap[parent_index]
            heap[parent_index] = heap[index]
            heap[index] = temp
            index = parent_index
            parent_index = (index - 1) // 2

    def is_empty(self) -> bool:
        """
        Checks if the heap is empty

        :param: a MinHeap class object

        :return: a boolean (True if the heap is empty, False otherwise)
        """

        return True if self._heap.length() == 0 else False

    def get_min(self) -> object:
        """
        Returns the object with the minimum key in the heap.

        :param: a MinHeap class object

        :return: any Python object
        """
        if self.is_empty():
            raise MinHeapException
        return self._heap[0]

    def remove_min(self) -> object:
        """
        Returns and removes the object with the minimum key in the
        heap.

        :param: a MinHeap class object

        :return: any Python object
        """

        if self._heap.is_empty():
            raise MinHeapException

        size = self._heap.length()
        min = self.get_min()
        last = self._heap[size - 1]
        self._heap[0], last = last, self._heap[0]
        self._heap.pop()
        self._percolate_down(0, size - 1)

        return min

    def _percolate_down(self, index: int, size: int) -> None:
        """
        Helper method which percolates down a minHeap
        keeping min heap property.

        :param index: an integer (index of the parent item)
        :param size: an integer (size of an array)

        :return: does not return
        """

        heap = self._heap

        # Percolates down the min heap to keep heap property
        while True:                                   # all if's below are False or last if is True, loop finishes
            left_child = index * 2 + 1                # index of left child in the array
            right_child = index * 2 + 2               # index of right child in the array
            min = index

            # checks if left child exists and is smaller than parent
            if left_child < size and heap[left_child] < heap[min]:
                min = left_child                      # if yes, min becomes left child index

            # checks if right child exists and is smaller than parent (if conditional above is False) or left child
            if right_child < size and heap[right_child] < heap[min]:
                min = right_child                     # if yes, min becomes right child index

            # checks if parent is smaller than left and right child
            if min == index:                          # if yes, all above are False and index = min
                return                                # breaks out the loop

            # swap places with the smallest child
            heap[index], heap[min] = heap[min], heap[index]
            index = min

    def build_heap(self, da: DynamicArray) -> None:
        """
        Builds a min heap from an unsorted DynamicArray object

        :param da: DynamicArray class object

        :return: does not return

        """
        # Clears the current heap
        self.clear()

        # Copies items from the DynamicArray passed as a parameter into the empty heap
        for index in range(da.length()):
            self._heap.append(da[index])

        size = self._heap.length()
        index = (size - 1) // 2

        # Builds the heap
        while index >= 0:
            self._percolate_down(index, size)
            index -= 1

    def size(self) -> int:
        """
        Returns the number of items stored in a min heap.

        :param node: a MinHeap class object

        :return: does not return

        """
        return self._heap.length()

    def clear(self) -> None:
        """
        Clears the contents of the heap.

        :param node: a MinHeap class object

        :return: does not return

        """
        self._heap = DynamicArray()

def heapsort(da: DynamicArray) -> None:
    """
    Sorts items of a DynamicArray object in non-ascending order.

    :param da: a DynamicArray class object

    :return: does not return
    """

    # Creates a MinHeap instance and builds the heap
    hp = MinHeap()
    hp.build_heap(da)

    # Loops through the heap and sorts it in un-ascending order
    size = da.length() - 1
    while size > 0:
        hp._heap[0], hp._heap[size] = hp._heap[size], hp._heap[0]
        hp._percolate_down(0, size)
        size -= 1

    # Copies the sorted items from the heap back into the array
    for index in range(da.length()):
        da[index] = hp._heap[index]

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())
    #
    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())
    #
    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())
    #
    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)
    #
    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")
