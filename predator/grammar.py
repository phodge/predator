class Item:
    """
    Base class for grammar objects that matches text.
    """


class Word(Item):
    """
    A grammar object that matches a whole word, respecting word boundaries.
    """


class Literal(Item):
    """
    A grammar object that matches text equal to an exact string.
    """


class Regex(Item):
    """
    A grammar object that matches text using a regular expression.
    """


class Linebreak(Item):
    """
    A grammar object that matches newlines. A special item is needed because
    the input stream doesn't store newline characters.
    """


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