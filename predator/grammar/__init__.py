import re

from predator.common import WORD_RE, GrammarConstructionError

LINEBREAK_ITEM_NAME = '__LINEBREAK__'


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
    def __init__(self, chars, *, name=None):
        super().__init__(name)

        if not len(chars):
            err = 'A Literal cannot have an empty character list'
            raise GrammarConstructionError(err)

        if '\n' in chars or '\r' in chars:
            err = 'Literal cannot be used to match "\\r" or "\\n".'
            err += ' Use a Linebreak instead.'
            raise GrammarConstructionError(err)

        self._chars = chars

    def __repr__(self):
        return '<{}{} {}>'.format(
            self.__class__.__name__,
            '[{}]'.format(self.item_name) if self.item_name else '',
            repr(self._chars))


class Regex(Item):
    """
    A grammar object that matches text using a regular expression.
    """
    def __init__(self, name, pattern):
        import sre_constants

        super().__init__(name)

        self._pattern = pattern

        if not len(pattern):
            err = 'Regex cannot use an empty pattern'
            raise GrammarConstructionError(err)

        try:
            self._regex = re.compile(pattern, re.MULTILINE)
        except sre_constants.error as err:
            msg = "Regex compilation failed: " + str(err)
            raise GrammarConstructionError(msg)

    def __repr__(self):
        return '<{}{} /{}/>'.format(
            self.__class__.__name__,
            '[{}]'.format(self.item_name) if self.item_name else '',
            self._regex.pattern)


class Linebreak(Item):
    """
    A grammar object that matches newlines. A special item is needed because
    the input stream doesn't store newline characters.
    """
    def __init__(self):
        super().__init__(LINEBREAK_ITEM_NAME)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)


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
