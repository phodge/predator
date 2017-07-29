from predator.grammar.common import Item


class Sequence(Item):
    """
    A grammar object that matches text using a fixed sequence of child Items.
    """


class Whitespace(Sequence):
    """
    A grammar object that matches whitespace.
    """
