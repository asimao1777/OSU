# Name: Andre Simao Osorio de Barros
# OSU Email: simaoosa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 02
# Due Date: Jul 15, 2024
# Description: Creation of Bag class with its methods.


from dynamic_array import *


class Bag:
    def __init__(self, start_bag=None):
        """
        Init new bag based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

        # populate bag with initial values (if provided)
        # before using this feature, implement add() method
        if start_bag is not None:
            for value in start_bag:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "BAG: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da.get_at_index(_))
                          for _ in range(self._da.length())])
        return out + ']'

    def size(self) -> int:
        """
        Return total number of items currently in the bag
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def add(self, value: object) -> None:
        """
        Adds an item to the bag.

        :param value: any Python object

        :return: does not return
        """
        self._da.append(value)

    def remove(self, value: object) -> bool:
        """
        Removes an item from the bag that coincides with the value passed.

        :param value: any Python object

        :return: a boolean (True if the value passed is removed and False otherwise)
        """

        for index in range(self._da.length()):
            if self._da[index] == value:
                self._da.remove_at_index(index)
                return True
        return False

    def count(self, value: object) -> int:
        """
        Counts the number of items in the bag that coincides with the value passed.

    :param value: any Python object

    :return: an integer
        """
        final_count = 0
        for index in range(self._da.length()):
            if self._da[index] == value:
                final_count += 1

        return final_count

    def clear(self) -> None:
        """
        Clears all items in the bag.

        :param: no parameters

        :return: does not return
        """
        self._da = DynamicArray()

    def equal(self, second_bag: "Bag") -> bool:
        """
        Compares elements of two bag objects.

        :param second_bag: Bag object

        :returns: a boolean (True if the bags are equal, False otherwise)
        """

        flag = True
        counter = 0

        # If both objects do not have the same cardinality they are not equal
        if second_bag.size() != self._da.length():
           return False

        # Check whether the items are the same in both objects
        else:
            for index in range(self._da.length()):
                for pos in range(self._da.length()):
                    if self._da[index] == self._da[pos]:
                        counter += 1

                if second_bag.count(self._da[index]) != counter:
                    flag = False
                counter = 0
        return flag

    def __iter__(self):
        """
        Makes the Bag object a iterable object.

        :param: no parameters

        :return: an iterator Bag object
        """
        self._index = 0

        return self

    def __next__(self):
        """
        Returns the next item in the bag based on the current index
        of the iterator.

        :param: no parameters

        :return: a Python object (each item of an array)
        """
        try:
            value = self._da[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# add example 1")
    bag = Bag()
    print(bag)
    values = [10, 20, 30, 10, 20, 30]
    for value in values:
        bag.add(value)
    print(bag)

    print("\n# remove example 1")
    bag = Bag([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(bag)
    print(bag.remove(7), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)

    print("\n# count example 1")
    bag = Bag([1, 2, 3, 1, 2, 2])
    print(bag, bag.count(1), bag.count(2), bag.count(3), bag.count(4))

    print("\n# clear example 1")
    bag = Bag([1, 2, 3, 1, 2, 3])
    print(bag)
    bag.clear()
    print(bag)

    print("\n# equal example 1")
    bag1 = Bag([10, 20, 30, 40, 50, 60])
    bag2 = Bag([60, 50, 40, 30, 20, 10])
    bag3 = Bag([10, 20, 30, 40, 50])
    bag_empty = Bag()

    print(bag1, bag2, bag3, bag_empty, sep="\n")
    print(bag1.equal(bag2), bag2.equal(bag1))
    print(bag1.equal(bag3), bag3.equal(bag1))
    print(bag2.equal(bag3), bag3.equal(bag2))
    print(bag1.equal(bag_empty), bag_empty.equal(bag1))
    print(bag_empty.equal(bag_empty))
    print(bag1, bag2, bag3, bag_empty, sep="\n")

    bag1 = Bag([100, 200, 300, 200])
    bag2 = Bag([100, 200, 30, 100])
    print(bag1.equal(bag2))

    print("\n# __iter__(), __next__() example 1")
    bag = Bag([5, 4, -8, 7, 10])
    print(bag)
    for item in bag:
        print(item)

    print("\n# __iter__(), __next__() example 2")
    bag = Bag(["orange", "apple", "pizza", "ice cream"])
    print(bag)
    for item in bag:
        print(item)
