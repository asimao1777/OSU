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
        cur = self._root                                    # cur acts as a pointer to parent node in each subtree

        # Adds node to BST interactively
        while cur is not None:
            if value < cur.value:
                # if cur has a left child, cur becomes cur.left to point to next parent
                if cur.left is None:
                    cur.left = new_node
                    return
                cur = cur.left
            else:
                # if cur has a right child, cur becomes cur.right to point to next parent
                if cur.right is None:
                    cur.right = new_node
                    return
                cur = cur.right

    def remove(self, value: object) -> bool:
        """
        Removes a value from the tree while maintaining BST property.

        :param value: any Python object

        :return: a boolean (True if a node was removed correctly from the BST, False otherwise)
        """

        node = self._root                                   # start the search for removal at tree root
        node, is_removed = self._remove_rec(node, value)    # recursively finds and removes the node, if exists
        self._root = node                                   # the new root of the tree or subtree is the returned node

        return is_removed

    def _remove_rec(self, node: BSTNode, value: object) -> tuple:
        """
        Helper method which finds and removes a leaf
        node, a node with one child or 2 children
        from a BST, recursively.

        :param node: a BSTNode instance
        :param value: any Python object

        :return: does not return
        """
        # BST is empty or root is None:
        if node is None:
            return node, False

        # Finds the node traversing the BST
        if value < node.value:
            node.left, is_removed = self._remove_rec(node.left, value)

        elif value > node.value:
            node.right, is_removed = self._remove_rec(node.right, value)

        # Case 1: Remove a leaf (no left or right child) and a node with 1 child
        else:
            is_removed = True
            if node.right is None:
                return node.left, is_removed
            elif node.left is None:
                return node.right, is_removed

            # Case 2: Removes a node with 2 children (left and right)
            min_val = self._minVal(node.right)             # looks for the inorder success
            node.value = min_val.value                     # replaces the value to be removed by the inorder successor

            # Removes the inorder successor node after it replaced the removed node value
            node.right, _ = self._remove_rec(node.right, min_val.value)

            # Checks if the node was not removed and returns if not
            if not is_removed:
                return node, is_removed

        return node, is_removed

    def _minVal(self, node: BSTNode) -> object:
        """
        Helper method which finds the inorder successor
        of a node with 2 children which will be removed from the BST

        :param node: a BSTNode instance

        :return: does not return

        """
        # Finds the lowest value node on the left of the node to be removed
        while node.left:
            node = node.left
        return node

    def contains(self, value: object) -> bool:
        """
        Looks for the existence of a value into a node in a BST.

        :param value: any Python object

        :return: a Boolean (True if the node value exists in a BST, False otherwise)
        """
        # Empty BST
        if self._root is None:
            return False

        cur = self._root

        # Looks for the node containing the value iteratively.
        while value != cur.value:
            if value < cur.value:
                if cur.left is None:
                    return False
                cur = cur.left
            else:
                if value > cur.value:
                    if cur.right is None:
                        return False
                    cur = cur.right
        return True

    def inorder_traversal(self) -> Queue:
        """
        Performs an inorder traversal of the tree.

        :param: an instance of a BST class.

        :return: an instance of a queue (with the values of the visited nodes)
        """
        # Helper inside method to allow for the creation of the queue before recursion
        def _inorder_traversal_rec(node):

            if node is not None:
                _inorder_traversal_rec(node.left)           # when reached "None" returns nothing and continues code
                final_queue.enqueue(node.value)             # Because left subtree reached "None", adds last node value
                _inorder_traversal_rec(node.right)          # when reaches "None" returns nothing

        final_queue = Queue()

        # Check if BST is empty
        if self._root is None:
            return final_queue

        # Traverses BST inorder recursively
        _inorder_traversal_rec(self._root)

        return final_queue

    def find_min(self) -> object:
        """
        Finds the lowest value in a BST.

        :param: an instance of the BST class.

        :return: any Python object
        """
        # Check if BST is empty
        if self._root is None:
            return None

        # Finds smallest value
        queue = self.inorder_traversal()
        return queue._data[0]

    def find_max(self) -> object:
        """
        Finds the highest value in a BST.

        :param: an instance of the BST class.

        :return: any Python object
        """
        # Check if BST is empty
        if self._root is None:
            return None

        # Finds largest value
        queue = self.inorder_traversal()
        return queue._data[-1]

    def is_empty(self) -> bool:
        """
        Checks if the BST is empty.

        :param: an instance of the BST class.

        :return: a boolean (True if it is empty, False otherwise)

        """
        if self._root is None:
            return True
        return False

    def make_empty(self) -> None:
        """
        Removes all nodes from a BST.

        :param: an instance of the BST class.

        :return: does not return
        """

        if self._root is None:
            return None
        self._root = None


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

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

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
