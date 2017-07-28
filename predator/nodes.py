class Node:
    """
    Base class for the real node classes (Forks and Tips).
    """


class Tip(Node):
    """
    A member of the syntax tree which doesn't have any children.
    """


class Fork(Node):
    """
    A member of the syntax tree which may have children.
    """
