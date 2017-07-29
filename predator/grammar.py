from predator.common import WORD_RE, GrammarConstructionError


class Item:
    """
    Base class for grammar objects that matches text.
    """
    item_name = None

    def __init__(self, name):
        super().__init__()

        if not (name is None or WORD_RE.fullmatch(name)):
            err = 'Invalid Item name {!r}'.format(name)
            raise GrammarConstructionError(err)

        self.item_name = name


class Word(Item):
    """
    A grammar object that matches a whole word, respecting word boundaries.
    """
    def __init__(self, word):
        super().__init__(None)

        if not WORD_RE.fullmatch(word):
            err = 'Not a valid word: {!r}'.format(word)
            raise GrammarConstructionError(err)

        self._word = word

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, self._word)


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
