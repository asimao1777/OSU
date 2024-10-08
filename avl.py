# Name: Andre Simao Osorio de Barros
# OSU Email: simaoosa@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 04
# Due Date: Jul 29, 2024
# Description: Creation of an AVL class.

import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    def add(self, value: object) -> None:
        """
        Adds a new value to the tree while maintaining AVL property

        :param value: any Python object

        :return: does not return
        """
        new_node = AVLNode(value)

        # Check of Tree is empty
        if self._root is None:
            self._root = new_node                          # empty tree, new node is the only node (tree is balanced)
        else:
            self._root = self._add_rec(self._root, value)  # tree is not empty, add node, re-balance from bottom-up

    def _add_rec(self, node: AVLNode, value: object) -> AVLNode:
        """
        Helper method to adds a new value to the tree and re-balancing the tree
        from bottom to top following the same path down.

        :param node: an AVLNode instance (root of the tree or a subtree)
        :param value: any Python object

        :return: an AVLNode instance
        """
        # Checks if the tree is empty
        if node is None:
            return AVLNode(value)

        # Add node to the tree keeping BST property
        if value < node.value:
            node.left = self._add_rec(node.left, value)
            node.left.parent = node
        elif value > node.value:
            node.right = self._add_rec(node.right, value)
            node.right.parent = node
        else:
            return node                                    # if the value exists in the tree, do nothing and return

        self._update_height(node)                          # updates the height of the node
        return self._rebalance(node)                       # re-balances the BST to ensure AVL property and return

    def remove(self, value: object) -> bool:
        """
        Removes a value from the tree while maintaining AVL property

        :param value: any Python object

        :return: True if the value was removed, False otherwise
        """

        node = self._root                                   # start the search for removal at tree root
        node, is_removed = self._remove_rec(node, value)    # recursively finds and removes the node, if exists
        self._root = node                                   # the new root of the tree or subtree is the returned node

        return is_removed

    def _remove_rec(self, node: AVLNode, value: object) -> tuple:
        """
        Helper method which finds and removes a leaf
        node, a node with one child or 2 children
        from a BST, recursively, updates the node height,
        and re-balances the BST to
        maintain AVL property.

        :param node: an AVLNode instance
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
            min_val = self._minVal(node.right)              # looks for the inorder success
            node.value = min_val.value                      # replaces the value to be removed by the inorder successor

            # Removes the inorder successor node after it replaced the removed node value
            node.right, _ = self._remove_rec(node.right, min_val.value)

            # Checks if the node was not removed and returns if not
            if not is_removed:
                return node, is_removed

        self._update_height(node)                          # updates the height of the node
        return self._rebalance(node), is_removed           # re-balances the BST to ensure AVL property and return

    def _minVal(self, node: AVLNode) -> AVLNode:
        """
        Helper method which finds the inorder successor
        of a node with 2 children which will be removed from the BST

        :param node: a AVLNode instance

        :return: does not return

        """
        # Finds the lowest value node on the left of the node to be removed
        while node.left is not None:
            node = node.left
        return node

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Calculates the balance factor

        :param node: an AVLNode instance

        :return: an integer

        """
        if node.left:
            left_height = node.left.height
        else:
            left_height = -1

        if node.right:
            right_height = node.right.height
        else:
            right_height = -1

        return right_height - left_height

    def _get_height(self, node: AVLNode) -> int:
        """
        Returns the height of a node

        :param node: an AVLNode instance

        :return: an integer
        """
        if not node:
            return -1
        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Simple rotates R-R imbalanced subtrees.

        :param node: an AVLNode instance (node for which the rotation is centered)

        :returns: an AVLNode instance (the new parent node for a balanced subtree)
        """
        # Sets the new parent node and reassigns the right child of current node
        new_parent = node.right
        node.right = new_parent.left

        # Updates the parent of the new right child and reassigns left child of new parent
        if node.right is not None:
            node.right.parent = node
        new_parent.left = node
        # Updates the parent of the new parent node
        new_parent.parent = node.parent        # the parent of the new parent is set to the parent of the current node

        # Updates root if applicable and links new parent with the correct subtree of its parent
        if node.parent is None:
            self._root = new_parent
        else:
            # Updates the parent's left or right child to be the new parent
            if node.parent.left == node:
                node.parent.left = new_parent
            else:
                node.parent.right = new_parent

        # Updates the parent of the current node
        node.parent = new_parent               # sets the parent of the current node to be the new parent

        # Updates the heights of the nodes
        self._update_height(node)
        self._update_height(new_parent)

        return new_parent

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Simple rotates L-L imbalanced subtrees.

        :param node: an AVLNode instance (node for which the rotation is centered)

        :returns: an AVLNode instance (the new parent node for a balanced subtree)
        """
        # Sets the new parent node and reassigns the left child of current node
        new_parent = node.left
        node.left = new_parent.right

        # Updates the parent of the new left child and reassigns right child of new parent
        if node.left is not None:
            node.left.parent = node
        new_parent.right = node
        # Updates the parent of the new parent node
        new_parent.parent = node.parent         # the parent of the new parent is set to the parent of the current node

        # Updates root if applicable and links new parent with the correct subtree of its parent
        if node.parent is None:
            self._root = new_parent
        else:
            # Updates the parent's left or right child to be the new parent
            if node.parent.left == node:
                node.parent.left = new_parent
            else:
                node.parent.right = new_parent

        # Updates the parent of the current node
        node.parent = new_parent

        # Updates the heights of the nodes
        self._update_height(node)               # sets the parent of the current node to be the new parent
        self._update_height(new_parent)

        return new_parent

    def _update_height(self, node: AVLNode) -> None:
        """
        Updates the height of the AVLNode whose subtree was restructured.

         :param node: an AVLNode instance.

        :returns: does not return
        """
        # Checks if node is a leaf (if a leaf height is -1)
        if node.left is not None:
            left_h = node.left.height
        else:
            left_h = -1

        if node.right is not None:
            right_h = node.right.height
        else:
            right_h = -1

        # Updates the height of the node
        node.height = 1 + max(left_h, right_h)

    def _rebalance(self, node: AVLNode) -> AVLNode:
        """
        Rebalances an imbalanced subtree(s) after the insert or removal of an AVL node.

        :param node: an AVLNode instance

        :return: the new root of the balanced subtree
        """
        balance = self._balance_factor(node)

        # Checks if the tree is imbalanced and re-balances it
        if balance < -1:
            # Left-Right imbalance
            if self._balance_factor(node.left) > 0:
                node.left = self._rotate_left(node.left)
            # Left-Left imbalance
            node = self._rotate_right(node)
        elif balance > 1:
            # Right-Left imbalance
            if self._balance_factor(node.right) < 0:
                node.right = self._rotate_right(node.right)
            # Right-Right imbalance
            node = self._rotate_left(node)

        # Updates the height of the node
        self._update_height(node)

        return node

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)
        tree.print_tree()

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.print_tree()
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.print_tree()
        print('')

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
