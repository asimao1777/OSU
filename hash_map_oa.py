# Name: Andre Simao Osorio de Barros
# OSU Email: simaoosa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 06
# Due Date: Aug 13, 2024
# Description: Creation of a Hashmap class using open addressing for collision resolution

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in a Hashmap object.

        :param key: a Python string instance.
        :param value: any Python object

        :return: does not return
        """

        # Checks if load factor is >= 0.5 and if it is resizes the hash
        load_factor = self.table_load()
        if load_factor >= 0.5:
            self.resize_table(self.get_capacity() * 2)

        # Applies hash function to capacity to get hash index
        hash_index = self._hash_function(key) % self.get_capacity()

        # Start quadratic probing
        quad_index = hash_index
        prob_index = 1                              # Quadratic probe index

        # Traverses the array checking key/value pairs
        while self._buckets.get_at_index(quad_index) is not None:
            curr = self._buckets.get_at_index(quad_index)

            # Replaces value if key matches and is not a tombstone
            if curr.key == key and not curr.is_tombstone:
                curr.value = value
                return

            # If key matches but is a tombstone, places key/value on spot
            if curr.key == key and curr.is_tombstone:
                curr.value = value
                curr.is_tombstone = False
                self._size += 1
                return

            # Recalculates new quad index using quadratic probing formula
            quad_index = (hash_index + prob_index ** 2) % self._capacity
            prob_index += 1

        # If no match is found, insert a new entry
        self._buckets.set_at_index(quad_index, HashEntry(key, value))
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash map to a new capacity and rehashes all
        key/value pairs.

        :param new_capacity: an integer

        :return: does not return
        """

        # Checks if new capacity is a prime number and greater than the number of items
        if new_capacity < self.get_size():
            return

        new_capacity = self._next_prime(new_capacity)

        # Stores the current buckets and reset the hash map
        curr_buckets = self._buckets
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0

        # Initializes new buckets
        for _ in range(self._capacity):
            self._buckets.append(None)

        # Rehashes all non-tombstone entries from the current buckets
        for index in range(curr_buckets.length()):
            curr = curr_buckets.get_at_index(index)
            if curr is not None and not curr.is_tombstone:
                self.put(curr.key, curr.value)

    def table_load(self) -> float:
        """
        Calculates and returns the current hash table load factor.

        :param: a Hashmap object

        :return: a float
        """
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Checks and returns the number of empty buckets in a HashMap instance.

        :param: a Hashmap object

        :return: an integer
        """
        count = 0
        for index in range(self._buckets.length()):
            if (self._buckets.get_at_index(index) is None or
                    self._buckets.get_at_index(index).is_tombstone):
                count += 1

        return count

    def get(self, key: str) -> object:
        """
        Finds the value associated to a key in a Hashmap object.

        :param key: a Python string instance

        :return: any Python object
        """
        # Applies hash function to capacity to get hash index
        hash_index = self._hash_function(key) % self.get_capacity()

        # Start quadratic probing
        quad_index = hash_index
        prob_index = 1

        # Traverses the array checking key/value pairs
        while self._buckets.get_at_index(quad_index) is not None:
            curr = self._buckets.get_at_index(quad_index)

            # Returns value if key matches and is not a tombstone
            if curr.key == key and not curr.is_tombstone:
                return curr.value

            # Recalculates new quad index using quadratic probing formula
            quad_index = (hash_index + prob_index ** 2) % self._capacity
            prob_index += 1

        return None

    def contains_key(self, key: str) -> bool:
        """
        Checks if a key passed as a parameter exists in a Hashmap object

        :param key: a Python string instance.

        :return: a Boolean (True if the key is in the Hashmap object, False otherwise).
        """
        # Applies hash function to capacity to get hash index
        hash_index = self._hash_function(key) % self.get_capacity()

        # Start quadratic probing
        quad_index = hash_index
        prob_index = 1

        # Traverses the array checking key/value pairs
        while self._buckets.get_at_index(quad_index) is not None:
            curr = self._buckets.get_at_index(quad_index)

            # Returns True if key matches and is not a tombstone
            if curr.key == key and not curr.is_tombstone:
                return True

            # Recalculates new quad index using quadratic probing formula
            quad_index = (hash_index + prob_index ** 2) % self._capacity
            prob_index += 1

        return False

    def remove(self, key: str) -> None:
        """
        Removes the key passed as parameter and its associated value from the Hashmap object.

        :param key: a Python string instance.

        :return: does not return
        """
        # Applies hash function to capacity to get hash index
        hash_index = self._hash_function(key) % self.get_capacity()

        # Start quadratic probing
        quad_index = hash_index
        prob_index = 1

        # Traverses the array looking for key/value pair to remove
        while self._buckets.get_at_index(quad_index) is not None:
            curr = self._buckets.get_at_index(quad_index)

            # Removes the key/pair value and replaces with a tombstone
            if curr.key == key and not curr.is_tombstone:
                curr.is_tombstone = True
                self._size -= 1
                return

            # Recalculates new quad index using quadratic probing formula
            quad_index = (hash_index + prob_index ** 2) % self._capacity
            prob_index += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Traverses a Hashmap object and retrieves keys/values tuples stored in it.

        :param: a Hashmap object.

        :return: DynamicArrays instances containing tuples of keys/values
        """
        final_array = DynamicArray()

        # Traverses array, takes key/value pair from position and append to final array.
        for index in range(self._buckets.length()):
            curr = self._buckets.get_at_index(index)
            if curr is not None and not curr.is_tombstone:
                final_array.append((curr.key, curr.value))

        return final_array

    def clear(self) -> None:
        """
        Clears the contents of a Hashmap object without changing its capacity.

        :param key: a Hashmap object

        :return: does not return
        """

        for index in range(self.get_capacity()):
            self._buckets[index] = DynamicArray()
        self._size = 0

    def __iter__(self):
        """
        Returns an iterator for the hash map.

        :param: a Hashmap object

        :return: an iterator
        """
        self._current = 0

        # Finds the first non-tombstone entry to start iteration
        while self._current < self.get_capacity():
            entry = self._buckets.get_at_index(self._current)
            if entry is not None and not entry.is_tombstone:
                break
            self._current += 1

        return self

    def __next__(self):
        """
        Returns the next key/value pair in the hash map.

        :param: a Hashmap object

        :return: the next key/value pair in the hash map
        """

        while self._current < self.get_capacity():
            entry = self._buckets.get_at_index(self._current)
            self._current += 1
            if entry is not None and not entry.is_tombstone:
                return entry

        raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
