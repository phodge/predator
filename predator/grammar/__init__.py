class Choice(Item):
    """
    A grammar object that attempts to match text using one of several other
    grammar Items.
    """


class Sequence(Item):
    """
    A grammar object that matches text using a fixed sequence of child Items.
    """


class Whitespace(Sequence):
    """
    A grammar object that matches whitespace.
    """


__all__ = [
    'Item',
    'Word',
    'Literal',
    'Regex',
    'Linebreak',
    'Choice',
    'Sequence',
    'Whitespace',
]
