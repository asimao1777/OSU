# Name: Andre Simao Osorio de Barros
# OSU Email: simaoosa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 02
# Due Date: Jul 15, 2024
# Description: Creation of several methods for the class DynamicArray.



from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Creates a new DynamicArray object which capacity is resized

        :param new_capacity: integer

        :return: previous DynamicArray object or does not return
        """

        # Data validation for new capacity
        if new_capacity <= 0 or new_capacity < self._size:
            return

        new_arr = StaticArray(new_capacity)

        for pos in range(self._size):
            new_arr[pos] = self._data[pos]

        self._data = new_arr
        self._capacity = new_capacity

    def append(self, value: object) -> None:
        """
        Adds an element at the end of the DynamicArray object

        :param value: any data type object

        :return: does not return
        """
        # Checks size and capacity and appends value at the end of array (resized or not)
        if self._size == self._capacity:
            self.resize(2 * self._capacity)

        self._data[self._size] = value
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts an element in the DynamicArray object at a specific index

        :param index: integer
        :param value: any data type object

        :return: does not return
        """
        # Data validation
        if index < 0 or index > self._size:
            raise DynamicArrayException("Invalid index.")

        # Checks if current array needs to be resized
        if self._size == self._capacity:
            self.resize(self._capacity*2)

        # Moves elements down the array to insert the new one
        for pos in range(self._size, index, -1):
            self._data[pos] = self._data[pos-1]

        # Inserts the new element in the array
        self._data[index] = value
        self._size += 1

    def remove_at_index(self, index: int) -> None:
        """
        Removes an element in the DynamicArray object at a specific index

        :param index: integer

        :return: does not return
        """
        # Data validation
        if index < 0 or index >= self._size:
            raise DynamicArrayException("Invalid index.")

        # Checks if current array needs to be resized
        if self._capacity > 10 and self._size < (self._capacity / 4):
            new_cap = max(self._size * 2, 10)
            self.resize(new_cap)

        # Moves elements up the array removing the element at the index
        for pos in range(index + 1, self._size):
            self._data[pos-1] = self._data[pos]

        # Turns the last element to 0
        self._data[self._size-1] = 0
        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Slices a DynamicArray object creating a new DynamicArray object as a subset.

        :param start_index: integer
        :param size: integer

        :return: a DynamicArray object
        """
        # Data Validation
        if ((start_index < 0 or start_index >= self._size)
                or (size > (self._size - start_index))
                or (size < 0)):
            raise DynamicArrayException

        output_arr = DynamicArray()

        # Slices the current array and creates a subset into a new array
        for pos in range(start_index, start_index + size):
            output_arr.append(self._data[pos])

        return output_arr

    def merge(self, second_da: "DynamicArray") -> None:
        """
        Merges a passed DynamicArray object to the existing

        :param second_da: DynamicArray object

        :return: does not return
        """
        for pos in range(second_da.length()):
            self.append(second_da[pos])

    def map(self, map_func) -> "DynamicArray":
        """
        Creates a new DynamicArray object by applying a function to each
        element of current array.

        :param map_func: a function

        :return: a DynamicArray object
        """
        # Creates a new DynamicArray object (new array)
        output_arr = DynamicArray()

        # Passes each item of current array to function and append to new array
        for pos in range(self.length()):
            output_arr.append(map_func(self._data[pos]))

        return output_arr

    def filter(self, filter_func) -> "DynamicArray":
        """
        Creates a new DynamicArray object by applying a filter function to the current array.

        :param filter_func: a function

        :return: a DynamicArray object
        """
        # Creates a new DynamicArray object (new array)
        output_arr = DynamicArray()

        # Passes each item of current array to function and, if True, append item to new array
        for pos in range(self.length()):
            res_bool = filter_func(self._data[pos])
            if res_bool:
                output_arr.append(self._data[pos])

        return output_arr

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Applies a function to all items in the current array and returns the
        resulting value and the current array.

        :param reduce_func: a function
        :param initializer: an integer

        :return: an integer or None
        """

        # Checks conditions and apply reduce_func accordingly
        if initializer is None and self._size > 1:
            first_iter = reduce_func(self._data[0], self._data[1])
            for pos in range(2, self._size):
                first_iter = reduce_func(first_iter, self._data[pos])
            return first_iter
        elif initializer is not None and self._size == 1:
            return reduce_func(initializer, self._data[0])
        elif self._size == 0:
            return initializer
        elif self._size == 1:
            return self._data[0]
        else:
            first_iter = reduce_func(initializer, self._data[0])
            for pos in range(1, self._size):
                first_iter = reduce_func(first_iter, self._data[pos])
            return first_iter


def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Determines the mode or modes for and its frequency from a DynamicArray object.

    :param arr: DynamicArray object

    :return: a tuple with a DynamicArray object and an integer
    """

    count = 1
    num = arr[0]
    max = 1                                     # frequency of the mode or modes
    mode = DynamicArray()                       # mode array created to deal with count = max for first 2 items

    # Checks for the mode and frequency of items
    for index in range(1, arr.length()):
        if arr[index] == num:
            count += 1
        else:
            if count > max:
                max = count
                mode = DynamicArray()            # created to overwrite previous mode in the mode array if count > max
                mode.append(num)
            elif count == max:
                mode.append(num)                 # if count = max, then appends the num to current mode array
            num = arr[index]
            count = 1

    # Checks for the last item in the array
    if count > max:
        max = count
        mode = DynamicArray()                    # created to overwrite previous mode in the mode array if count > max
        mode.append(num)
    elif count == max:
        mode.append(num)                         # if count = max, then appends the num to current mode array

    return mode, max


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()
    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()
    #
    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(948)
    print(da)
    da.resize(8)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    # print("\n# slice example 1")
    # da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    # da_slice = da.slice(1, 3)
    # print(da, da_slice, sep="\n")
    # da_slice.remove_at_index(0)
    # print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        # print(find_mode(da))
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")

