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
