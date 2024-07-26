# Name: Andre Simao Osorio de Barros
# OSU Email: simaoosa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 04
# Due Date: Jul 29, 2024
# Description: Creation of a Binary Search Tree class.


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    def print_tree(self):
        """
        Prints the tree using the print_subtree function.

        This method is intended to assist in visualizing the structure of the
        tree. You are encouraged to add this method to the tests in the Basic
        Testing section of the starter code or your own tests as needed.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.get_root():
            self._print_subtree(self.get_root())
        else:
            print('(empty tree)')

    def _print_subtree(self, node, prefix: str = '', branch: str = ''):
        """
        Recursively prints the subtree rooted at this node.

        This is intended as a 'helper' method to assist in visualizing the
        structure of the tree.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """

        def add_junction(string):
            if len(string) < 2 or branch == '':
                return string
            junction = '|' if string[-2] == '|' else '`'
            return string[:-2] + junction + '-'

        if not node:
            print(add_junction(prefix) + branch + "None")
            return

        if len(prefix) > 2 * 16:
            print(add_junction(prefix) + branch + "(tree continues)")
            return

        if node.left or node.right:
            postfix = ' (root)' if branch == '' else ''
            print(add_junction(prefix) + branch + str(node.value) + postfix)
            self._print_subtree(node.right, prefix + '| ', 'R: ')
            self._print_subtree(node.left, prefix + '  ', 'L: ')
        else:
            print(add_junction(prefix) + branch + str(node.value) + ' (leaf)')

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a node to a BST.

        :param value: any Python object

        :return: does not return
        """
        # Creates a new BSTNode object with parameter value before adding to BST
        new_node = BSTNode(value)

        # If BST is empty, creates root with 1st BSTNode
        if self._root is None:
            self._root = new_node
            return

        # Every addition starts checking from root
        cur = self._root                      # cur acts as a pointer to parent node in each subtree or None

        # Adds node to BST interactively
        while cur is not None:
            if value < cur.value:
                if cur.left is None:
                    cur.left = new_node
                    return
                cur = cur.left                # if cur has a left child, cur becomes cur.left to point to next parent
            else:
                if cur.right is None:
                    cur.right = new_node
                    return
                cur = cur.right               # if cur has a right child, cur becomes cur.right to point to next parent

    def remove(self, value: object) -> bool:
        """
        Removes a node from a BST.

        :param value: any Python object

        :return: a boolean (True if a node was removed correctly from the BST, False otherwise)
        """
        node = self._root
        node, is_removed = self._remove_rec(node, value)
        return is_removed

        # self._root, deleted = self._remove_rec(self._root, value)
        # return deleted
    def _remove_rec(self, node: BSTNode, value) -> tuple:
        """
        Removes a leaf node from a BST recursively.

        :param remove_node: a BSTNode

        :return: does not return
        """
        # BST is empty or root is None:
        if node is None:
            return False, node

        # Finds the node and removes it
        if value < node.value:
            node.left, is_removed = self._remove_rec(node.left, value)

        elif value > node.value:
            node.right, is_removed = self._remove_rec(node.right, value)

        # Case 1: Remove a leaf (no left or right child) and a node with 1 child
        else:
            if node.right is None and node.left is None:
                return
            elif node.right is None:
                return node.left, True
            elif node.left is None:
                return node.right, True

        # Case 2: Removes a node with 2 children (left and right)
            min_val = self._minVal(node.right)
            node.value = min_val.value
            node.right, _ = self._remove_rec(node.right, min_val.value)
            return node, True

        return node, is_removed

    def _minVal(self, node: BSTNode) -> object:
        """
        Removes a node with one child node, either left or right recursively.

        :param remove_node: a BSTNode object

        :return: does not return

        """
        while node.left:
            node = node.left
        return node

    def contains(self, value: object) -> bool:
        """
        TODO: Write your implementation
        """
        pass

    def inorder_traversal(self) -> Queue:
        """
        TODO: Write your implementation
        """
        pass

    def find_min(self) -> object:
        """
        TODO: Write your implementation
        """
        pass

    def find_max(self) -> object:
        """
        TODO: Write your implementation
        """
        pass

    def is_empty(self) -> bool:
        """
        TODO: Write your implementation
        """
        pass

    def make_empty(self) -> None:
        """
        TODO: Write your implementation
        """
        pass


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)
        tree.print_tree()

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    # print("\nPDF - method remove() example 1")
    # print("-------------------------------")
    # test_cases = (
    #     ((1, 2, 3), 1),
    #     ((1, 2, 3), 2),
    #     ((1, 2, 3), 3),
    #     ((50, 40, 60, 30, 70, 20, 80, 45), 0),
    #     ((50, 40, 60, 30, 70, 20, 80, 45), 45),
    #     ((50, 40, 60, 30, 70, 20, 80, 45), 40),
    #     ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    # )
    # for case, del_value in test_cases:
    #     tree = BST(case)
    #     print('INPUT  :', tree, "DEL:", del_value)
    #     tree.remove(del_value)
    #     print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.print_tree()
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.print_tree()
        print('')

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
