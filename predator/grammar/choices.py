from predator.grammar.common import Item


class Choice(Item):
    """
    A grammar object that attempts to match text using one of several other
    grammar Items.
    """
    def __init__(self, name=None):
        super().__init__(name)

        self._choices = []

    def addchoice(self, item):
        assert isinstance(item, Item)
        self._choices.append(item)
