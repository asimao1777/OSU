# Name: Andre Simao Osorio de Barros
# OSU Email: simaoosa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 06
# Due Date: Aug 13, 2024
# Description: Creation of an Hashmap class using chaining for collision resolution



from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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

        load_factor = self.table_load()
        if load_factor >= 1:
            self.resize_table(self.get_capacity()*2)

        hash_index = self._hash_function(key) % self.get_capacity()
        cur_bucket = self._buckets[hash_index]

        node_key_exist = cur_bucket.contains(key)
        if node_key_exist:
            node_key_exist.value = value
        else:
            cur_bucket.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash map to a new capacity and rehashes all keys.

        :param new_capacity: an integer

        :return: does not return
        """
        if new_capacity == 2:
            new_capacity = 2

        if new_capacity >= 1:
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)

        new_hash = HashMap(new_capacity, self._hash_function)

        for index in range(self.get_capacity()):
            node = self._buckets[index]._head
            while node is not None:
                new_hash.put(node.key, node.value)
                node = node.next

            # Replace the old HashMap attributes with the new ones
        self._buckets = new_hash._buckets
        self._capacity = new_hash._capacity
        self._size = new_hash.get_size()

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
            if self._buckets[index].length() == 0:
                count += 1
        return count

    def get(self, key: str) -> object:
        """
        Finds the value associated to a key in a Hashmap object.

        :param key: a Python string instance

        :return: any Python object
        """

        hash_index = self._hash_function(key) % self.get_capacity()
        cur_bucket = self._buckets[hash_index]

        node_key_exist = cur_bucket.contains(key)
        if node_key_exist:
            return node_key_exist.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Checks if a key passed as a parameter exists in a Hashmap object

        :param key: a Python string instance.

        :return: a Boolean (True if the key is in the Hashmap object, False otherwise).
        """

        hash_index = self._hash_function(key) % self.get_capacity()
        cur_bucket = self._buckets[hash_index]
        if cur_bucket.contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the key passed as parameter and its associated value from the Hashmap object.

        :param key: a Python string instance.

        :return: does not return
        """

        hash_index = self._hash_function(key) % self.get_capacity()
        cur_bucket = self._buckets[hash_index]
        if self.contains_key(key):
            cur_bucket.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Traverses a Hashmap object and retrieves keys/values tuples stored in it.

        :param: a Hashmap object.

        :return: DynamicArrays instances containing tuples of keys/values
        """
        final_array = DynamicArray()
        for index in range(self.get_capacity()):
            node = self._buckets[index]._head
            while node is not None:
                key_val = (node.key, node.value)
                final_array.append(key_val)
                node = node.next
        return final_array

    def clear(self) -> None:
        """
        Clears the contents of a Hashmap object without changing its capacity.

        :param key: a Hashmap object

        :return: does not return
        """

        for index in range(self.get_capacity()):
            self._buckets[index] = LinkedList()
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Determines the mode or modes for and its frequency from a DynamicArray object.

    :param da: DynamicArray object

    :return: a tuple with a DynamicArray object and an integer
    """
    # Checks if array is empty
    if da.length() == 0:
        return DynamicArray(), 0

    freq_map = HashMap()

    # Populates the Hashmap
    for index in range(da.length()):
        key = da[index]
        if freq_map.contains_key(key):
            count = freq_map.get(key)
            freq_map.put(key, count + 1)
        else:
            freq_map.put(key, 1)

    # Finds the maximum frequency (max)
    max = 0
    for index in range(freq_map.get_capacity()):
        node = freq_map._buckets[index]._head
        while node is not None:
            if node.value > max:
                max = node.value
            node = node.next

    # Compares each key/value in the Hashmap and when value is equal to max adds it to array
    mode = DynamicArray()
    for index in range(freq_map.get_capacity()):
        node = freq_map._buckets[index]._head
        while node is not None:
            if node.value == max:
                mode.append(node.key)
            node = node.next

    return mode, max


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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
