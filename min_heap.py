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
        min = self.get_min()
        self._heap[0], self._heap[self._heap.length() - 1] = self._heap[self._heap.length() - 1], self._heap[0]
        self._heap.pop()
        # self._percolate_down(self._heap, self._heap.get_min())
        return min

    def build_heap(self, da: DynamicArray) -> None:
        """
        TODO: Write this implementation
        """
        pass

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
    TODO: Write this implementation
    """
    pass


# It's highly recommended that you implement the following optional          #
# helper function for percolating elements down the MinHeap. You can call    #
# this from inside the MinHeap class. You may edit the function definition.  #

def _percolate_down(da: DynamicArray, parent: int) -> None:
    """
    TODO: Write your implementation
    """
    pass


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
    # print("\nPDF - build_heap example 1")
    # print("--------------------------")
    # da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    # h = MinHeap(['zebra', 'apple'])
    # print(h)
    # h.build_heap(da)
    # print(h)
    #
    # print("--------------------------")
    # print("Inserting 500 into input DA:")
    # da[0] = 500
    # print(da)
    #
    # print("Your MinHeap:")
    # print(h)
    # if h.get_min() == 500:
    #     print("Error: input array and heap's underlying DA reference same object in memory")
    #
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
    # print("\nPDF - heapsort example 1")
    # print("------------------------")
    # da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    # print(f"Before: {da}")
    # heapsort(da)
    # print(f"After:  {da}")
    #
    # print("\nPDF - heapsort example 2")
    # print("------------------------")
    # da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    # print(f"Before: {da}")
    # heapsort(da)
    # print(f"After:  {da}")
