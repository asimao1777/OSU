class SLNode:
    """
    Singly Linked List Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object, next=None) -> None:
        self._head = None
        self.value = value
        self.next = next
